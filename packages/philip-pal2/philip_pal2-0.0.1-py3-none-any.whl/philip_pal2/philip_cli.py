#! /usr/bin/env python3
# Copyright (c) 2022 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT

"""Interface for PHiLIP."""
import argparse
import logging
import statistics as sta
from datetime import datetime
from time import sleep

from cmd2 import with_argparser
from mm_pal import MmCmd, serial_connect_wizard
from tabulate import tabulate

from philip_pal2.philip_if import Philip


class PhilipCli(MmCmd):
    """Command loop for the PHILIP interface."""

    prompt = "PHILIP: "

    def __init__(self, **kwargs):
        """Instantiate cmd based MmCmd class.

        Args:
            port - Serial port for the PHILIP, if None connection wizard tries to
                connect.
            dev_driver (obj): The device driver that contains the map info.
            driver (obj): The communication driver eg. SerialDriver object.
            persistent_history_file (str): Path to history file,
                defaults to ~/.philip_history.
            transcript_files: Files to run transcript tests.

        Note:
            For args and kwargs, check ``MmCmd`` and ``cmd2.Cmd`` for
                clarification.
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        hist = "persistent_history_file"
        transf = "transcript_files"
        cmd_kwargs = {
            hist: kwargs.pop(hist, "~/.philip2_history"),
            transf: kwargs.pop(transf, None),
        }

        self.logger.debug("__init__(%r, %r)", kwargs, cmd_kwargs)
        port = kwargs.get("port", None)

        if "dev_driver" in kwargs:
            super().__init__(kwargs["dev_driver"], **cmd_kwargs)
        elif port or "driver" in kwargs:
            super().__init__(Philip(**kwargs), **cmd_kwargs)
        else:
            super().__init__(serial_connect_wizard(Philip, **kwargs), **cmd_kwargs)

        self.hidden_commands.append("py")

    log_struct_parser = argparse.ArgumentParser()
    log_struct_parser.add_argument(
        "struct",
        choices_provider=MmCmd.regs_choices_method,
        help="name of the structure to read",
    )
    log_struct_parser.add_argument(
        "--interval", "-i", type=float, default=1, help="the rate to log structure"
    )
    log_struct_parser.add_argument(
        "--delimiter",
        "-d",
        type=str,
        default="\n",
        help="number of elements to read in array",
    )
    log_struct_parser.add_argument(
        "--amount",
        "-a",
        type=int,
        default=-1,
        help="amount of samples, -1 = continuous",
    )
    log_struct_parser.add_argument(
        "--csv-style",
        "-c",
        action="store_true",
        default=False,
        help="Outputs header then only data",
    )
    log_struct_parser.add_argument(
        "--timestamp",
        "-t",
        action="store_true",
        default=False,
        help="include timestamp",
    )

    @with_argparser(log_struct_parser)
    def do_log_struct(self, opts):
        """Log at structure at an interval."""
        try:
            amount = opts.amount
            while amount != 0:
                now = datetime.now()
                resps = self.dev_driver.read_struct(opts.struct)
                if opts.timestamp:
                    resps.insert(0, {"timestamp": now})
                if opts.amount == amount and opts.csv_style:
                    self._log_resps_header(resps, delimiter=opts.delimiter)
                self._log_resps(
                    resps, delimiter=opts.delimiter, csv_style=opts.csv_style
                )
                amount -= 1
                time_diff = min((datetime.now() - now).total_seconds(), 0)
                sleep(float(opts.interval) - time_diff)
        except KeyboardInterrupt:
            self.poutput("\nStopped logging")

    log_regs_parser = argparse.ArgumentParser()
    log_regs_parser.add_argument(
        "regs",
        nargs="+",
        choices_provider=MmCmd.regs_choices_method,
        help="name of the structure to read",
    )
    log_regs_parser.add_argument(
        "--interval", "-i", type=float, default=1, help="the rate to log structure"
    )
    log_regs_parser.add_argument(
        "--delimiter",
        "-d",
        type=str,
        default="\n",
        help="number of elements to read in array",
    )
    log_regs_parser.add_argument(
        "--amount",
        "-a",
        type=int,
        default=-1,
        help="amount of samples, -1 = continuous",
    )
    log_regs_parser.add_argument(
        "--csv-style",
        "-c",
        action="store_true",
        default=False,
        help="Outputs header then only data",
    )
    log_regs_parser.add_argument(
        "--timestamp",
        "-t",
        action="store_true",
        default=False,
        help="include timestamp",
    )

    @with_argparser(log_regs_parser)
    def do_log_regs(self, opts):
        """Log at structure at an interval."""
        try:
            amount = opts.amount
            while amount != 0:
                now = datetime.now()
                resps = []
                for reg in opts.regs:
                    resps.append({reg: self.dev_driver.read_reg(reg)})
                if opts.timestamp:
                    resps.insert(0, {"timestamp": now})
                if opts.amount == amount and opts.csv_style:
                    self._log_resps_header(resps, delimiter=opts.delimiter)
                self._log_resps(
                    resps, delimiter=opts.delimiter, csv_style=opts.csv_style
                )
                amount -= 1
                time_diff = min((datetime.now() - now).total_seconds(), 0)
                sleep(float(opts.interval) - time_diff)
        except KeyboardInterrupt:
            self.poutput("\nStopped logging")

    def do_read_trace(self, arg):
        """Read event trace from the dut.

        Usage:
            read_trace
        """
        results = self.dev_driver.read_trace()

        if len(results) == 0:
            return
        headers = ["time", "diff", "source_diff", "source", "event"]
        table_data = []
        diffs = []
        for event in results:
            row_data = []
            for key_name in headers:
                if key_name == "diff":
                    diffs.append(event[key_name])
                row_data.append(event[key_name])
            table_data.append(row_data)
        self.poutput(tabulate(table_data, headers=headers, floatfmt=".9f"))

        try:
            if len(diffs) > 1:
                diffs = diffs[1:]
                self.poutput("\nDifference Stats")
                self.poutput("     min: {:.9f}".format(min(diffs)))
                self.poutput("     max: {:.9f}".format(max(diffs)))
                self.poutput("    mean: {:.9f}".format(sta.mean(diffs)))
                self.poutput("  median: {:.9f}".format(sta.median(diffs)))
                self.poutput("   stdev: {:.9f}".format(sta.stdev(diffs)))
                self.poutput("variance: {:.9f}".format(sta.variance(diffs)))
        except ValueError:
            pass

    def do_show_pinout(self, arg):
        """Prints the pinout for the connected board

        Usage:
            show_pinout
        """
        if arg:
            showboard = int(arg)
        else:
            showboard = self.dev_driver.read_reg("sys.status.board")
        show_pinout(showboard)

    def do_dut_reset(self, arg):
        """Provides a reset to the dut

        Toggles the dut reset pin for the reset time.

        Usage:
            dut_reset
        """
        self.dev_driver.dut_reset()


def show_pinout(showboard):
    """Prints the pinout for the connected board

    Usage:
        show_pinout
    """
    if showboard == 1:
        print(
            """
