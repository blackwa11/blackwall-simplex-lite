import bpy
from bpy.props import FloatProperty
from bpy.types import Operator

from ..core.geometry import Simplex4D
from ..core.materials import get_or_create_material
from ..core.state import object_4d_data
from ..core.transform import proj4to3


class UNIVERSAL_OT_create_simplex(Operator):
    bl_idname = "universal.create_simplex"
    bl_label = "Create Simplex"
    bl_description = "Create 4D simplex"
    bl_options = {'REGISTER', 'UNDO'}

    size: FloatProperty(name="Size", default=1.0, min=0.1, max=5.0)

    def execute(self, context):
        try:
            settings = context.scene.universal_4d_settings
            vertices_4d, edges = Simplex4D.generate_simplex(self.size)
            vertices_3d = [proj4to3(v, settings.w_depth) for v in vertices_4d]

            mat = get_or_create_material()

            if settings.object_type == 'CURVE':
                curve = bpy.data.curves.new("Simplex_Curve", 'CURVE')
                curve.dimensions = '3D'
                curve.bevel_depth = 0.02

                for edge in edges:
                    spline = curve.splines.new('POLY')
                    spline.points.add(1)
                    a = (*vertices_3d[edge[0]], 1.0)
                    b = (*vertices_3d[edge[1]], 1.0)
                    spline.points[0].co = a
                    spline.points[1].co = b
                    spline.use_cyclic_u = False

                obj = bpy.data.objects.new("Simplex_Curve", curve)
                context.collection.objects.link(obj)
                data_type = "CURVE"
            else:
                mesh = bpy.data.meshes.new("Simplex_Mesh")
                mesh.from_pydata(vertices_3d, edges, [])
                mesh.update()

                obj = bpy.data.objects.new("Simplex_Mesh", mesh)
                context.collection.objects.link(obj)
                data_type = "MESH"

            if len(obj.data.materials) == 0:
                obj.data.materials.append(mat)
            else:
                obj.data.materials[0] = mat

            for other in context.selected_objects:
                other.select_set(False)
            obj.select_set(True)
            context.view_layer.objects.active = obj

            object_4d_data[obj.name] = {
                "type": data_type,
                "vertices_4d": [v[:] for v in vertices_4d],
                "original_vertices_4d": [v[:] for v in vertices_4d],
                "edges": edges,
                "animation_running": False,
            }

            self.report({'INFO'}, f"Simplex {data_type.lower()} created")
            return {'FINISHED'}

        except Exception as exc:
            self.report({'ERROR'}, f"Error: {str(exc)}")
            return {'CANCELLED'}
