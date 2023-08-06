import os
import subprocess
from time import time, sleep
import numpy as np
import cv2
import psutil
import keyboard as keyboardx___
from a_cv2_easy_resize import easy_resize_image


class ADBScreenshot:
    def __init__(
        self,
        adb_path: str,
        deviceserial: str,
        show_capture_keys: str = "ctrl+alt+z",
        show_fps_keys: str = "ctrl+alt+f",
        kill_screencap_keys: str = "ctrl+alt+x",
    ):
        self.adb_path = adb_path
        self.deviceserial = deviceserial
        self.show_capture_keys = show_capture_keys
        self.show_capture = False
        keyboardx___.add_hotkey(self.show_capture_keys, self._show_capture_switch)
        self.show_fps_keys = show_fps_keys
        self.show_fps = False
        keyboardx___.add_hotkey(self.show_fps_keys, self._show_fps_keys_switch)
        self.popenpid = None
        self.kill_screencap_keys = kill_screencap_keys
        keyboardx___.add_hotkey(self.kill_screencap_keys, self._kill_screencap)

    def _kill_screencap(self):
        self.show_capture = False
        self.show_fps = False
        sleep(1)
        try:
            cv2.destroyAllWindows()
        except:
            pass
        sleep(1)
        try:
            p = psutil.Process(self.popenpid)
            p.kill()
        except:
            pass

    def _show_capture_switch(self):
        self.show_capture = not self.show_capture

    def _show_fps_keys_switch(self):
        self.show_fps = not self.show_fps

    def _get_adb_screenshots(self, sleeptime=None):
        read, write = os.pipe()
        if sleeptime is None:
            subcommand = (
                b"n=0; while (( n++ < 1000000000 )); do "
                + b"screencap -p\n"
                + b"echo oioioioioioioioi"
                + b"; done"
            )
        else:
            subcommand = (
                b"n=0; while (( n++ < 1000000000 )); do "
                + b"screencap -p\n"
                + b"echo oioioioioioioioi\nsleep "
                + str(sleeptime).encode()
                + b"; done"
            )

        DEVNULL = open(os.devnull, "wb")
        os.write(write, subcommand)

        os.close(write)
        popen = subprocess.Popen(
            f"{self.adb_path} -s {self.deviceserial} shell",
            stdin=read,
            stdout=subprocess.PIPE,
            universal_newlines=False,
            stderr=DEVNULL,
            shell=False,
        )
        self.popenpid = popen.pid
        wholbilist = []
        killit = False
        try:
            for stdout_line in iter(popen.stdout.readline, b""):
                try:
                    try:
                        wholbilist.append(stdout_line.replace(b"\r\n", b"\n"))
                        if (wholbilist[-1][-17:]) == b"oioioioioioioioi\n":
                            wholbilist[-1] = wholbilist[-1][:-17]
                            varaba = b"".join(wholbilist)
                            yield (
                                cv2.imdecode(
                                    np.frombuffer(varaba, np.uint8), cv2.IMREAD_COLOR
                                )
                            )
                            wholbilist = []

                    except Exception as fe:
                        print(fe)
                        pass

                except Exception as Fehler:
                    print(Fehler)
                    continue
                except KeyboardInterrupt:
                    killit = True
                    break
        except Exception:
            pass
        except KeyboardInterrupt:
            killit = True
        if killit:
            try:
                p = psutil.Process(self.popenpid)
                p.kill()
            except:
                pass

    def get_adb_screenshots(
        self,
        sleeptime=None,
        resize_width=None,
        resize_height=None,
        resize_percent=None,
        interpolation=cv2.INTER_AREA,
    ):
        cv2.destroyAllWindows()
        loop_time = time()
        killcvwindow = False
        for babda in iter(self._get_adb_screenshots(sleeptime=sleeptime)):
            babda = easy_resize_image(
                img=babda,
                width=resize_width,
                height=resize_height,
                percent=resize_percent,
                interpolation=interpolation,
            )
            yield babda
            if self.show_fps:
                print("FPS {}            ".format(1 / (time() - loop_time)), end="\r")
            if self.show_capture:
                killcvwindow = True
                cv2.imshow(fr"pic", babda)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
            else:
                if killcvwindow:
                    cv2.destroyAllWindows()
                killcvwindow = False
            loop_time = time()


#
# from capture_adb_screenshot import ADBScreenshot
# bilder = ADBScreenshot(
#     "C:\\Users\\Gamer\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe",
#     "localhost:5735",
#     show_capture_keys="ctrl+alt+z", # cv2.imshow() - can be enabled/disabled by pressing ctrl+alt+z
#     show_fps_keys="ctrl+alt+f", # show the fps rate - can be enabled/disabled by pressing ctrl+alt+f
#     kill_screencap_keys="ctrl+alt+x", # kills the capture process
# )
# for ka in bilder.get_adb_screenshots(
#     sleeptime=None,
#     resize_width=None,
#     resize_height=None,
#     resize_percent=None,
#     interpolation=cv2.INTER_AREA,
# ):
#     print('Do some stuff here', end='\r')
