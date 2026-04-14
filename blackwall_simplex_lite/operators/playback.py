import bpy
from bpy.types import Operator

from ..core.state import object_4d_data
from ..core.transform import ensure_timer_running, reset_object_to_original


class UNIVERSAL_OT_start_all(Operator):
    bl_idname = "universal.start_all"
    bl_label = "Start"
    bl_options = {'REGISTER'}

    def execute(self, context):
        if not object_4d_data:
            self.report({'WARNING'}, "No simplex created")
            return {'CANCELLED'}

        for _, data in object_4d_data.items():
            data["animation_running"] = True

        ensure_timer_running()
        self.report({'INFO'}, "Animation started")
        return {'FINISHED'}


class UNIVERSAL_OT_stop_all(Operator):
    bl_idname = "universal.stop_all"
    bl_label = "Stop"
    bl_options = {'REGISTER'}

    def execute(self, context):
        if not object_4d_data:
            self.report({'WARNING'}, "No active object")
            return {'CANCELLED'}

        for _, data in object_4d_data.items():
            data["animation_running"] = False

        self.report({'INFO'}, "Animation stopped")
        return {'FINISHED'}


class UNIVERSAL_OT_reset_all(Operator):
    bl_idname = "universal.reset_all"
    bl_label = "Reset"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.universal_4d_settings

        for _, data in object_4d_data.items():
            data["animation_running"] = False

        for obj_name in list(object_4d_data.keys()):
            obj = bpy.data.objects.get(obj_name)
            if obj is not None:
                reset_object_to_original(obj, object_4d_data[obj_name], settings.w_depth)

        settings.speed = 1.0
        settings.scale = 1.0
        settings.w_depth = 4.0
        settings.rotation_xy = 0.0
        settings.rotation_xz = 0.0
        settings.rotation_xw = 0.0
        settings.rotation_yz = 0.0
        settings.rotation_yw = 0.0
        settings.rotation_zw = 0.0

        self.report({'INFO'}, "Reset complete")
        return {'FINISHED'}
