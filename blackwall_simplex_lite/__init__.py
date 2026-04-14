bl_info = {
    "name": "Simplex Lite",
    "author": "blackwa11 / Blackwall",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > 4D Transform",
    "description": "Lite Blender addon for real-time simplex projection and 4D rotation",
    "category": "Object",
}

import bpy
from bpy.props import PointerProperty

from .properties import Universal4DSettings
from .operators.create import UNIVERSAL_OT_create_simplex
from .operators.playback import (
    UNIVERSAL_OT_start_all,
    UNIVERSAL_OT_stop_all,
    UNIVERSAL_OT_reset_all,
)
from .ui.panel import UNIVERSAL_PT_4d_panel
from .core.state import object_4d_data
from .core.transform import animation_update

classes = [
    Universal4DSettings,
    UNIVERSAL_OT_create_simplex,
    UNIVERSAL_OT_start_all,
    UNIVERSAL_OT_stop_all,
    UNIVERSAL_OT_reset_all,
    UNIVERSAL_PT_4d_panel,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.universal_4d_settings = PointerProperty(type=Universal4DSettings)


def unregister():
    if bpy.app.timers.is_registered(animation_update):
        try:
            bpy.app.timers.unregister(animation_update)
        except Exception:
            pass

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    try:
        del bpy.types.Scene.universal_4d_settings
    except Exception:
        pass

    object_4d_data.clear()


if __name__ == "__main__":
    register()
