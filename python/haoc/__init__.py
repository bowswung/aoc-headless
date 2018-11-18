"""Headless AoC launch and control."""

import datetime
import logging
import os
import socket
import shutil
import time

import Xlib.display
from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay


WK_PATH = 'age2_x1/WK.exe'
REC_PATH = 'Games/WololoKingdoms/SaveGame'
LOGGER = logging.getLogger(__name__)


class HeadlessAOC():
    """Headless AOC."""

    def __init__(self, aoc_path, input_path, visible=False):
        """Initialize."""
        self._aoc_path = aoc_path
        self._exe_path = os.path.join(aoc_path, WK_PATH)
        self._rec_path = os.path.join(aoc_path, REC_PATH)
        self._visible = visible
        self._filename = os.path.basename(input_path)
        self._setup_rec(input_path)

    def _setup_rec(self, path):
        """Remove any existing MGZ files and copy in the input rec."""
        for rec in os.listdir(self._rec_path):
            if rec.endswith('mgz'):
                os.remove(os.path.join(self._rec_path, rec))
        shutil.copyfile(path, os.path.join(self._rec_path, 'headless.mgz'))

    def _click(self, x, y, wait=None):
        """Click on the UI."""
        import pyautogui
        if wait:
            self._wait_for_pixel(x, y, wait)
        pyautogui.click(x, y)
        LOGGER.debug('clicked at %d, %d', x, y)

    def _wait_for_pixel(self, x, y, color):
        """Wait for a pixel to become a given color."""
        try:
            img = self.display.grab()
        except OSError:
            raise SystemExit
        rgb = None
        try:
            rgb = img.getpixel((x, y))
        except AttributeError:
            pass
        if not rgb or rgb != color:
            time.sleep(0.1)
            self._wait_for_pixel(x, y, color)

    def wait_for_replay_finish(self):
        """Wait for replay to finish."""
        self._wait_for_pixel(241, 222, (255, 255, 255))
        LOGGER.info("replay finished")

    def select_single_player(self):
        """Select single player mode."""
        self._click(370, 80, wait=(157, 172, 184))
        LOGGER.info("selected single player")

    def select_recorded_games(self):
        """Select saved games/recorded games menu option."""
        self._click(520, 430, wait=(215, 209, 176))
        LOGGER.info("selected recorded games")

    def select_launch_game(self):
        """Select 'OK' to play the selected recorded game."""
        self._click(195, 560, wait=(215, 198, 173))
        LOGGER.info("selected launch game")

    def select_speed_up(self, wait=False):
        """Press the speed up button.

        Only wait if the cursor has moved.
        """
        self._click(190, 570, wait=(70, 32, 6) if wait else None)
        LOGGER.info("selected speed up")

    def _build_command(self):
        """Build the command line to run AoC via wine."""
        return ' '.join([
            'wine',
            '"{}"'.format(self._exe_path),
            'NOSTARTUP',
            'NOSOUND',
            'NODXCHECK'
        ])

    def _startup(self):
        """Start up the virtual display and AoC process."""
        self.display = SmartDisplay(visible=self._visible, size=(800,600), color_depth=24)
        self.display.start()

        # import here because it expects to find `DISPLAY`,
        # but won't until `display.start()`.
        import pyautogui
        pyautogui.PAUSE = 0
        pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])

        cmd = self._build_command()
        LOGGER.info("running: %s", cmd)
        self.process = EasyProcess(cmd)
        self.process.start()

    def _teardown(self):
        """Stop the process and virtual display."""
        self.process.stop()
        self.display.stop()

    def play(self):
        """Play a recorded game."""
        self._startup()

        # series of actions to start and "watch" a rec
        self.select_single_player()
        self.select_recorded_games()
        self.select_launch_game()
        self._start_time = datetime.datetime.now()
        self.select_speed_up()
        self.select_speed_up(wait=False)
        self.select_speed_up(wait=False)
        self.wait_for_replay_finish()

        self._teardown()
        self._end_time = datetime.datetime.now()
        self._run_duration = self._end_time - self._start_time
        LOGGER.info("replayed in %s", str(self._run_duration).split('.')[0])

        return {
            'filename': self._filename,
            'analysis_host': socket.gethostname(),
            'run_duration': self._run_duration,
            'start_time': self._start_time,
            'end_time': self._end_time
        }
