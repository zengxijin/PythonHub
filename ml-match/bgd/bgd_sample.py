# -*- coding: utf-8 -*-
"""
这是一个梯度下降算法来求参数的一个线性回归的例子
"""
'''
模型假设
'''
# 假设f(x1,x2;θ)= x1*θ1 + x2*θ2
# 这是一个多参数的线性回归函数

'''
样本
'''
input_x1x2 = [[1, 3], [3, 6], [3, 4], [5, 6]]
output_y = [11, 24, 18, 28]

'''
超参初始化
'''
# 参数随机初始化
theta_params = [1, 1]

learn_rate = 0.01  # 学习率
expect_err = 0.0001  # 误差
loss = 10  # 一次迭代累加残差和

theta_1_gradient = [0, 0, 0, 0]
theta_2_gradient = [0, 0, 0, 0]

'''
循环控制，控制训练收敛
'''
max_iterations = 10000  # 最大迭代次数
cur_iterations = 0  # 当前迭代次数

while (loss > expect_err and cur_iterations < max_iterations):
    loss = 0
    err_sum_1 = 0
    err_sum_2 = 0

    for i in range(4):
        predict_value = theta_params[0] * input_x1x2[i][0] + theta_params[1] * input_x1x2[i][1]
        theta_1_gradient[i] = (predict_value - output_y[i]) * input_x1x2[i][0]
        theta_2_gradient[i] = (predict_value - output_y[i]) * input_x1x2[i][1]
        err_sum_1 = err_sum_1 + theta_1_gradient[i]
        err_sum_2 = err_sum_2 + theta_2_gradient[i]

    theta_params[0] = theta_params[0] - learn_rate * err_sum_1 / 4
    theta_params[1] = theta_params[1] - learn_rate * err_sum_2 / 4

    for i in range(4):
        predict_value = theta_params[0] * input_x1x2[i][0] + theta_params[1] * input_x1x2[i][1]
        error = 1 / (2 * 4) * (predict_value - output_y[i]) ** 2  # 计算残差平方和
        loss = loss + error

    cur_iterations += 1
    # print("count:", cur_iterations)

print("theta:", theta_params)
print("loss:", loss)
print("count:", cur_iterations)
