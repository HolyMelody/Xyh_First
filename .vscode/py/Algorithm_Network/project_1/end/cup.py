from collections import defaultdict
import collections
from math import fabs
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.topology import event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.topology.api import get_switch, get_all_link, get_link
import copy
from ryu.lib.packet import arp
import networkx as nx

import matplotlib.pyplot as plt
from ryu.lib import mac


class Topo(object):
    def __init__(self, logger):

        self.adjacent = defaultdict(lambda s1,s2: None)
        # datapathes
        self.switches = None

        self.logger = logger
        self.graph = {}

    def reset(self):
        self.adjacent = defaultdict(lambda s1,s2: None)
        self.switches = None

    def get_adjacent(self, s1, s2):
        return self.adjacent.get((s1, s2))

    def set_adjacent(self, s1, s2, port):
        self.adjacent[(s1, s2)] = port

    def shortest_path(self, src_sw, dst_sw, first_port, last_port):
        ans=[]
        sign=[0]
            
        for i in range(1,25):
            a=[]
            a=[0] * 20
            sign.append(a)

        stack = []
        #标记的数组
        stack.append(src_sw)
        while len(stack) != 0:
            stack_top = stack[-1]
            nodes_nums = len(self.graph[stack_top])
            for i in self.graph[stack_top]:
                # 未标记且未加入则加入
                dst = self.graph[stack_top].index(i)
                if sign[stack_top][dst] == 0 and i not in stack:
                    stack.append(i)
                    sign[stack_top][dst] = 1
                    break
            # 到终点打印路径
            if dst_sw in stack:
                ans.append((copy.deepcopy)(stack))
                stack.pop()
                continue
            # 如果没有点加入路径，则弹出这个点并重新标记为未标记
            last = stack[-1]
            if last == stack_top:
                # 标记为未访问，并出栈
                sign[stack_top] = [0]*nodes_nums
                stack.pop()
            ############
        print(ans)
        short=[]
        long=[]
        for x in ans:
                short=x
                if len(x)>len(long):
                    long=x
                if len(x)<len(short):
                    short=x
        #print(short)
        #print(long)
        #G = nx.Graph()
        list1=[]
        for key in self.graph.keys():
            q=[]
            q=self.graph[key]
            for nodes in q:
                b=(key,nodes)
                list1.append(b)
        
        #G.add_edges_from(list1)
        #nx.draw(G, pos=nx.circular_layout(G), with_labels=True,edge_color='green')
        list2=[]
        record = []
        inport = first_port
        for s1,s2 in zip(long[:-1],long[1:]):
            a=(s1,s2)
            list2.append(a)
            outport = self.get_adjacent(s1, s2)
            record.append((s1, inport, outport))
            inport = self.get_adjacent(s2, s1)
        #G = nx.DiGraph()
        #G.add_edges_from(list2)
        #nx.draw(G, with_labels=True,edge_color='red')
        #plt.show()
        #######################

        record.append((dst_sw, inport, last_port))
        return record, short ,long

   
# TODO Port status monitor

