from robots import Robot
from robots.links import Link
from robots.joints import Revolute
from matplotlib import pyplot as plt

robi = Robot(
    Revolute(rotation=0),
    Link(5),
    Revolute(rotation=-1),
    Link(3),
    Revolute(rotation=-1),
    Link(3)
)

for i in range(200):
    robi.structure[0].rotation += 0.1
    robi.structure[2].rotation -= 0.1
    robi.show()
    plt.pause(1e-2)
input("Press ENTER to close the visualization")
