from datetime import timedelta
import os
# Third-party imports
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure, output_file, show
# Project imports
from utils import get_user_data_dir


def encircle_for_patch(data):
    x_points = data[0]
    x_points.insert(0, x_points[0]-timedelta(days=1))
    x_points.append(x_points[-1])

    y_points = data[1]
    y_points.insert(0, 0.0)
    y_points.append(0.0)

    return x_points, y_points


def visualize(goal_transactions):
    # Unpack progressive total into sequences of dates (x points) and totals
    # (y points)
    data = map(list, zip(*((
        prog_point.date, float(prog_point.total))
        for prog_point in goal_transactions.progressive_total)))
    x_points, y_points = encircle_for_patch(data)

    # Set up plot
    output_file(os.path.join(get_user_data_dir(), u"zmsavings_{0}.html".format(
        goal_transactions.goal.name)))
    p = figure(title=goal_transactions.goal.name, tools=[], plot_width=1200,
               x_axis_label='Date', x_axis_type='datetime',
               y_axis_label='Total',
               y_range=(0, float(goal_transactions.goal.total)))

    # Tweak y-axis
    p.yaxis.formatter = NumeralTickFormatter(format='0.00')

    # Add chart (glyph)
    p.patch(x_points, y_points, line_width=1, color="orange")

    # Show the results
    show(p)