class DFSController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(DFSController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        # logical switches
        self.datapaths = []

        self.arp_table = {} #知道目标设备的IP地址，查询目标设备的MAC地址
        self.arp_history = {}
        self.rarp_table = {}#Reverse Address Resolution Protocol
        self.topo = Topo(self.logger)
        self.flood_history = {}
        self.switch_num = 0
        # self.is_learning={}
        self.graph = collections.defaultdict(list)
        self.initshow = 0
        self.index = 1
        self.lp_path = []
        self.falg = False


    def set_adj(self,s1,s2):
        self.graph[s1].append(s2)
        self.graph[s2].append(s1)

    def _find_dp(self, dpid):
        for dp in self.datapaths:
            if dp.id == dpid:
                return dp
        return None

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.logger.info("add_flow--dpid:{}".format(datapath.id) )

        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None): 
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    def configure_path(self, longest_path, event, src_mac, dst_mac):
        # configure longest path to switches
        msg = event.msg
        datapath = msg.datapath

        ofproto = datapath.ofproto

        parser = datapath.ofproto_parser

        # enumerate the calculated path
        # (s1,inport,outport)->(s2,inport,outport)->...->(dest_switch,inport,outport)
        for switch, inport, outport in longest_path:
            match = parser.OFPMatch(in_port=inport, eth_src=src_mac, eth_dst=dst_mac)

            actions = [parser.OFPActionOutput(outport)]

            datapath = self._find_dp(int(switch))
            self.logger.info("dpid:{} is:{}".format(datapath, int(switch)))
            assert datapath is not None

            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

            mod = datapath.ofproto_parser.OFPFlowMod(
                datapath=datapath,
                match=match,
                idle_timeout=0,
                hard_timeout=0,
                priority=1,
                instructions=inst
            )
            datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, event):

        # msg is an object which desicribes the corresponding OpenFlow message
        msg = event.msg
        #self.logger.info("packet_in")
        datapath = msg.datapath

        # object for the negotiated Openflow version
        ofproto = datapath.ofproto

        parser = datapath.ofproto_parser

        # through which port the packet comes in
        in_port = msg.match['in_port']

        # self.logger.info("From datapath {} port {} come in a packet".format(datapath.id,in_port))

        # get src_mac and dest mac
        pkt = packet.Packet(msg.data)

        eth = pkt.get_protocols(ethernet.ethernet)[0]

        
        # drop lldpobserve-links命令会导致控制器在运行期间 会不间断地发送LLDP数据包进行链路探测

        #而simple_switch_stp_13中对于lldp包，依然会当做packetin信息处理  ，因此只需要添加以下代码去忽略lldp包就可以了
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # self.logger.info("LLDP")
            return

        # get source and destination mac address
        dst_mac = eth.dst

        src_mac = eth.src

        arp_pkt = pkt.get_protocol(arp.arp)

        # if this is an arp packet,we remember "ip---mac"
        # we learn ip---mac mapping from arp reply and request
        if arp_pkt:
            self.arp_table[arp_pkt.src_ip] = src_mac


        dpid = datapath.id

        self.flood_history.setdefault(dpid, [])
        if '33:33' in dst_mac[:5]:
            # the controller has not flooded this packet before
            if (src_mac, dst_mac) not in self.flood_history[dpid]:
                # we remember this packet
                self.flood_history[dpid].append((src_mac, dst_mac))
            else:
                # the controller have flooded this packet before,we do nothing and return
                return

        if src_mac not in self.mac_to_port.keys():
            self.mac_to_port[src_mac] = (dpid, in_port)

        if dst_mac in self.mac_to_port.keys():

            final_port = self.mac_to_port[dst_mac][1]

            # the first switc
            src_switch = self.mac_to_port[src_mac][0]

            # the final switch
            dst_switch = self.mac_to_port[dst_mac][0]

            self.logger.info("src_switch:{},mac_switch:{}in_port:{}out_port:{}".format(src_switch,dst_switch,in_port,final_port))
           

            result,a,b= self.topo.shortest_path(src_switch,dst_switch,in_port,final_port)
            self.falg = True
            #self.logger.info("最短路:{}".format(a))
            self.logger.info("从{}到{}最长路{}".format(src_switch,dst_switch,b))
            # calculate the longest path
            #self.logger.info("src{},,mac{}in第二{} out{}".format(src_switch,dst_switch,in_port,final_port))
            
            self.configure_path(result, event, src_mac, dst_mac)

            self.logger.info("Configure done")

            # current_switch=None
            out_port = None
            for s, _, op in result:
                # print(s,dpid)
                if s == dpid:
                    out_port = op
            # assert out_port is not None

        else:

            if self.arp_handler(msg):
                return
            out_port = ofproto.OFPP_FLOOD

        # actions= flood or some port
        actions = [parser.OFPActionOutput(out_port)]

        data = None

        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        # send the packet out to avoid packet loss
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data
        )
        datapath.send_msg(out)

    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, event):
        self.switch_status_handler(event)

    def switch_status_handler(self, event):

        self.switch_num += 1
        self.logger.info("SwNum:{} /20".format(self.switch_num))
        if(20==self.switch_num):
            self.logger.info('Topology rediscovery done')
            all_switches = copy.copy(get_switch(self, None))
            # get all datapathid
            # 获取交换机的ID值
            self.topo.switches = [s.dp.id for s in all_switches]

            self.logger.info("switches {}".format(self.topo.switches))

            self.datapaths = [s.dp for s in all_switches]

            # get link and get port
            all_links = copy.copy(get_link(self, None))

            all_link_stats = [(l.src.dpid, l.dst.dpid, l.src.port_no, l.dst.port_no) for l in all_links]

            for s1, s2, p1, p2 in all_link_stats:
                # weight = random.randint(1, 10)
                self.topo.set_adjacent(s1, s2, p1)
                self.topo.set_adjacent(s2, s1, p2)
                self.set_adj(s1, s2)

                
            self.topo.graph = self.graph
 
    def arp_handler(self, msg): #ip->mac

        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)

        eth = pkt.get_protocols(ethernet.ethernet)[0]
        arp_pkt = pkt.get_protocol(arp.arp)

        if eth:
            eth_dst = eth.dst
            eth_src = eth.src

        if eth_dst == mac.BROADCAST_STR and arp_pkt:
            # target ip
            arp_dst_ip = arp_pkt.dst_ip

            # we have met this particular arp request before
            if (datapath.id, eth_src, arp_dst_ip) in self.arp_history:

                if self.arp_history[(datapath.id, eth_src, arp_dst_ip)] != in_port:
                    return True
            else:
                # we didnt met this packet before, record it
                self.arp_history[(datapath.id, eth_src, arp_dst_ip)] = in_port

        if arp_pkt:

            hwtype = arp_pkt.hwtype
            # protocol type
            proto = arp_pkt.proto
            # hardware address length
            hlen = arp_pkt.hlen
            # protocol address length
            plen = arp_pkt.plen

            # specify the operation that the sender is performing:1 for request,2 for reply
            opcode = arp_pkt.opcode

            # src ip
            arp_src_ip = arp_pkt.src_ip
            # dst ip
            arp_dst_ip = arp_pkt.dst_ip

            # arp_request
            if opcode == arp.ARP_REQUEST:

                # we have learned the target ip mac mapping
                if arp_dst_ip in self.arp_table:
                    # send arp reply from in port
                    actions = [parser.OFPActionOutput(in_port)]
                    arp_reply = packet.Packet()

                    arp_reply.add_protocol(ethernet.ethernet(
                        ethertype=eth.ethertype,
                        dst=eth_src,
                        src=self.arp_table[arp_dst_ip]))

                    # add arp protocol
                    arp_reply.add_protocol(arp.arp(
                        opcode=arp.ARP_REPLY,
                        src_mac=self.arp_table[arp_dst_ip],
                        src_ip=arp_dst_ip,
                        dst_mac=eth_src,
                        dst_ip=arp_src_ip))

                    # serialize the packet to binary format 0101010101
                    arp_reply.serialize()
                    # arp reply
                    out = parser.OFPPacketOut(
                        datapath=datapath,
                        buffer_id=ofproto.OFP_NO_BUFFER,
                        in_port=ofproto.OFPP_CONTROLLER,
                        actions=actions, data=arp_reply.data)
                    datapath.send_msg(out)

                    return True
        return False        

    