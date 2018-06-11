import numpy as np
import matplotlib.pyplot as plt

r = 125+20
d0 = np.array([0,2.25,5,10,15.75,20.75,-10.25,-5.25])
d = d0*4 # to mm
a = np.arctan2(d,r)
pwm = np.array([1500, 1550, 1600, 1700, 1805, 1904, 1308, 1404])
A = np.vstack([pwm, np.ones(len(pwm))]).T
m, c = np.linalg.lstsq(A, a)[0]

print('rudder')
print('m={} c={}'.format(m, c))

plt.plot(pwm, a, 'o', label='measurements', markersize=10)
x = np.linspace(1000, 2000)
y = c + m*x
plt.plot(x, c + m*x, label='linar fit')
plt.legend()
plt.show()

# right flap
a = np.pi / 180 * np.array([-13.8, -1.2, 9.2, 16.8, 4.4, -16.8, -9.6, -15.0, -5.6, -2.3, -0.5, 5.6]) # [rad]
pwm = np.array([1151, 1404, 1610, 1752, 1498, 1074, 1245, 1105, 1309, 1392, 1424, 1533])
A = np.vstack([pwm, np.ones(len(pwm))]).T
m, c = np.linalg.lstsq(A, a)[0]

print('right flap')
print('m={} c={}'.format(m, c))

plt.plot(pwm, a, 'o', label='measurements', markersize=10)
x = np.linspace(1000, 2000)
y = c + m*x
plt.plot(x, c + m*x, label='linar fit')
plt.legend()
plt.show()


# left flap
a = np.pi / 180 * np.array([20.1, 17.1, 15.4, 12.5, 9.1, 7.2, 6.3, 2.9, 1.6, -3.4, -5.5, -8.7, -11.4, -15.6]) # [rad]
pwm = np.array([1199, 1273, 1291, 1362, 1417, 1448, 1463, 1523, 1547, 1626, 1666, 1725, 1774, 1852])
A = np.vstack([pwm, np.ones(len(pwm))]).T
m, c = np.linalg.lstsq(A, a)[0]

print('left flap')
print('m={} c={}'.format(m, c))

plt.plot(pwm, a, 'o', label='measurements', markersize=10)
x = np.linspace(1000, 2000)
y = c + m*x
plt.plot(x, c + m*x, label='linar fit')
plt.legend()
plt.show()

