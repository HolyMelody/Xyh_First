
#include <vector>
#include <iostream>
using namespace std;

//自定义输出函数
// ostream& operator<<(ostream& os, const vector<int>& vec) {
//     os << "[";
//     for (int i = 0; i < vec.size(); ++i) {
//         os << vec[i];
//         if (i != vec.size() - 1) {
//             os << ", ";
//         }
//     }
//     os << "]";
//     return os;
// }
ostream& operator<<(ostream& os, const vector<int>& vec) {
    os << "[";
    for (vector<int>::size_type i = 0; i < vec.size(); ++i) {
        os << vec[i];
        if (i != vec.size() - 1) {
            os << ", ";
        }
    }
    os << "]";
    return os;
}


class DecisionStump {
public:
    int feature; // 特征索引
    double threshold; // 阈值
    int direction; // 方向

    // 构造函数
    DecisionStump(int feature, double threshold, int direction)
        : feature(feature), threshold(threshold), direction(direction) {}

    // 预测函数
    vector<int> predict(const vector<vector<double>>& X) {
        int m = X.size();
        vector<int> y_pred(m, 1);
        for (int i = 0; i < m; ++i) {
            cout<<"X[i][feature]:"<<X[i][feature]<<endl;
            cout<<"direction * X[i][feature]:"<<direction * X[i][feature]<<endl;
            cout<<"direction * threshold:"<<direction * threshold<<endl;
            cout<<"direction * X[i][feature] < direction * threshold:"<<direction * X[i][feature] << direction * threshold<<endl;
            if (direction * X[i][feature] < direction * threshold) {
                y_pred[i] = -1;
            }
        }
        return y_pred;
    }
};
