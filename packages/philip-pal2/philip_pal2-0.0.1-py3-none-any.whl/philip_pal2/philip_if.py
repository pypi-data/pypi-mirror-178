# Copyright (c) 2019 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Interface for PHILIP in philip_pal.

This handles the basic protocol interface to PHILIP and extended helpers for
PHILIP.
"""
import logging
from pathlib import Path
from statistics import mean, stdev
from time import sleep

from mm_pal import MmIf, import_mm_from_csv


class Philip(MmIf):
    """Interface to a philip memory map.

    Attributes:
        parser (obj): The type of parser to use, defaults to MmJsonParser.
        mem_map (dict): Register memory mapping information.
        if_version (str): Interface version of connected device.
    """

    def __init__(self, *args, **kwargs):
        """Initialize driver and parser to interface to memory map device.

        If a mem_map is not provided, check version and and match the memory
        map provided by the package.

        Args:
            default_retry (int): The default amount of times a command retries
                until an exception is raised, defaults to 1.
            frag_size (int): Number of registers until fragmented packet, based
                on device buffer size, defaults to 128
            toggle_rst_boot (bool): Try toggling all combinations of rts and
                boot pins when connecting, defaults to true

        Note:
            For args and kwargs, check ``MmIf`` for clarification.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        kwargs["default_retry"] = kwargs.pop("default_retry", 1)
        kwargs["frag_size"] = kwargs.pop("frag_size", 128)
        super().__init__(*args, **kwargs)
        self.if_version = self.get_version(timeout=0.2)
        self._sys_clock = None

        self.logger.info("Interface version: %r", self.if_version)
        version_str = self.if_version.replace(".", "_")
        rel_path = f"/mem_map/mm_PHiLIP_philip_map_{version_str}.csv"
        version_path = str(Path(__file__).parents[0]) + rel_path
        self.mem_map = import_mm_from_csv(version_path)

    def read_trace(self, to_ns=False):
        """Reads event trace from the dut

        Returns:
            see send_and_parse_cmd()
            formatted to return the time sorted events
        """
        trace = []
        self._get_trace_events(trace, to_ns)

        sorted_events = sorted(trace, key=lambda x: x["time"])
        any_diff = 0
        ev_diff = {"DEBUG0": 0, "DEBUG1": 0, "DEBUG2": 0, "DUT_IC": 0}

        for event in sorted_events:
            event["diff"] = 0
            event["source_diff"] = 0
            if any_diff != 0:
                event["diff"] = event["time"] - any_diff
            if ev_diff[event["source"]] != 0:
                event["source_diff"] = event["time"] - ev_diff[event["source"]]
            ev_diff[event["source"]] = event["time"]
            any_diff = event["time"]

        response = sorted(trace, key=lambda x: x["time"])
        return response

    def _get_trace_events(self, trace, to_ns):
        self.logger.debug("_get_trace_events(trace=?, to_ns=%r)", to_ns)
        # should be time in seconds
        trace_tick_divs = self.read_reg("trace.tick_div")
        trace_sources = self.read_reg("trace.source")
        trace_ticks = self.read_reg("trace.tick")
        trace_values = self.read_reg("trace.value")
        for _ in range(len(trace_ticks)):
            trace_event = {}
            trace_tick_div = trace_tick_divs[_]
            trace_source = trace_sources[_]
            trace_tick = trace_ticks[_]
            trace_value = trace_values[_]
            total_tick = trace_tick << trace_tick_div
            time_sec = float(total_tick) / self.sys_clk()
            if to_ns:
                trace_event["time"] = int(time_sec * 10000000000)
            else:
                trace_event["time"] = round(time_sec, 9)
            if trace_source == 1:
                trace_event["source"] = "DEBUG0"
            elif trace_source == 2:
                trace_event["source"] = "DEBUG1"
            elif trace_source == 3:
                trace_event["source"] = "DEBUG2"
            elif trace_source == 4:
                trace_event["source"] = "DUT_IC"
            else:
                trace_event["source"] = trace_source

            if trace_value == 0:
                trace_event["event"] = "FALLING"
            elif trace_value == 1:
                trace_event["event"] = "RISING"
            else:
                trace_event["event"] = trace_value
            if trace_source != 0:
                trace.append(trace_event)

    def _get_stats(self, vals: list):
        """Calculate stats of a list of values.

        Args:
            vals: The values to run stats on.

        Returns:
            dict containing stats.
        """
        if len(vals) == 0:
            return {}
        if len(vals) == 1:
            return {
                "values": vals,
                "num_values": len(vals),
                "mean": vals[0],
                "min": vals[0],
                "max": vals[0],
                "e_minus": 0,
                "e_plus": 0,
                "stdev": 0,
            }
        return {
            "values": vals,
            "num_values": len(vals),
            "mean": mean(vals),
            "min": min(vals),
            "max": max(vals),
            "e_minus": mean(vals) - min(vals),
            "e_plus": max(vals) - mean(vals),
            "stdev": stdev(vals),
        }

    def get_spi_transfer_count(self) -> int:
        """Get the amount of captured transfers."""
        return self.read_reg("spi.transfer_count")

    def get_spi_clk_frames(self) -> int:
        """Get the amount of bytes in the spi clk buffer."""
        return int(self.get_spi_transfer_count() / 8)

    def sys_clk(self) -> int:
        """Get PHiLIP system clock frequency."""
        if not self._sys_clock:
            self._sys_clock = self.read_reg("sys.sys_clk")
        return self._sys_clock

    def get_spi_clk_freqs(self) -> list:
        """Calculate frequency of captured timestamps.
        Returns:
            List of frequencies
        """
        sm_buf = self.get_spi_sm_buf()
        timer_max = 0x10000
        pulses_per_byte = 8
        freqs = []
        for idx in range(1, len(sm_buf)):
            if (idx) % pulses_per_byte == 0:
                # filter deadtimes
                continue
            dif_ticks = sm_buf[idx] - sm_buf[idx - 1]
            if dif_ticks < 0:
                dif_ticks += timer_max
            if dif_ticks == 0:
                freqs.append(0)
            else:
                freqs.append(self.sys_clk() / dif_ticks)
        return freqs

    def get_spi_clk_stats(self) -> list:
        """Get stats of captured frequencies."""
        return self._get_stats(self.get_spi_clk_freqs())

    def get_spi_sm_buf(self):
        """Get buffer of captured timestamps."""
        return self.read_reg("spi.sm_buf", size=self.get_spi_transfer_count())

    def get_spi_clk_byte_stats(self, byte=None) -> dict:
        """Get stats for each clock pulse of the spi clk.
        Args:
            byte (int, None): The byte in the 8 bit calculation to use, if None
                then use all bytes. Starting with index 0.
        Return:
            dict containing stats.
        """
        num_bytes = self.get_spi_clk_frames()
        bit_freqs = self.get_spi_clk_freqs()
        if byte is not None:
            assert byte < num_bytes
            freqs_per_byte = 7
            start = byte * freqs_per_byte
            end = start + freqs_per_byte
            bit_freqs = bit_freqs[start:end]
        return self._get_stats(bit_freqs)

    def get_spi_clk_frame_stats(self) -> dict:
        """Get stats for byte in the spi frame.
        Return:
            dict containing stats.
        """
        byte_freqs = []
        for byte in range(self.get_spi_clk_frames()):
            byte_freqs.append(self.get_spi_clk_byte_stats(byte)["mean"])
        return self._get_stats(byte_freqs)

    def get_spi_clk_deadtime_stats(self) -> dict:
        """Get stats for the time between spi bytes.
        Return:
            dict containing stats.
        """
        sm_buf = self.get_spi_sm_buf()
        timer_max = 0x10000
        pulses_per_byte = 8
        deadtimes = []
        for i in range(self.get_spi_clk_frames() - 1):
            offset = i * pulses_per_byte + pulses_per_byte
            deadtime_begin = offset - 1
            deadtime_end = offset
            deadtime = sm_buf[deadtime_end] - sm_buf[deadtime_begin]
            if deadtime < 0:
                deadtime += timer_max
            deadtimes.append(deadtime)
        return self._get_stats(deadtimes)

    def dut_reset(self, reset_time=0.3, timeout=None):
        """Provides a reset to the dut

        Toggles the dut reset pin for the reset time.

        Args:
            reset_time: The duration the dut is put in reset
            timeout: Optional timeout value for command specific timeouts
        Returns:
            see send_and_parse_cmd()
        """
        reset_time = float(reset_time)
        self.commit_write("sys.mode.dut_rst", 1, timeout=timeout)
        sleep(reset_time)
        self.commit_write("sys.mode.dut_rst", 0, timeout=timeout)

    def commit_write(self, reg, data, offset=0, verify=False, timeout=None, retry=None):
        """Write and commit in one step.

        This may need to be overridden if commit involves more complicated
        checks.

        Args:
            cmd_name (str): The name of the register to write.
            data (list, int, str): The data to write to the register.
            verify (bool): Verify the register has changed, defaults to False
            offset (int): The number of elements to offset in an array,
                defaults to 0.
            timeout (float): Optional override driver timeout for command,
                defaults to None.
            retry (int): Optional override retry count, defaults to None.

        Exceptions:
            IOError: Errno based error from device
            TimeoutError: Device did not respond
            ValueError: Argument incorrect
            TypeError: Data type not correct
        """
        mode_init = reg.split(".")[0] + ".mode.init"
        if mode_init in self.mem_map:
            self.write_reg(mode_init, 0, verify=verify, timeout=timeout, retry=retry)
        return super().commit_write(
            reg, data, offset=offset, verify=verify, timeout=timeout, retry=retry
        )
