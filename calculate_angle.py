import numpy as np


def all_level_angle(R, l, y, r):
    gamma = np.arcsin((R ** 2 + l ** 2 + y ** 2 - r ** 2) / (2 * R * np.sqrt(y ** 2 + l ** 2))) - np.arctan(l / y)
    beta = np.arccos((r ** 2 + R ** 2 - y ** 2 - l ** 2) / (2 * r * R))
    alpha = np.pi + gamma - beta
    return np.degrees(alpha), np.degrees(beta), np.degrees(gamma)


def make_level_angle(now_alpha, now_beta):
    return 180 - now_beta - now_alpha


#
# y = np.linspace(0.001, 2.7, 100)
# alpha, beta, gamma = calculate_angle(2, 1, y, 1)
# print(alpha, beta,gamma)
for y in np.linspace(0.01, 2.7, 100):
    calculate_alpha, calculate_beta, calculate_gamma = all_level_angle(2, 1, y, 1)
    if calculate_alpha < 90 or calculate_alpha < 0:
        break
    print(calculate_alpha, calculate_beta, calculate_gamma)
