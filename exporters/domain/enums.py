from enum import IntFlag


class BufferVertType(IntFlag):
    position = 0
    texcoord = 1
    texcoord1 = 2
    texcoord2 = 3
    lightmap_texcoord = 4
    normal = 5
    tangent = 6
    node_indices = 7
    node_weights = 8
    binormal = 9
    dual_quat_weight = 10
    vertex_color = 11
    vertex_alpha = 12
    tangent_UV2 = 13
    tangent_UV3 = 14
    change_15 = 15
    change_16 = 16
    change_17 = 17
    change_18 = 18


class IndexBufferType(IntFlag):
    DEFAULT = 0
    line_list = 1
    line_strip = 2
    triangle_list = 3
    triangle_patch = 4
    triangle_strip = 5
    quad_list = 6


class VertType(IntFlag):
    world = 0
    rigid = 1
    skinned = 2
    particle_model = 3
    screen = 4
    debug = 5
    transparent = 6
    particle = 7
    removed08 = 8
    removed09 = 9
    chud_simple = 10
    decorator = 11
    position_only = 12
    removed13 = 13
    ripple = 14
    removed15 = 15
    tessellatedTerrain = 16
    empty = 17
    decal = 18
    removed19 = 19
    removed20 = 20
    position_only_21 = 21
    tracer = 22
    rigid_boned = 23
    removed24 = 24
    CheapParticle = 25
    dq_skinned = 26
    skinned_8_weights = 27
    tessellated_vector = 28
    interaction = 29
    number_of_standard_vertex_types = 30