PHILIP-B -> BLUEPILL

                    ____
                 ___|__|___
 DUT_RST = B12 - |        | - GND
 DUT_CTS = B13 - |        | - GND
 DUT_RTS = B14 - |        | - 3V3
USER_BTN = B15 - |        | - NRST
   DUT_IC = A8 - |        | - B11 = DUT_RX
    IF_TX = A9 - |        | - B10 = DUT_TX
   IF_RX = A10 - |        | - B1 = PM_V_ADC
  USB_DM = A11 - |        | - B0 = PM_HI_ADC
  USB_DP = A12 - |        | - A7 = PM_LO_ADC
 DUT_NSS = A15 - |        | - A6 = DUT_ADC
  DUT_SCK = B3 - |        | - A5 = TEST_FAIL
 DUT_MISO = B4 - |        | - A4 = TEST_WARN
 DUT_MOSI = B5 - |        | - A3 = TEST_PASS
  DUT_SCL = B6 - |        | - A2 = DEBUG2
  DUT_SDA = B7 - |        | - A1 = DEBUG1
  DUT_PWM = B8 - |        | - A0 = DEBUG0
  DUT_DAC = B9 - |        | - C15
            5V - |        | - C14
           GND - |        | - C13 = LED0
           3V3 - |        | - VBAT
                 __________
                    ||||
