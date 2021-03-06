import numpy as np
import matplotlib.pyplot as plt

from profilehist import PlotProfileHistogram

x_data = np.linspace(-10, +10, 50)

# generate some linear y_data with a noise term dependent on X
y_data = (x_data * 5.0 + 3.5) + ((abs(x_data / 2.0) + 1.0) * 10.0 * np.random.normal(0, 1.0, size=len(x_data)))

plt.scatter(x_data, y_data)
plt.savefig("Original-scatter.png", bbox_inches='tight')
PlotProfileHistogram(x_data, y_data, output_filepath="Profile-Histogram.png")