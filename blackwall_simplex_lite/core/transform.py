import bpy
import math

from .state import object_4d_data


def rot4(v, a, b, angle):
    c = math.cos(angle)
    s = math.sin(angle)
    v_copy = v[:]
    va = v[a]
    vb = v[b]
    v_copy[a] = va * c - vb * s
    v_copy[b] = va * s + vb * c
    return v_copy


def proj4to3(p, w_depth=4.0):
    denom = w_depth - p[3]
    if abs(denom) < 1e-9:
        denom = 1e-9
    k = w_depth / denom
    return [p[0] * k, p[1] * k, p[2] * k]


def apply_4d_transform(vertex_4d, angles, scale=1.0):
    p = [vertex_4d[i] * scale for i in range(4)]

    if abs(angles['xy']) > 1e-6:
        p = rot4(p, 0, 1, angles['xy'])
    if abs(angles['xz']) > 1e-6:
        p = rot4(p, 0, 2, angles['xz'])
    if abs(angles['yz']) > 1e-6:
        p = rot4(p, 1, 2, angles['yz'])
    if abs(angles['xw']) > 1e-6:
        p = rot4(p, 0, 3, angles['xw'])
    if abs(angles['yw']) > 1e-6:
        p = rot4(p, 1, 3, angles['yw'])
    if abs(angles['zw']) > 1e-6:
        p = rot4(p, 2, 3, angles['zw'])

    return p


def ensure_timer_running():
    if not bpy.app.timers.is_registered(animation_update):
        bpy.app.timers.register(animation_update, persistent=True)


def animation_update():
    context = bpy.context

    if not hasattr(context.scene, "universal_4d_settings"):
        return 1.0 / 60.0

    if not object_4d_data:
        return 1.0 / 60.0

    if not hasattr(animation_update, "frame_counter"):
        animation_update.frame_counter = 0
    animation_update.frame_counter += 1

    current_time = animation_update.frame_counter / 60.0
    settings = context.scene.universal_4d_settings

    for obj_name in list(object_4d_data.keys()):
        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            continue

        data = object_4d_data[obj_name]
        if data.get("animation_running", False):
            _transform_4d_object(obj, data, settings, current_time)

    return 1.0 / 60.0


def _transform_4d_object(obj, data, settings, current_time):
    try:
        speed = settings.speed
        scale = settings.scale

        angles = {
            "xy": current_time * speed * settings.rotation_xy,
            "xz": current_time * speed * settings.rotation_xz,
            "yz": current_time * speed * settings.rotation_yz,
            "xw": current_time * speed * settings.rotation_xw,
            "yw": current_time * speed * settings.rotation_yw,
            "zw": current_time * speed * settings.rotation_zw,
        }

        if data.get("type") == "CURVE":
            _transform_curve_object(obj, data, angles, settings.w_depth, scale)
        else:
            _transform_mesh_object(obj, data, angles, settings.w_depth, scale)

    except Exception as exc:
        print(f"Error transforming {obj.name}: {exc}")


def _transform_mesh_object(obj, data, angles, w_depth, scale):
    try:
        mesh = obj.data
        original_vertices_4d = data["original_vertices_4d"]

        for i, vert in enumerate(mesh.vertices):
            if i < len(original_vertices_4d):
                transformed = apply_4d_transform(original_vertices_4d[i], angles, scale)
                proj = proj4to3(transformed, w_depth)
                vert.co.x = proj[0]
                vert.co.y = proj[1]
                vert.co.z = proj[2]

        mesh.update()

    except Exception as exc:
        print(f"Error transforming mesh {obj.name}: {exc}")


def _transform_curve_object(obj, data, angles, w_depth, scale):
    try:
        curve = obj.data
        edges = data["edges"]
        original_vertices_4d = data["original_vertices_4d"]

        transformed_vertices = []
        for vert_4d in original_vertices_4d:
            transformed = apply_4d_transform(vert_4d, angles, scale)
            proj = proj4to3(transformed, w_depth)
            transformed_vertices.append((proj[0], proj[1], proj[2]))

        while curve.splines and len(curve.splines) > 0:
            curve.splines.remove(curve.splines[-1])

        for edge in edges:
            if edge[0] < len(transformed_vertices) and edge[1] < len(transformed_vertices):
                spline = curve.splines.new('POLY')
                spline.points.add(1)
                a = (*transformed_vertices[edge[0]], 1.0)
                b = (*transformed_vertices[edge[1]], 1.0)
                spline.points[0].co = a
                spline.points[1].co = b
                spline.use_cyclic_u = False

    except Exception as exc:
        print(f"Error transforming curve {obj.name}: {exc}")


def reset_object_to_original(obj, data, w_depth):
    try:
        original_vertices_4d = data["original_vertices_4d"]

        if data.get("type") == "CURVE":
            curve = obj.data
            edges = data["edges"]
            original_vertices_3d = [proj4to3(v, w_depth) for v in original_vertices_4d]

            while curve.splines and len(curve.splines) > 0:
                curve.splines.remove(curve.splines[-1])

            for edge in edges:
                if edge[0] < len(original_vertices_3d) and edge[1] < len(original_vertices_3d):
                    spline = curve.splines.new('POLY')
                    spline.points.add(1)
                    a = (*original_vertices_3d[edge[0]], 1.0)
                    b = (*original_vertices_3d[edge[1]], 1.0)
                    spline.points[0].co = a
                    spline.points[1].co = b
                    spline.use_cyclic_u = False
        else:
            mesh = obj.data
            for i, vert in enumerate(mesh.vertices):
                if i < len(original_vertices_4d):
                    proj = proj4to3(original_vertices_4d[i], w_depth)
                    vert.co.x = proj[0]
                    vert.co.y = proj[1]
                    vert.co.z = proj[2]
            mesh.update()

    except Exception as exc:
        print(f"Error resetting {obj.name}: {exc}")
