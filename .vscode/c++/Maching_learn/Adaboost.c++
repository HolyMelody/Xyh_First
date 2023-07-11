#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <numeric>
#include <limits>

using namespace std;

// 决策树桩
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
            if (direction * X[i][feature] < direction * threshold) {
                y_pred[i] = -1;
            }
        }
        return y_pred;
    }
};

// Adaboost分类器
class Adaboost {
public:
    int n_learners; // 决策树桩数量
    vector<DecisionStump> learners; // 决策树桩集合
    vector<double> alphas; // 决策树桩权重

    // 构造函数
    Adaboost(int n_learners) : n_learners(n_learners) {}

    // 拟合函数
    void fit(const vector<vector<double>>& X, const vector<int>& y) {
        int m = X.size();
        int n = X[0].size();
        vector<double> w(m, 1.0 / m); // 初始化样本权重

        for (int k = 0; k < n_learners; ++k) {
            DecisionStump best_learner(0, 0.0, 1); // 最佳决策树桩
            double best_error = numeric_limits<double>::infinity(); // 最小误差

            // 遍历特征寻找最佳决策树桩
            for (int feature = 0; feature < n; ++feature) {
                for (const auto& xi : X) {
                    double threshold = xi[feature]; // 阈值
                    for (int direction : {1, -1}) { // 方向
                        vector<int> y_pred = (DecisionStump(feature, threshold, direction)).predict(X);
                        double error = 0;
                        for (int i = 0; i < m; ++i) {
                            if (y_pred[i] != y[i]) {
                                error += w[i];
                            }
                        }

                        if (error < best_error) { // 更新最佳决策树桩
                            best_error = error;
                            best_learner = DecisionStump(feature, threshold, direction);
                        }
                    }
                }
            }

            vector<int> y_pred = best_learner.predict(X); // 最佳决策树桩的预测结果
            double err = 0;
            for (int i = 0; i < m; ++i) {
                if (y_pred[i] != y[i]) {
                    err += w[i];
                }
            }
            double alpha = 0.5 * log((1 - err) / err); // 计算该决策树桩的权重
            for (int i = 0; i < m; ++i) {
                w[i] *= exp(-alpha * y[i] * y_pred[i]); // 更新样本权重
            }
            double w_sum = accumulate(w.begin(), w.end(), 0.0);
            for (double& wi : w) {
                wi /= w_sum; // 归一化样本权重
            }
            learners.push_back(best_learner); // 添加决策树桩到集合
            alphas.push_back(alpha); // 添加权重
        }
    }

    // 预测函数
    vector<int> predict(const vector<vector<double>>& X) {
        int m = X.size();
        vector<double> predictions(m, 0);
        for (int i = 0; i < n_learners; ++i) {
            vector<int> y_pred = learners[i].predict(X);
            for (int j = 0; j < m; ++j) {
                predictions[j] += alphas[i] * y_pred[j];
            }
        }
        vector<int> y_sign(m);
        transform(predictions.begin(), predictions.end(), y_sign.begin(),
                  [](double x) { return (x >= 0) ? 1 : -1; }); // 预测结果正负判断
        return y_sign;
    }
};

// 计算准确率
double accuracy_score(const vector<int>& y_true, const vector<int>& y_pred) {
    int correct = 0;
    for (size_t i = 0; i < y_true.size(); ++i) {
        if (y_true[i] == y_pred[i]) {
            ++correct;
        }
    }
    return static_cast<double>(correct) / y_true.size();
}

int main() {
    vector<vector<double>> X = {{1, 2},
                                 {2, 3},
                                 {3, 4},
                                 {4, 5},
                                 {5, 6}};
    vector<int> y = {1, 1, -1, -1, -1};

    Adaboost adaboost(10); // 创建Adaboost分类器，决策树桩数量为10
    adaboost.fit(X, y); // 拟合数据
    vector<int> y_pred = adaboost.predict(X); // 预测
    double accuracy = accuracy_score(y, y_pred); // 计算准确率
    cout << "Adaboost accuracy: " << accuracy << endl;

    return 0;
}