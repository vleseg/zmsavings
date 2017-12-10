import datetime
# Third-party imports
from mock import patch
from money import Money
import pytest
# Project imports
from zmsavings_new.data.model import ProgressiveTotalPoint
from zmsavings_new.visualizer import Visualizer


@pytest.fixture
def progressive_total():
    rur = lambda amount: Money(amount, currency='RUR')
    nov = lambda day: datetime.date(2017, 11, day)

    return [
        ProgressiveTotalPoint(total=rur(0), date=nov(1)),
        ProgressiveTotalPoint(total=rur(1000), date=nov(2)),
        ProgressiveTotalPoint(total=rur(800), date=nov(3)),
        ProgressiveTotalPoint(total=rur('1150.75'), date=nov(4)),
        ProgressiveTotalPoint(total=rur('1150.75'), date=nov(5)),
        ProgressiveTotalPoint(total=rur('1150.75'), date=nov(6)),
        ProgressiveTotalPoint(total=rur(1340), date=nov(7)),
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
    fixture_obj.mocks = patch(
        'zmsavings_new.visualizer.get_random_file_path',
        return_value=fixture_obj.out_file).start()
    fixture_obj.mocks.print_function = patch(
        'zmsavings_new.visualizer.print_function').start()

    return fixture_obj


class TestVisualizer(object):
    def test_basic_functionality(self, fixture):
        v = Visualizer("test_goal", fixture.progressive_total)
        v.generate()

        assert fixture.mocks.print_function.assert_called_once_with(
            'Visualization generated successfully. Saved to {0}'.format(
                fixture.out_file + '.png'))
