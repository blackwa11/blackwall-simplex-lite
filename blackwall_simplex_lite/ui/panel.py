from bpy.types import Panel


class UNIVERSAL_PT_4d_panel(Panel):
    bl_label = "4D Transformer Lite"
    bl_idname = "UNIVERSAL_PT_4d_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "4D Transform"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.universal_4d_settings

        box = layout.box()
        box.label(text="Create")
        box.operator("universal.create_simplex", text="Create Simplex", icon='MESH_GRID')

        box = layout.box()
        box.label(text="Playback")
        row = box.row(align=True)
        row.operator("universal.start_all", text="Start", icon='PLAY')
        row.operator("universal.stop_all", text="Stop", icon='PAUSE')
        box.operator("universal.reset_all", text="Reset", icon='LOOP_BACK')

        box = layout.box()
        box.label(text="Settings")
        box.prop(settings, "object_type")
        box.prop(settings, "speed")
        box.prop(settings, "scale")
        box.prop(settings, "w_depth")

        box = layout.box()
        box.label(text="Rotation")
        box.prop(settings, "rotation_xy")
        box.prop(settings, "rotation_xz")
        box.prop(settings, "rotation_xw")
        box.prop(settings, "rotation_yz")
        box.prop(settings, "rotation_yw")
        box.prop(settings, "rotation_zw")
