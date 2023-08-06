from time import time, sleep
import cv2
import win32gui, win32ui, win32con
import numpy as np
import pandas as pd
import re
from typing import Union
import keyboard as keyboardx___
from a_cv2_easy_resize import easy_resize_image


class WindowIterCapture:
    def __init__(
        self,
        hwnd: Union[None, int] = None,
        window_text: Union[None, re.Pattern, str] = None,
        show_capture_keys: str = "ctrl+alt+z",
        show_fps_keys: str = "ctrl+alt+f",
        kill_screencap_keys: str = "ctrl+alt+x",
    ):
        if hwnd is None and window_text is not None:
            hwnd = WindowIterCapture.find_window_with_regex(window_text)
        self.hwnd = hwnd
        self.window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = self.window_rect[2] - self.window_rect[0]
        self.h = self.window_rect[3] - self.window_rect[1]
        self.offset_x = self.window_rect[0]
        self.offset_y = self.window_rect[1]
        self.df = pd.DataFrame()
        self.stop = False

        self.show_capture_keys = show_capture_keys
        self.show_capture = False
        keyboardx___.add_hotkey(self.show_capture_keys, self._show_capture_switch)
        self.show_fps_keys = show_fps_keys
        self.show_fps = False
        keyboardx___.add_hotkey(self.show_fps_keys, self._show_fps_keys_switch)
        self.popenpid = None
        self.kill_screencap_keys = kill_screencap_keys
        keyboardx___.add_hotkey(self.kill_screencap_keys, self.kill_screencap)

    def _show_capture_switch(self):
        self.show_capture = not self.show_capture

    def _show_fps_keys_switch(self):
        self.show_fps = not self.show_fps

    def kill_screencap(self):
        self.show_fps = False
        self.show_capture = False
        sleep(1)
        self.stop = True
        sleep(1)
        cv2.destroyAllWindows()

    def get_window_position(self):
        self.window_rect = win32gui.GetWindowRect(self.hwnd)
        self.offset_x = self.window_rect[0]
        self.offset_y = self.window_rect[1]

    def get_screenshot(
        self,
        sleeptime=None,
        resize_width=None,
        resize_height=None,
        resize_percent=None,
        interpolation=cv2.INTER_AREA,
    ):
        self.stop = False
        cv2.destroyAllWindows()
        loop_time = time()
        killcvwindow = False
        while not self.stop:
            self.get_window_position()
            wDC = win32gui.GetWindowDC(self.hwnd)
            dcObj = win32ui.CreateDCFromHandle(wDC)
            cDC = dcObj.CreateCompatibleDC()
            dataBitMap = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
            cDC.SelectObject(dataBitMap)
            cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0, 0), win32con.SRCCOPY)
            signedIntsArray = dataBitMap.GetBitmapBits(True)
            img = np.frombuffer(signedIntsArray, dtype="uint8")
            img.shape = (self.h, self.w, 4)
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())
            img = np.ascontiguousarray(img)
            img = easy_resize_image(
                img=img,
                width=resize_width,
                height=resize_height,
                percent=resize_percent,
                interpolation=interpolation,
            )
            yield img
            if self.show_fps:
                print("FPS {}            ".format(1 / (time() - loop_time)), end="\r")
            if self.show_capture:
                killcvwindow = True
                cv2.imshow(fr"picture", img)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
            else:
                if killcvwindow:
                    cv2.destroyAllWindows()
                killcvwindow = False
            if sleeptime is not None:
                sleep(sleeptime)
            loop_time = time()

    @staticmethod
    def get_all_hwnds_and_titles():
        dflist = []

        def winEnumHandler(hwnd, ctx):
            nonlocal dflist
            if win32gui.IsWindowVisible(hwnd):
                dflist.append((hwnd, hex(hwnd), win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(winEnumHandler, None)
        return pd.DataFrame.from_records(
            dflist, columns=["aa_hwnd_int", "aa_hwnd_hex", "aa_title"]
        )

    @staticmethod
    def find_window_with_regex(regular_expression):
        df = WindowIterCapture.get_all_hwnds_and_titles()
        print(df)

        windowtitles = df.loc[
            df.aa_title.str.contains(regular_expression, regex=True, na=False)
        ]
        if not windowtitles.empty:
            return windowtitles["aa_hwnd_int"].iloc[0]
        return None


