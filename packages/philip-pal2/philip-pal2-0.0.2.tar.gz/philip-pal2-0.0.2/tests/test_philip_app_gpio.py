"""
Tests for the extended PHiLIP interface
"""
from time import sleep

_SLEEP_TIME = 0.3

GPIO_NAME_LIST = [
    {"tmr": ["dut_ic"]},
    {"adc": ["dut_adc"]},
    {"i2c": ["dut_sda", "dut_scl"]},
    {"pwm": ["dut_pwm"]},
    {"dac": ["dut_dac"]},
    {"spi": ["dut_mosi", "dut_miso", "dut_sck", "dut_nss"]},
    {"uart": ["dut_rx", "dut_tx", "dut_cts", "dut_rts"]},
]


def test_all_gpio_input_hi(phil_ex):
    for gpio in GPIO_NAME_LIST:
        k, pins = next(iter(gpio.items()))
        res = phil_ex.commit_write("{}.mode.disable".format(k), 1)
        for pin in pins:
            res = phil_ex.commit_write("{}.{}.pull".format(k, pin), 1)
            sleep(_SLEEP_TIME)
            res = phil_ex.read_reg("{}.{}.level".format(k, pin))
            assert res == 1, "{}.{}.level failed to be pulled up".format(k, pin)


def test_all_gpio_input_lo(phil_ex):
    for gpio in GPIO_NAME_LIST:
        k, pins = next(iter(gpio.items()))
        res = phil_ex.commit_write("{}.mode.disable".format(k), 1)
        for pin in pins:
            res = phil_ex.commit_write("{}.{}.pull".format(k, pin), 2)
            sleep(_SLEEP_TIME)
            res = phil_ex.read_reg("{}.{}.level".format(k, pin))
            assert res == 0, "{}.{}.level failed to be pulled down".format(k, pin)


def test_all_gpio_output_hi(phil_ex):
    for gpio in GPIO_NAME_LIST:
        k, pins = next(iter(gpio.items()))
        res = phil_ex.commit_write("{}.mode.disable".format(k), 1)
        for pin in pins:
            res = phil_ex.commit_write("{}.{}.io_type".format(k, pin), 1)
            res = phil_ex.commit_write("{}.{}.set_level".format(k, pin), 1)
            sleep(_SLEEP_TIME)
            res = phil_ex.read_reg("{}.{}.level".format(k, pin))
            assert res == 1, "{}.{}.level failed to be pulled down".format(k, pin)


def test_all_gpio_output_lo(phil_ex):
    for gpio in GPIO_NAME_LIST:
        k, pins = next(iter(gpio.items()))
        res = phil_ex.commit_write("{}.mode.disable".format(k), 1)
        for pin in pins:
            res = phil_ex.commit_write("{}.{}.io_type".format(k, pin), 1)
            res = phil_ex.commit_write("{}.{}.set_level".format(k, pin), 0)
            sleep(_SLEEP_TIME)
            res = phil_ex.read_reg("{}.{}.level".format(k, pin))
            assert res == 0, "{}.{}.level failed to be pulled down".format(k, pin)
