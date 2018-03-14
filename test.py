import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 400)
y = np.sin(x**2)


f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, sharex=True)
ax1.plot(x, y)
ax1.set_title('Sharing Y axis')
ax2.plot(x, y)
plt.show()