from zmsavings_new.data.model import ProgressiveTotal


class TestProgressiveTotal():
    def test_transactions_and_pt_points_initialized_by_list_by_default(self):
        pt = ProgressiveTotal('goal name')

        assert pt.transactions == []
        assert pt.progressive_total_points == []
