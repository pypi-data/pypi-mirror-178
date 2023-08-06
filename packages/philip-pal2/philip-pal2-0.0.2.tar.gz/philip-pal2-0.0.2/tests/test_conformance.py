import pytest
from mm_pal.conformance_test import BaseConformanceSuite


class TestMockIf(BaseConformanceSuite):
    @pytest.fixture
    def target(self, phil_ex):
        self.resolved_write_permission = 3
        return phil_ex
