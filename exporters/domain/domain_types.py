from commons.enums_struct_def import PcVertexBuffersUsage
from exporters.domain.enums import *


class ObjRgPermutation:
    def __init__(self):
        self.name = ""
        self.mesh_index = -1
        self.mesh_count = -1
        self.clone_name = ""


class ObjRgRegion:
    def __init__(self):
        self.name = ""
        self.permutations: [ObjRgPermutation] = []


class ObjRgMarkers:
    def __init__(self):
        self.name = ""
        self.region_index = -1
        self.permutation_index = -1
        self.node_index = -1
        self.flags = {}
        self.translation = []
        self.rotation = []
        self.scale = []
        self.direction = []


class ObjNode:
    def __init__(self):
        self.name = ""


class ObjMaterial:
    def __init__(self):
        self.material_path = ""


class ObjRenderModel:
    def __init__(self):
        self.name = ""
        self.flags = {}
        self.regions: [ObjRgRegion] = []
        self.nodes: [ObjNode] = []
        self.nodes_data: {str: ObjNode} = {}
        self.marker_groups: [ObjRgMarkers] = []
        self.materials: [ObjMaterial] = []
        self.meshes: [ObjMesh] = []
        self.render_geometry: ObjRenderGeometry = ObjRenderGeometry()


class ObjRenderGeometry:
    def __init__(self):
        self.meshes: [ObjMesh] = []
        self.compression_info = []
        self.per_mesh_node_map = [[]]


class ObjCompressionInfo:
    def __init__(self):
        self.compression_flags = {}
        self.scale = {}


class AttachmentInfo:
    def __init__(self):
        self.node_index = -1
        self.translation = (0, 0, 0)
        self.rotation = (0, 0, 0)
        self.scale = (1, 1, 1)
        self.direction = (0, 0, 0)


class ObjMesh:
    def __init__(self):
        self.LOD_render_data: [ObjLOD] = []
        self.name = ""
        self.bones = []
        self.bones_data = {}
        self.parts = []
        self.rigid_node_index = -1
        self.use_dual_quat = False
        self.clone_index = -1
        self.mesh_flags = {}
        self.vert_type: VertType = VertType.rigid
        self.index_buffer_type: IndexBufferType = IndexBufferType.DEFAULT
        self.attachment_info: AttachmentInfo = None

    def generateFaceIndexOfLod(self, lod_index):
        return self.LOD_render_data[lod_index].generateFaceIndex(self.index_buffer_type)

    def getFaceMaterialIndexOfLod(self, indexFace, lod_index):
        return self.LOD_render_data[lod_index].getFaceMaterialIndex(indexFace)


