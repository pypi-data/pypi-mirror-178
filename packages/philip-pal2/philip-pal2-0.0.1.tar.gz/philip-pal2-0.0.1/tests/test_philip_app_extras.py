"""
Tests for the extended PHiLIP interface
"""


def test_empty_read_trace(phil_ex):
    res = phil_ex.read_trace()
    assert res == [], "read_trace should return an empty list"


def test_extra_funcs_not_crash_when_empty(phil_ex):
    phil_ex.get_spi_clk_deadtime_stats()
    phil_ex.get_spi_clk_frame_stats()
    phil_ex.get_spi_clk_stats()
    phil_ex.dut_reset()
