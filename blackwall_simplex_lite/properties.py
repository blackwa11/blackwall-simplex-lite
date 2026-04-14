from bpy.props import EnumProperty, FloatProperty
from bpy.types import PropertyGroup


class Universal4DSettings(PropertyGroup):
    object_type: EnumProperty(
        name="Object Type",
        items=[
            ('MESH', "Mesh", "Create simplex as mesh"),
            ('CURVE', "Curve", "Create simplex as curve"),
        ],
        default='MESH'
    )

    speed: FloatProperty(name="Speed", default=1.0, min=0.0, max=5.0)
    scale: FloatProperty(name="Scale", default=1.0, min=0.1, max=10.0)
    w_depth: FloatProperty(name="4D Depth", default=4.0, min=2.0, max=10.0)

    rotation_xy: FloatProperty(name="XY Rotation", default=0.0, min=0.0, max=2.0)
    rotation_xz: FloatProperty(name="XZ Rotation", default=0.0, min=0.0, max=2.0)
    rotation_xw: FloatProperty(name="XW Rotation", default=0.0, min=0.0, max=2.0)
    rotation_yz: FloatProperty(name="YZ Rotation", default=0.0, min=0.0, max=2.0)
    rotation_yw: FloatProperty(name="YW Rotation", default=0.0, min=0.0, max=2.0)
    rotation_zw: FloatProperty(name="ZW Rotation", default=0.0, min=0.0, max=2.0)
