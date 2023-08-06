### Grab screenshots from a specific window and process them right away

```python
pip install window-capture-streaming


from window_capture_streaming import WindowIterCapture
import re
import cv2
capt = WindowIterCapture(
    hwnd=None,
    window_text=re.compile(r".*bluestacks.*", flags=re.IGNORECASE),
    show_capture_keys="ctrl+alt+z",  # starts cv2.imshow() - can be enabled/disabled by pressing ctrl+alt+z
    show_fps_keys="ctrl+alt+f",  # show the fps rate - can be enabled/disabled by pressing ctrl+alt+f
    kill_screencap_keys="ctrl+alt+x",  # kills the capture process
)

for screen_shot in capt.get_screenshot(
    sleeptime=None,
    resize_width=None,
    resize_height=None,
    resize_percent=None,
    interpolation=cv2.INTER_AREA,
):
    pass
    # print('do some stuff here')
    break #if you break out of the loop, stop capturing 
capt.kill_screencap()

```

