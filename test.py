import numpy as np
import matplotlib.pyplot as plt

from profilehist import PlotProfileHistogram

x_data = np.linspace(-10, +10, 50)

y_data = x_data * 5.0 + 3.5 + 10.0 * np.random.normal(0, 1.0, size=len(x_data))

plt.scatter(x_data, y_data)
plt.savefig("Original scatter.png")
PlotProfileHistogram(x_data, y_data, output_filepath="Profile Histogram.png")