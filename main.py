from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton,MDTextButton
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import TouchBehavior
from kivymd.app import MDApp
from kivymd.uix.behaviors import CircularRippleBehavior, CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from jnius import autoclass, cast

# Load Android classes
Context = autoclass('android.content.Context')
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Activity = autoclass('android.app.Activity')
PackageManager = autoclass('android.content.pm.PackageManager')
CameraManager = autoclass('android.hardware.camera2.CameraManager')
KV = '''
<CircularElevationButton>
    
    
    size_hint: None, None
    size: "230dp", "230dp"
    radius: self.size[0] / 2
    shadow_radius: self.radius[0]
    md_bg_color: "blue"

    MDIcon:
        icon: "flash"
        halign: "center"
        valign: "center"
        pos_hint: {"center_x": .5, "center_y": .5}
        size: root.size
        pos: root.pos
        font_size: root.size[0] * .6
        theme_text_color: "Custom"
        text_color: "white"
<MagicButton@MagicBehavior+CircularElevationButton>

MDScreen:
    md_bg_color:"black"

    MagicButton:
        pos_hint: {"center_x": .5, "center_y": .6}
        elevation: 40
        shadow_softness: 40
        on_release: app.toggle_torch()
        
        on_release: self.twist()
    
        
    
'''
class CircularElevationButton(
    CommonElevationBehavior,
    CircularRippleBehavior,
    ButtonBehavior,
    MDFloatLayout,
    TouchBehavior,
):
    pass

class TorchApp(MDApp):
   
    def build(self):
        return Builder.load_string(KV)

    def toggle_torch(self):
        activity = cast(Activity, PythonActivity.mActivity)
        context = activity.getSystemService(Context.CAMERA_SERVICE)
        camera_manager = cast(CameraManager, context)
        camera_id = camera_manager.getCameraIdList()[0]

        if not hasattr(self, '_torch_on'):
            self._torch_on = False

        self._torch_on = not self._torch_on
        camera_manager.setTorchMode(camera_id, self._torch_on)

    def on_stop(self):
        # Turn off torch if it is still on
        if hasattr(self, '_torch_on') and self._torch_on:
            self.toggle_torch()
        super().on_stop()

   

if __name__ == '__main__':
    TorchApp().run()