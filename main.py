from robots import Robot
from robots.links import Link
from robots.joints import Revolute
from matplotlib import pyplot as plt
import numpy as np

N = 10

robi = Robot(
    [Revolute() if i % 2 == 0 else Link(1) for i in range(N)]

)

# current sim
rot = [np.random.normal(0, 0.1) for _ in range(N)]
for t in range(200):
    for i in range(N // 2):
        robi.structure[i * 2].rotation += rot[i]
    robi.show()
    plt.pause(1e-2)
input("Press ENTER to close the visualization")
