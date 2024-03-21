# pylint: disable=[W,R,C]

import pywinctl as gw
import pyautogui
from screeninfo import get_monitors
import platform

if platform.system() == "Darwin":
    from Quartz import CoreGraphics # pylint: disable=import-error # type: ignore

    def macOSsetWindow(window_name:str, x:int, y:int, width:int, height:int):
        # Get the frontmost window
        frontmost_window = CoreGraphics.CGWindowListCopyWindowInfo(CoreGraphics.kCGWindowListOptionOnScreenOnly, CoreGraphics.kCGNullWindowID)
        frontmost_window = frontmost_window[0]

        # Get the window ID
        window_id = frontmost_window[CoreGraphics.kCGWindowNumber]

        # Move and resize the window
        CoreGraphics.CGWindowMove(window_id, (x, y))
        CoreGraphics.CGWindowResize(window_id, (width, height))

    def macOSgetWindowPos(window_name:str):
        # Get the frontmost window
        frontmost_window = CoreGraphics.CGWindowListCopyWindowInfo(CoreGraphics.kCGWindowListOptionOnScreenOnly, CoreGraphics.kCGNullWindowID)
        frontmost_window = frontmost_window[0]

        # Get the window ID
        window_id = frontmost_window[CoreGraphics.kCGWindowNumber]

        window_info_list = CoreGraphics.CGWindowListCopyWindowInfo(CoreGraphics.kCGWindowListOptionIncludingWindow, window_id)
    
        if window_info_list:
            window_info = window_info_list[0]
            bounds = window_info[CoreGraphics.kCGWindowBounds]
            success, egg = CoreGraphics.CGRectMakeWithDictionaryRepresentation(bounds, None)
            # return {egg.origin.x, egg.origin.y if success else None}
            if success:
                return egg.origin.x, egg.origin.y
            return None
            #
            # x, y = bounds[CoreGraphics.kCGWindowBoundsX], bounds[CoreGraphics.kCGWindowBoundsY]
            # return x, y
        else:
            return None

    def macOSfocusWindow(window_name:str):
        ...

else:
    macOSfocusWindow = macOSgetWindowPos = macOSsetWindow = None