class ObjLOD:

    def __init__(self, p_mesh):

        self.vertex_colour = []
        self.unique_pos_vert = {}
        self.parts: [ObjPart] = []
        self.sub_parts: [ObjSubPart] = []
        self.vertex_buffer_indices = {}
        self.index_buffer_index = []
        self.lod_flags = {}
        self.lod_render_flags = {}
        self.vert_count = 0
        self.name = ''
        # index buffers
        self.faces = []
        self.vert_pos = []
        self.vert_uv0 = []
        self.vert_uv1 = []
        self.vert_norm = []
        self.vert_tangent = []
        self.vert_index = []
        self.weight_indices = []
        self.weights = []
        self.dual_quat_weight = []
        self.weight_pairs = []
        self.mesh_container: ObjMesh = p_mesh

    def generateFaceIndex(self, index_buffer_type = IndexBufferType.triangle_list):
        self.faces = []
        if index_buffer_type == IndexBufferType.triangle_list:
            faces = {}
            faces_v = {}
            nFace = 0
            # faces.extend((0.0,)*(src_mesh.index_block.size//(index_len*3)))
            vert_index = self.index_buffer_index
            for v_i in range(0, vert_index.__len__(), 3):
                # read 3 16-bit integers that correspond to the vertex ids of the vertices of the face

                index_1 = vert_index[v_i]
                index_2 = vert_index[v_i + 1]
                index_3 = vert_index[v_i + 2]
                """
                
                index_1 = self.getUniqVertPos(vert_index[v_i])
                index_2 = self.getUniqVertPos(vert_index[v_i + 1])
                index_3 = self.getUniqVertPos(vert_index[v_i + 2])
                """
                # if index_1 >= len(vert_arr) or index_2 >= len(vert_arr) or index_3 >= len(vert_arr):
                #    print(f"Invalid vertex index on face {nFace}! Skipping mesh (would likely be very broken otherwise)")
                #    print(f"(data at {hex(face_start)})")
                #    print(f"data array size {hex(len(chunk_data))}")
                #    return
                """
                faces_v[nFace] = {
                    index_1:(self.weight_indices[index_1],self.weights[index_1]),
                    index_2:(self.weight_indices[index_2],self.weights[index_2]),
                    index_3:(self.weight_indices[index_3],self.weights[index_3]),
                }
                """
                faces[nFace] = [index_1, index_2, index_3]
                nFace += 1

            # print("faces done")
            # TODO Crteate Mesh
            self.faces = list(faces.values())
            if len(faces) < 1:
                debug = 1
            return self.faces
        else:
            debug = 1

        return self.faces

    def generateWeightPairs(self):
        self.weight_pairs = []

        if len(self.weight_indices) != len(self.weights):
            if len(self.weight_indices) != 0 and len(self.weights) == 0:
                for i in range(self.weight_indices.__len__()):
                    self.weight_pairs.append((self.weight_indices[i], (1, 1, 1, 1)))
            else:
                debug = 1
        else:
            self.weight_pairs = []

            for i in range(self.weight_indices.__len__()):
                dq_weight = []
                if len(self.dual_quat_weight) != 0:
                    dq_weight = self.dual_quat_weight[i]
                self.weight_pairs.append(self._processWeightPairs_3(i, self.weight_indices[i], self.weights[i], dq_weight))

        return self.weight_pairs

    def _processWeightPairsVertPos(self, vert_index):
        list_v_w= []

        for i in vert_index:
            list_v_w.append((self.weight_indices[i],self.weights[i]))
        debug = 1

    def getUniqVertPos(self, v_i):
        return self.unique_pos_vert[self.vert_pos[v_i]][0]

    def _processWeightPairs_1(self, vert_index, weight_indices, p_weights, p_dq_weights = []):
        w_pairs = {}
        _weights = p_weights
        bone_name_list = []
        repetidos = {}
        repetidos_no_z = {}

        for i, wi in enumerate(weight_indices):
            bone_info_name = self.mesh_container.bones_data['skeletons'][wi]['name']
            bone_name_list.append(bone_info_name)
            if w_pairs.keys().__contains__(wi):
                if repetidos.keys().__contains__(weight_indices[i]):
                    repetidos[weight_indices[i]] += 1
                else:
                    repetidos[weight_indices[i]] = 1

                if w_pairs[wi] !=0:
                    if repetidos_no_z.keys().__contains__(weight_indices[i]):
                        repetidos_no_z[weight_indices[i]] += 1
                    else:
                        repetidos_no_z[weight_indices[i]] = 1

                    if len(p_dq_weights) == 0:
                        debug = True
                    # assert len(p_dq_weights) != 0, f'Solo en QA m_name {self.parts[0].material_path}'
                    if weight_indices[i] != weight_indices[i-1]:
                        #assert i==3, 'el ultimo siempre es el primero si se repite'
                        if i!=3:
                            debug = True
                        if weight_indices[i]!=3 or weight_indices[i]!=73:
                            debug = True
                        assert weight_indices[i]==3 or weight_indices[i]==73, f'solo pasa con pelvis y lef hand {weight_indices}'
                        #assert weight_indices[i]==weight_indices[0], 'el ultimo siempre es el primero si se repite'
                        if weight_indices[i]!=weight_indices[0]:
                            debug = True

                    # assert weight_indices[i] != weight_indices[i-1] and i==3, 'si tiena mas de 1 hueso y se repite, debe estar al final'

                w_pairs[wi] = w_pairs[wi] + _weights[i]
            else:
                w_pairs[wi] = _weights[i]

        if len(repetidos_no_z) != 0:
            if len(repetidos_no_z) != 1:
                assert False, f'Solo se debe repetir un hueso vertex {vert_index}, {weight_indices}, {bone_name_list} and w {p_weights}, {repetidos_no_z}'

        if sum(p_weights[0:4]) != 0:
            last_index_0 = -1
            for i, wi in enumerate(weight_indices):
                if p_weights[i]==0:
                    last_index_0 = i

            if last_index_0 != -1 and weight_indices[last_index_0]!=weight_indices[last_index_0-1]:
                arra_sub_w = p_weights[last_index_0:4]
                arra_sub_i = weight_indices[last_index_0:4]
                debug = True


        #assert repetidos_no_z.keys()[0]==3 or repetidos_no_z.keys()[0]==73, f'Solo se debe repetir un hueso vertex {vert_index}, {weight_indices}, {bone_name_list} and w {p_weights}'
        if len(repetidos)!=0 and len(repetidos)!=1:
            print(f' Se repetir mas de un hueso, vertex {vert_index}, {weight_indices}, {bone_name_list} and w {p_weights}')


        suma_to_n = sum(w_pairs.values())

        if suma_to_n == 0:
            count =len(w_pairs.keys())
            if count>1:
                for key in w_pairs.keys():
                    w_pairs[key] = 1/count
            else:
                for key in w_pairs.keys():
                    if w_pairs[key] != 1:
                        w_pairs[key] = 1
        else:
            if w_pairs.__len__() == 1:
                for key in w_pairs.keys():
                    if w_pairs[key] != 1:
                        sum_w = sum(p_weights[4:8])
                        r_sum_w = round(sum_w, 1)
                        """
                        if not (w_pairs[key] == 0):
                            print(f'si es un solo hueso y no es 1 deberia ser 0, bone name {bone_name_list[0]} '
                                  f'vert_inex {vert_index}, {w_pairs[key]}, {weight_indices}, {p_weights}, r_sum_w {r_sum_w}')
                        no es significativo solo 156 puede ser error de lectura o descomprension
                        
                        """
                        w_pairs[key] = 1
            else:
                keys = list(w_pairs.keys())
                sum_w = sum(p_weights[4:8])
                for key in keys:
                    bone_info = self.mesh_container.bones_data['skeletons'][key]
                    if w_pairs[key] == 0:
                        del w_pairs[key]
                        if sum_w>1:
                            debug = True
                    else:
                        w_pairs[key] = w_pairs[key]/ suma_to_n

                if len(w_pairs) == 1 and w_pairs[list(w_pairs.keys())[0]]!=1:
                    debug = 1

        return [list(w_pairs.keys()), list(w_pairs.values())]

    def _processWeightPairs_2(self, vert_index, weight_indices, p_weights, p_dq_weights = []):
        _weights = p_weights[4:8]
        initial_w = 1
        rest = initial_w
        w_pairs = {}
        for i,b_i in enumerate(weight_indices):
            temp_rest = rest - _weights[i]*0.5
            if temp_rest < 0:
                w_pairs[b_i] = 1 - temp_rest
                break
            w_pairs[b_i] = temp_rest
            rest = temp_rest

        return [list(w_pairs.keys()), list(w_pairs.values())]

    def _processWeightPairs_3(self, vert_index, weight_indices, p_weights, p_dq_weights = []):
        _weights = p_weights
        initial_w = 1
        rest = initial_w
        w_pairs = {}
        for i,b_i in enumerate(weight_indices):
            if i ==3:
                temp_rest = 1-sum(list(w_pairs.values()))
            else:
                temp_rest = rest - _weights[i]

            if temp_rest < 0:
                w_pairs[b_i] = 1 - temp_rest
                break
            w_pairs[b_i] = temp_rest
            rest = temp_rest
        if sum(list(w_pairs.values())) != 1:
            debug = True
        return [list(w_pairs.keys()), list(w_pairs.values())]






    def _processWeightPairs(self, weight_indices, p_weights):
        w_pairs = {}
        #round( w / 255.00, 4)
        suma = 0
        weights = list(p_weights)
        suma_to_n = sum(p_weights)
        for k, wi in enumerate(weights):
            #weights[k] = round(wi / 255.00, 4)
            if suma_to_n != 0:
                weights[k] = wi/255
            suma = suma + wi/255

        if suma==1:
            debug = 1
        for i, wi in enumerate(weight_indices):
            if w_pairs.keys().__contains__(wi):
                if w_pairs[wi] !=0:
                   debug = 1
                w_pairs[wi] = w_pairs[wi] + weights[i]
            else:
                w_pairs[wi] = weights[i]


            #w_pairs[key] = 1 - w_pairs[key]

        if w_pairs.__len__() == 1:
            for key in w_pairs.keys():
                if w_pairs[key] != 1:
                    w_pairs[key] = 1
        else:
            keys = list(w_pairs.keys())

            """"""
            for key in keys:
                if w_pairs[key] == 0:
                    del w_pairs[key]


            keys = list(w_pairs.keys())
            cant_b=len(keys)
            if cant_b == 2:
                debug = 1

            rest = 0
            for key in keys:
                #w_pairs[key] = 1-w_pairs[key]
                w_pairs[key] = 1/cant_b*w_pairs[key]


        return [list(w_pairs.keys()), list(w_pairs.values())]
        #return [weight_indices, weights]

    def getFaceMaterialIndex(self, indexFace):
        if len(self.parts) > 1:
            for p, part in enumerate(self.parts):
                if int(part.index_start / 3) <= indexFace < int(
                        (part.index_start + part.index_count) / 3):
                    return p
        else:
            return 0

    def setVertBufferArray(self, vertex_type_index, vertx_data):
        if vertex_type_index == PcVertexBuffersUsage.Position:
            self.vert_pos = vertx_data[0]
            self.unique_pos_vert = vertx_data[1]
            self.vert_count = len(self.vert_pos)
        elif vertex_type_index == PcVertexBuffersUsage.UV0:
            self.vert_uv0 = vertx_data
        elif vertex_type_index == PcVertexBuffersUsage.UV1:
            self.vert_uv1 = vertx_data
        elif vertex_type_index == PcVertexBuffersUsage.Tangent:
            self.vert_tangent = vertx_data
        elif vertex_type_index == PcVertexBuffersUsage.Normal:
            self.vert_norm = vertx_data
        elif vertex_type_index == PcVertexBuffersUsage.BlendWeights1:
            self.dual_quat_weight = vertx_data
            """
            if len(self.dual_quat_weight) !=0:
                pares = []
                for ti, tupla in enumerate(self.weights):
                    pares.append((tupla, self.dual_quat_weight[ti],[sum(tupla),sum(self.dual_quat_weight[ti])]))
                debug = True
            """
        elif vertex_type_index == PcVertexBuffersUsage.BlendWeights0:
            self.weights = vertx_data
        elif vertex_type_index == PcVertexBuffersUsage.BlendIndices0:
            self.weight_indices = vertx_data
        elif vertex_type_index == PcVertexBuffersUsage.Color:
            self.vertex_colour = vertx_data


class ObjPart:

    def __init__(self):
        self.material_index = -1
        self.material_path = -1
        self.index_start = -1
        self.index_count = -1
        self.part_type = -1
        self.part_flags = {}
        self.budget_vertex_count = -1
        self.mat_string = ""
        self.material = None


class ObjSubPart:

    def __init__(self):
        self.index_start = -1
        self.index_count = -1
        self.part_index = -1
        self.budget_vertex_count = -1