"""
        )
    else:
        print(
            """
PHILIP-N -> NUCLEO-F103RB
CN6

                            DUT_SCL = PB8 = SCL/D15 -
                            DUT_SDA = PB9 = SDA/D14 -
                                               AVDD -
                                                GND -
-                              LED0 = PA5 = SCK/D13 -
- IOREF                                    MISO/D12 -
- NRST                                 PWM/MOSI/D11 -
- 3V3                                    PWM/CS/D10 -
- 5V                                         PWM/D9 -
- GND                             DUT_TX = PA9 = D8 -
- GND                                           |CN5|
- VIN                             DUT_IC = PA8 = D7 -
|CN6|                                        PWM/D6 -
- A0 = PA0 = TEST_WARN      DUT_MISO = PB4 = PWM/D5 -
- A1 = PA1 = TEST_FAIL          DUT_MOSI = PB5 = D4 -
- A2 = PA4 = TEST_PASS       DUT_SCK = PB3 = PWM/D3 -
- A3 = PB0 = DUT_ADC             DUT_RX = PA10 = D2 -
- A4 = PC1 = PM_HI_ADC          IF_TX = PA2 = TX/D1 -
- A5 = PC0 = PM_V_ADC           IF_RX = PA3 = RX/D0 -
|CN8|                                          |CN9|

          -1 -                  DUT_DAC -1 - DUT_PWM
          -2 -                  DUT_SCL -2 -
          -3 -                  DUT_SDA -3 -
          -4 -                          -4 -
          -5 -                          -5 -
          -6 -                     LED0 -6 - DUT_RTS
          -7 -                          -7 - DUT_CTS
          -8 -                          -8 -
  DUT_NSS -9 -                          -9 -
          -10-                          -10-
          -11-                   DUT_TX -11- DUT_RST
 USER_BTN -12-                   DUT_IC -12-
          -13-                          -13- DEBUG2
          -14- TEST_WARN       DUT_MISO -14- DEBUG1
          -15- TEST_FAIL       DUT_MOSI -15- DEBUG0
          -16- TEST_PASS        DUT_SCK -16-
          -17- DUT_ADC           DUT_RX -17-
PM_LO_ADC -18- PM_HI_ADC          IF_TX -18-
          -19- PM_V_ADC           IF_RX -19-
          |CN7|                         |CN10|
"""
        )


def log_level_module_control(pargs):
    """Enable logs depending on modules.

    Args:
        pargs: arguments from argparse
    """
    if pargs.loglevel:
        loglevel = logging.getLevelName(pargs.loglevel.upper())
        if pargs.logmodules is not None:
            logging.basicConfig()
            for logname in pargs.logmodules:
                logger = logging.getLogger(logname)
                logger.setLevel(loglevel)
        else:
            logging.basicConfig(level=loglevel)


def main():
    """Run PhilipCli command loop."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--loglevel", default="INFO", help="Python logger log level, defaults to INFO."
    )
    parser.add_argument(
        "--logmodules", nargs="+", default=None, help="Modules to enable logging."
    )
    parser.add_argument(
        "--port", "-p", default=None, help="Serial device name, defaults to None."
    )
    parser.add_argument(
        "--mm-path", default=None, help="Path to memory map, defaults to None."
    )
    parser.add_argument(
        "--onecmd",
        "-o",
        type=str,
        default=None,
        help="Execute only one command then exit.",
    )
    parser.add_argument(
        "--transcript-files",
        default=None,
        nargs="+",
        help="Transcript files to run automated test.",
    )

    pargs = parser.parse_args()
    log_level_module_control(pargs)
    kwargs = {
        "port": pargs.port,
        "mm_path": pargs.mm_path,
        "transcript_files": pargs.transcript_files,
    }
    if pargs.onecmd:
        PhilipCli(**kwargs).onecmd(pargs.onecmd)
    else:
        PhilipCli(**kwargs).cmdloop()


if __name__ == "__main__":
    main()
