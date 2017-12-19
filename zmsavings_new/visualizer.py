from __future__ import print_function
# Third-party imports
import matplotlib.pyplot as plt
# Project imports
from utils.fs import get_random_file_path


class Visualizer(object):
    def __init__(self, goal, progressive_total):
        self.goal = goal
        self.progressive_total = progressive_total

    def generate(self):
        out_file = get_random_file_path() + '.png'

        data = zip(*(
            (ptp.date, ptp.total.amount) for ptp in self.progressive_total))

        plt.plot_date(*data, xdate=True)
        plt.title(self.goal)
        plt.savefig(out_file)

        print_function('Visualization generated successfully. Saved to {0}'
                       .format(out_file))
