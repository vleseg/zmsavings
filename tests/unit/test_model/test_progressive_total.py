from zmsavings_new.data.model import ProgressiveTotal


class TestProgressiveTotal(object):
    def test_progressive_total_points_initialized_by_list_by_default(self):
        pt = ProgressiveTotal('goal name', transactions=[])

        assert pt.progressive_total_points == []
