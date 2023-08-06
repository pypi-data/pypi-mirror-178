### Grab screenshots from ADB's screencap and process them right away

```python
pip install adb-screencap-streaming


from adb_screencap_streaming import ADBScreenshot
import cv2
bilder = ADBScreenshot(
    "C:\\Users\\Gamer\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe",
    "localhost:5735",
    show_capture_keys="ctrl+alt+z", # starts cv2.imshow() - can be enabled/disabled by pressing ctrl+alt+z
    show_fps_keys="ctrl+alt+f", # show the fps rate - can be enabled/disabled by pressing ctrl+alt+f
    kill_screencap_keys="ctrl+alt+x", # kills the capture process
)
for ka in bilder.get_adb_screenshots(
    sleeptime=None,
    resize_width=None,
    resize_height=None,
    resize_percent=None,
    interpolation=cv2.INTER_AREA,
):
    print('Do some stuff here', end='\r')
    break #if you break out of the loop, stop capturing 
    
bilder.kill_screencap()

```

