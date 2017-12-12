import datetime
import os
# Third-party imports
from mock import Mock, patch
from money import Money
import pytest
# Project imports
from zmsavings_new.data.model import ProgressiveTotalPoint
from zmsavings_new.visualizer import Visualizer

RUR = lambda amount: Money(amount, currency='RUR')
NOV = lambda day: datetime.date(2017, 11, day)


@pytest.fixture
def progressive_total():

    return [
        ProgressiveTotalPoint(total=RUR(0), date=NOV(1)),
        ProgressiveTotalPoint(total=RUR(1000), date=NOV(2)),
        ProgressiveTotalPoint(total=RUR(800), date=NOV(3)),
        ProgressiveTotalPoint(total=RUR('1150.75'), date=NOV(4)),
        ProgressiveTotalPoint(total=RUR('1150.75'), date=NOV(5)),
        ProgressiveTotalPoint(total=RUR('1150.75'), date=NOV(6)),
        ProgressiveTotalPoint(total=RUR(1340), date=NOV(7)),
    ]


@pytest.fixture
def fixture(progressive_total, tmpdir):
    class Fixture(object):
        pass

    class Mocks(object):
        pass

    fixture_obj = Fixture()
    fixture_obj.progressive_total = progressive_total
    fixture_obj.out_file = str(tmpdir.mkdir('plot_out').join("out"))

    fixture_obj.mocks = Mocks()
    fixture_obj.mocks.get_random_file_path = patch(
        'zmsavings_new.visualizer.get_random_file_path').start()
    fixture_obj.mocks.get_random_file_path.return_value = fixture_obj.out_file
    fixture_obj.mocks.print_function = patch(
        'zmsavings_new.visualizer.print_function').start()

    return fixture_obj


class TestVisualizer(object):
    @pytest.skip
    def test_basic_functionality(self, fixture):
        v = Visualizer('test_goal', fixture.progressive_total)
        v.generate()

        os.path.isfile(fixture.out_File)

    @patch('zmsavings_new.visualizer.plt.plot')
    def test_progressive_total_is_split_into_two_lists_to_generate_plot(
            self, mock_plot, fixture):
        v = Visualizer('test_goal', fixture.progressive_total)
        v.generate()

        mock_plot.assert_called_once()
        x_axis, y_axis = mock_plot.call_args[0][0]

        assert x_axis[0] == NOV(1)
        assert x_axis[-1] == NOV(7)
        assert y_axis[0] == RUR(0)
        assert y_axis[-1] == RUR(1340)

    @patch('zmsavings_new.visualizer.plt.plot')
    def test_reports_success(self, _, fixture):
        v = Visualizer('test_goal', fixture.progressive_total)
        v.generate()

        fixture.mocks.print_function.assert_called_once_with(
            'Visualization generated successfully. Saved to {0}'.format(
                fixture.out_file + '.png'))
