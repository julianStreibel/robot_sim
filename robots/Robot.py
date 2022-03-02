import numpy as np
from matplotlib import pyplot as plt
from math import sin, cos

from .links import Link
from .joints import Joint


class Robot():
    def __init__(self, *args, vis=True):
        self.init_structure(args)
        self.base = np.array([0, 0, 1])
        self.max_length = sum(
            [s.length for s in self.structure if type(s) == Link])
        if vis:
            self.init_vis()

    def init_structure(self, parts):
        structure = list(parts)
        for i, part in enumerate(structure):
            if i % 2 == 0:
                assert isinstance(part, Joint), "A robot starts with a joint"
            else:
                assert isinstance(
                    part, Link), "The parts of a robot alternate between joint and link"
        self.structure = structure

    def init_vis(self):
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(
            xlim=(-self.max_length - 1, self.max_length + 1), ylim=(-self.max_length - 1, self.max_length + 1))
        self.robot_plot, = ax.plot([], [], 'o-', lw=1, color='r',
                                   markerfacecolor='w', markersize=3)
        plt.xlabel('x-axis [m]', fontsize=15)
        plt.ylabel('y-axis [m]', fontsize=15)
        plt.draw()

    def get_joints_in_task_space(self):
        q = [self.base]
        transformations = np.identity(3)
        for i in range(len(self.structure) // 2):
            current_transformation = np.identity(3)
            for part in self.structure[i*2: i*2 + 2]:
                new_transformation = np.identity(3)
                if isinstance(part, Link):
                    new_transformation[0, -1] = part.length
                    current_transformation = current_transformation @ new_transformation
                else:
                    new_transformation[0:2, 0:2] = np.array(
                        [[cos(part.rotation), -sin(part.rotation)], [sin(part.rotation), cos(part.rotation)]])
                    current_transformation = current_transformation @ new_transformation
            transformations = transformations @ current_transformation
            q.append(transformations @ q[0])
        q = np.array(q)[:, :-1].T
        self.forward_kinematic_transformation = transformations
        return q

    def get_jacobian(self):
        pass

    def forward_kinematics(self):
        self.get_joints_in_task_space()
        return self.forward_kinematic_transformation @ self.base

    def show(self):
        self.robot_plot.set_data(self.get_joints_in_task_space())
        plt.title(f"x = {self.forward_kinematics()[:-1]}")
