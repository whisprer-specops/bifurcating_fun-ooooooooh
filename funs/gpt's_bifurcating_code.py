import numpy as np
import matplotlib.pyplot as plt

def generate_bifurcation_plot(start=2.8, end=4.0, accuracy=0.0001, reps=600, numtoplot=200):
    interval = (start, end)
    lims = np.zeros(reps)
    fig, biax = plt.subplots()
    fig.set_size_inches(16, 9)

    lims[0] = np.random.rand()
    for r in np.arange(interval[0], interval[1], accuracy):
        for i in range(reps - 1):
            lims[i + 1] = r * lims[i] * (1 - lims[i])
        biax.plot([r] * numtoplot, lims[reps - numtoplot:], "b.", markersize=0.02)

    biax.set(xlabel="r", ylabel="x", title="Logistic Map Bifurcation Plot")
    plt.show()

# Example usage:
generate_bifurcation_plot(start=3.5, end=4.0, accuracy=0.0001, reps=1000, numtoplot=300)
