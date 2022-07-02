import io
import math
import os
import struct


import numpy as np
import mathutils
import utils
from exporters.base_exporter import BaseExporter
from exporters.domain.domain_types import *
from exporters.to.fbx.export_to_fbx import FbxModel
from halo_infinite_tag_reader.model import Model
from halo_infinite_tag_reader.render_model import RenderModel


class ModelExporter(BaseExporter):

    def __init__(self, model: Model):
        super(ModelExporter, self).__init__()
        self.coun_index_dic = {}
        self.export_by_regions = False
        self.flipUv = True
        self.model = model
        self.obj_render_model: ObjRenderModel = ObjRenderModel()
        self._chunk_data = None
        self._chunk_data_map = {}
        self.render_model_inst = None
        self.export_separate_files = True
        self.split_in_parts = False
        self.minLOD = 0
        self.maxLOD = 0
        self.filepath_export = 'J:/Games/Halo Infinite Stuf/Extracted/Converted/RE_OtherGames/HI/models/'
        self.export_skl = True
        self.filterArmorCore = utils.CoreArmor.ALL
        self.import_weights = True
        self.debug_dict = {}

    def readVertBlockDesc(self, vert_block_desc, m_v_t_index):
        offset = vert_block_desc['offset'].value
        size = vert_block_desc['size'].value
        sub_data = self._chunk_data[offset:offset + size]
        vertex_count = vert_block_desc['vertex_count'].value
        vertex_stride = vert_block_desc['vertex_stride'].value
        vertex_type = vert_block_desc['vertex_type'].selected_index
        self.debug_dict[vert_block_desc['vertex_type'].selected] = vert_block_desc['unknown_off_4_8'].value
        bin_stream = io.BytesIO(sub_data)
        unknown_off_60_64 = vert_block_desc['unknown_off_60_64'].value
        if vertex_type == 0:
            return self.readPositionIn(bin_stream, vertex_count, vertex_stride, m_v_t_index)
        elif vertex_type == 1:
            return self.readTexcoordIn(bin_stream, vertex_count, 0, vertex_stride, m_v_t_index)
        elif vertex_type == 2:
            return self.readTexcoordIn(bin_stream, vertex_count, 1, vertex_stride, m_v_t_index)
        elif vertex_type == 5:
            return self.readNormalIn(bin_stream, vertex_count, vertex_stride, m_v_t_index)
        elif vertex_type == 7:
            return self.readNodeIndicesIn(bin_stream, vertex_count, vertex_stride, m_v_t_index)
        elif vertex_type == 8:
            return self.readNodeWeightsIn(bin_stream, vertex_count, vertex_stride, m_v_t_index)
        elif vertex_type == 10:
            return self.readDualQuatWeightIn(bin_stream, vertex_count, vertex_stride, m_v_t_index)
        else:
            array = [0.0] * vertex_count

            return array

    def readPositionIn(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
        vertx_pos_array = []
        model_scale = self.obj_render_model.render_geometry.compression_info[0].scale["model_scale"]
        f_from_bytes = int.from_bytes
        dict_vert = {}
        for x in range(vertex_count):
            chunk_data = bin_stream.read(vertex_stride)
            pos_x = f_from_bytes(chunk_data[0:2], 'little') / (2 ** 16 - 1) * model_scale[0][-1] + model_scale[0][0]
            pos_y = f_from_bytes(chunk_data[2:4], 'little') / (2 ** 16 - 1) * model_scale[1][-1] + model_scale[1][0]
            pos_z = f_from_bytes(chunk_data[4:6], 'little') / (2 ** 16 - 1) * model_scale[2][-1] + model_scale[2][0]
            pos_w = f_from_bytes(chunk_data[6:8], 'little')
            pos = (pos_x, pos_y, pos_z, pos_w)
            if dict_vert.keys().__contains__(pos):
                dict_vert[pos].append(x)
            else:
                dict_vert[pos] = [x]
            vertx_pos_array.append(pos)
        return vertx_pos_array, dict_vert

    def readTexcoordIn(self, bin_stream, vertex_count, n, vertex_stride, m_v_t_index):
        vertx_texcoor_array = []
        uv0_scale = self.obj_render_model.render_geometry.compression_info[0].scale["uv" + str(n) + "_scale"]
        f_from_bytes = int.from_bytes
        for x in range(vertex_count):
            chunk_data = bin_stream.read(vertex_stride)
            u = f_from_bytes(chunk_data[0:2], 'little') / (2 ** 16 - 1) * \
                uv0_scale[0][-1] + uv0_scale[0][0]
            v = f_from_bytes(chunk_data[2:4], 'little') / (2 ** 16 - 1) * \
                uv0_scale[1][-1] + uv0_scale[1][0]
            # uv0.append([u,v])
            if self.flipUv:
                v = -1 * v + 1
            vertx_texcoor_array.append((u, v))
        return vertx_texcoor_array

    def readNodeIndicesIn(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
        vert_data_array = []
        f_from_bytes = int.from_bytes
        for x in range(vertex_count):
            chunk_data = bin_stream.read(vertex_stride)
            x = f_from_bytes(chunk_data[0:1], 'little')
            y = f_from_bytes(chunk_data[1:2], 'little')
            z = f_from_bytes(chunk_data[2:3], 'little')
            w = f_from_bytes(chunk_data[3:4], 'little')
            if x > 120 or y > 120 or z > 120 or w > 120:
                debug = 1
            vert_data_array.append((x, y, z, w))
        return vert_data_array

    def readNodeWeightsIn(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
        vert_data_array = []
        f_from_bytes = int.from_bytes
        model_scale = self.obj_render_model.render_geometry.compression_info[0].scale["model_scale"]
        for x in range(vertex_count):
            chunk_data = bin_stream.read(vertex_stride)
            x = f_from_bytes(chunk_data[0:1], 'little', signed=False)
            y = f_from_bytes(chunk_data[1:2], 'little', signed=False)
            z = f_from_bytes(chunk_data[2:3], 'little', signed=False)
            w = f_from_bytes(chunk_data[3:4], 'little', signed=False)
            vert_data_array.append((x, y, z, w))
        if m_v_t_index == 1:
            debug = 1
        if m_v_t_index == 26:
            debug = 1
        return vert_data_array

    def readDualQuatWeightIn(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
        vert_data_array = []
        f_from_bytes = int.from_bytes
        for x in range(vertex_count):
            chunk_data = bin_stream.read(vertex_stride)
            x = f_from_bytes(chunk_data[0:1], 'little')
            y = f_from_bytes(chunk_data[1:2], 'little')
            z = f_from_bytes(chunk_data[2:3], 'little')
            w = f_from_bytes(chunk_data[3:4], 'little')
            vert_data_array.append((x, y, z, w))
        if m_v_t_index != 26:
            debug = 1
        return vert_data_array

    def readNormalIn(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
        vertx_normal_array = []
        f_from_bytes = int.from_bytes
        for x in range(vertex_count):
            chunk_offset = j = 0
            chunk_data = bin_stream.read(vertex_stride)
            x = (f_from_bytes(chunk_data[j:j + 2], 'little') & 0x3ff) / 1023 - 0.5
            y = ((f_from_bytes(chunk_data[j + 1:j + 3], 'little') & 0xffc) >> 2) / 1023 - 0.5
            z = ((f_from_bytes(chunk_data[j + 2:j + 4], 'little') & 0x3ff0) >> 4) / 1023 - 0.5

            sqrt_of_two = 2 ** 0.5

            # x /= sqrt_of_two
            # y /= sqrt_of_two
            # z /= sqrt_of_two
            w = (1 - x ** 2 - y ** 2 - z ** 2) ** 0.5

            missing = chunk_data[j + 3] >> 6
            # print(missing)
            if missing == 1:
                quat = mathutils.Quaternion((w, x, y, z))
            elif missing == 2:
                quat = mathutils.Quaternion((x, w, y, z))
            elif missing == 3:
                quat = mathutils.Quaternion((x, y, w, z))
            elif missing == 0:
                quat = mathutils.Quaternion((x, y, z, w))
            # print(f"Normal: {quat.to_euler()}")
            # norm_data = f_from_bytes(chunk_data[j:j+4],'little')
            # x = (norm_data & 0x3ff) / 1023
            # y = ((norm_data >> 10) & 0x3ff) / 1023
            # z = ((norm_data >> 20) & 0x3ff) / 1023
            # quat.rotate(mathutils.Euler((1,0.8,0),'XYZ'))
            vertx_normal_array.append(quat.to_axis_angle()[0])
        return vertx_normal_array

    def readIndexBlock(self, index_block_descr):
        """
        self.fillChunkDataArray(index_block_descr['offset'].value, index_block_descr[
            'size'].value)
        """
        sub_chunk_data = self._chunk_data[
                         index_block_descr['offset'].value:index_block_descr['offset'].value + index_block_descr[
                             'size'].value]
        bin_stream = io.BytesIO(sub_chunk_data)
        f_from_bytes = int.from_bytes
        index_array = []
        for i in range(index_block_descr['index_count'].value):
            index = f_from_bytes(bin_stream.read(2), 'little')
            index_array.append(index)
        return index_array

    def export(self):
        super(ModelExporter, self).export()
        if not self.model.is_loaded():
            self.model.load()
        if self.model.render_model is None:
            return
        self.readChunksData()

        if self._chunk_data is None:
            return
        self.render_model_inst = self.model.render_model.tag_parse.rootTagInst.childs[0]
        self.createScaleInfo()
        self.obj_render_model.name = self.render_model_inst['name'].str_value
        self.obj_render_model.nodes_data = self.model.render_model.getBonesInfo()
        mesh_resource = \
            self.render_model_inst['mesh resource groups'].childs[0]['mesh resource (unmapped type(_43)'].childs[0]
        instance = self.model.tag_parse.rootTagInst.childs[0]['variants']
        if instance.tagDef.N == 'variants':
            temp_mesh_s = None
            temp_mesh_r = None
            if not (self.model.render_model is None):
                temp_mesh_s = self.model.render_model.tag_parse.rootTagInst.childs[0]['meshes'].childs
                temp_mesh_r = self.model.render_model.tag_parse.rootTagInst.childs[0]['regions'].childs

            for ch in instance.childs:
                fbx_model = FbxModel(p_skl_data=self.obj_render_model.nodes_data)
                regions = ch['regions'].childs
                for region in regions:
                    region_name = region['region name']
                    temp_mesh_r_i = -1
                    for rn in temp_mesh_r:
                        if rn['name'].value == region_name.value:
                            temp_mesh_r_i = rn['permutations'].childs
                            break
                    for per in region['permutations'].childs:

                        per_mesh_index = per['runtime permutation index'].value
                        if temp_mesh_s is None:
                            continue
                        else:
                            if per_mesh_index != -1 and not (temp_mesh_r_i is None):
                                permutation = temp_mesh_r_i[per_mesh_index]
                                per_mesh_index_1 = permutation['mesh_index'].value
                                if per_mesh_index_1 == -1:
                                    continue
                                temp_name = '-1'
                                mesh_name = ''
                                for m_index in range(per_mesh_index_1, per_mesh_index_1 + permutation['mesh_count'].value):
                                    mesh = temp_mesh_s[m_index]

                                    t_m = self.processMeshInst(mesh, mesh_resource)

                                    material_path = t_m.LOD_render_data[0].parts[0].material_path
                                    mesh_name = ''
                                    if len(material_path.split('\\')) >= 1:
                                        mesh_name += material_path.split('\\')[-1]
                                    if temp_name == mesh_name:
                                        continue

                                    if mesh_name == '':
                                        mesh_name = "unknown mesh"

                                    temp_name = mesh_name
                                    print(mesh_name)

                                    t_m.name = mesh_name
                                    t_m.name = utils.getNamePart(t_m)
                                    fbx_model.add(t_m)


                            else:
                                continue
                temp_str = self.model.filename.split('\\')[-1].replace('.', '_')
                sub_dir = f"{temp_str}/variants/"
                os.makedirs(f"{self.filepath_export}{sub_dir}", exist_ok=True)
                save_path = f"{self.filepath_export}{sub_dir}{ch['name'].str_value}.fbx"
                fbx_model.export(save_path, True)
                print(f"Saved model to {save_path}")





        print('end Export')

    def initChunksData(self):
        if self._chunk_data is None:
            chunk_data_map: {str: []} = {}
            more_chunks = True
            self._chunk_data = b""
            nChunk = 0
            ch_offset = 0
            while more_chunks:
                try:
                    chunk_path = f"{self.render_model.filename}[{nChunk}_mesh_resource.chunk{nChunk}]"
                    temp_len = os.path.getsize(chunk_path)
                    self._chunk_data_map[ch_offset] = (chunk_path, temp_len)

                    ch_offset += temp_len
                    """
                    size_str = f"{temp_len / 1000000} MB" if temp_len > 1000000 else f"{temp_len / 1000} KB"
                    if chunk_data_map.keys().__contains__(size_str):
                        chunk_data_map[size_str].append(nChunk)
                    else:
                        chunk_data_map[size_str] = [nChunk]
                    """
                    nChunk += 1
                except:
                    more_chunks = False

            self._chunk_data = np.empty(ch_offset, dtype=object)
            print(f"Read {nChunk} chunks ({hex(len(self._chunk_data))} bytes)")

    def fillChunkDataArray(self, offset, size):
        if not self._chunk_data[offset] is None and not self._chunk_data[offset + size] is None:
            return

        keys = list(self._chunk_data_map.keys())
        init_key = 0
        if keys.__contains__(offset):
            init_key = keys.index(offset)

        for ki, k_offset in enumerate(keys, start=init_key):
            if k_offset <= offset <= keys[ki + 1]:
                increasing = 1
                self.readChunkData(self._chunk_data_map[keys[ki]],keys[ki])
                print(self._chunk_data_map[keys[ki]][0])
                while offset + size > keys[ki + increasing]:
                    self.readChunkData(self._chunk_data_map[keys[ki + increasing]], keys[ki + increasing])
                    print(self._chunk_data_map[keys[ki + increasing]])
                    increasing += 1
                return

    def readChunkData(self, chunk_info, offset):
        chunk_path = chunk_info[0]
        with open(chunk_path, 'rb') as ch_file:
            k = offset
            while True:
                buf = ch_file.read(1)
                if not buf:
                    break
                self._chunk_data[k] = buf
                k += 1

            ch_file.close()

    def readChunksData(self):
        if self._chunk_data is None:
            chunk_data_map: {str: []} = {}
            more_chunks = True
            self._chunk_data = b""
            nChunk = 0
            ch_offset = 0
            while more_chunks:
                try:
                    chunk_path = f"{self.model.render_model.filename}[{nChunk}_mesh_resource.chunk{nChunk}]"
                    self._chunk_data_map[ch_offset] = chunk_path
                    # print(f"Trying to read chunk {chunk_path}")
                    chunk_data_temp = []
                    ch_offset += os.path.getsize(chunk_path)

                    with open(chunk_path, 'rb') as ch_file:

                        chunk_data_temp = ch_file.read()
                        ch_file.close()

                    arr = np.empty(10, dtype=bytes)
                    self._chunk_data += chunk_data_temp
                    temp_len = len(chunk_data_temp)
                    size_str = f"{temp_len / 1000000} MB" if temp_len > 1000000 else f"{temp_len / 1000} KB"
                    # print(f" Chunk n: {nChunk}. size {size_str}")
                    if chunk_data_map.keys().__contains__(size_str):
                        chunk_data_map[size_str].append(nChunk)
                    else:
                        chunk_data_map[size_str] = [nChunk]
                    nChunk += 1
                except:
                    more_chunks = False
            print(f"Read {nChunk} chunks ({hex(len(self._chunk_data))} bytes)")

    def processMeshInst(self, mesh, mesh_resource, m_i=-1) -> ObjMesh:
        obj_mesh = ObjMesh()
        obj_mesh.clone_index = mesh["clone_index"].value
        obj_mesh.mesh_flags = mesh["mesh_flags"].options
        obj_mesh.rigid_node_index = mesh["rigid_node_index"].value
        m_v_t_index = mesh["vertex_type"].selected_index
        obj_mesh.vertex_type = m_v_t_index
        obj_mesh.vert_type = m_v_t_index
        obj_mesh.use_dual_quat = mesh["use_dual_quat"].value
        obj_mesh.index_buffer_type = mesh["index_buffer_type"].selected_index
        obj_mesh.clone_index = mesh["clone_index"].value

        for lod_i, lod in enumerate(mesh['LOD_render_data'].childs):
            if not (self.minLOD <= lod_i <= self.maxLOD):
                continue
            obj_lod = ObjLOD()
            vertx_blocks = {}
            min_offset = -1
            max_offset = -1
            size_sum = 0
            last_size = -1
            for xi, x in enumerate(lod['vertex_buffer_indices'].childs):
                temp_vert_index_block = x.value
                if temp_vert_index_block != -1:
                    vertx_block_descr = mesh_resource['vertex_blocks'].childs[temp_vert_index_block]
                    vertex_type_ = vertx_block_descr['vertex_type'].selected
                    vertex_type_index = vertx_block_descr['vertex_type'].selected_index
                    offset = vertx_block_descr['offset'].value
                    size = vertx_block_descr['size'].value
                    print(f"{m_i}-{lod_i}-{vertex_type_}")
                    #self.fillChunkDataArray(offset, size)

                    if max_offset == -1:
                        max_offset = offset
                        min_offset = offset
                        last_size = size
                    elif max_offset < offset:
                        max_offset = offset
                        last_size = size
                    elif min_offset > offset:
                        min_offset = offset
                    if self.coun_index_dic.keys().__contains__(temp_vert_index_block):
                        self.coun_index_dic[temp_vert_index_block] += 1
                    else:
                        self.coun_index_dic[temp_vert_index_block] = 0
                    size_sum += size
                    vertx_data = self.readVertBlockDesc(vertx_block_descr, m_v_t_index)
                    vertx_blocks[vertex_type_] = vertx_data
                    obj_lod.setVertBufferArray(vertex_type_index, vertx_data)
            s_t = (max_offset - min_offset) + last_size
            if s_t == size_sum:
                debug = 1
            else:
                debug = 1
            index_buffer_index = lod['index_buffer_index'].value

            if index_buffer_index == -1:
                continue
            else:
                index_block_descr = mesh_resource['index_blocks'].childs[index_buffer_index]
            s_t_1 = max_offset + last_size
            if index_block_descr['offset'].value == s_t_1:
                debug = 1
            else:
                debug = 1
            obj_lod.lod_flags = lod['lod_flags'].options
            obj_lod.lod_render_flags = lod['lod_render_flags'].options
            obj_lod.index_buffer_index = self.readIndexBlock(index_block_descr)
            obj_lod.vertex_buffer_indices = vertx_blocks

            for part in lod['parts'].childs:
                obj_part = ObjPart()
                path_mat = part['material_index'].extra_data['path']
                obj_part.index_start = part['index_start'].value
                obj_part.part_type = part['part_type'].value
                obj_part.index_count = part['index_count'].value
                obj_part.budget_vertex_count = part['budget_vertex_count'].value
                obj_part.part_flags = part['part_flags'].options
                obj_part.material_index = part['material_index'].value
                obj_part.mat_string = path_mat
                obj_part.material_path = path_mat
                obj_lod.parts.append(obj_part)

            for subpart in lod['subparts'].childs:
                obj_subpart = ObjSubPart()
                obj_subpart.index_start = subpart['index_start'].value
                obj_subpart.index_count = subpart['index_count'].value
                obj_subpart.part_index = subpart['part_index'].value
                obj_subpart.budget_vertex_count = subpart['budget_vertex_count'].value
                obj_lod.sub_parts.append(obj_subpart)

            obj_mesh.LOD_render_data.append(obj_lod)
        return obj_mesh

    def createScaleInfo(self):
        for compression_info in self.render_model_inst['compression_info'].childs:
            obj_compression_inf = ObjCompressionInfo()
            obj_compression_inf.compression_flags = compression_info['compression_flags']
            obj_compression_inf.scale["model_scale"] = [
                [compression_info['position_x_bounds'].min,
                 compression_info['position_x_bounds'].max,
                 compression_info['position_x_bounds'].max - compression_info['position_x_bounds'].min],
                [compression_info['position_y_bounds'].min,
                 compression_info['position_y_bounds'].max,
                 compression_info['position_y_bounds'].max - compression_info['position_y_bounds'].min],
                [compression_info['position_z_bounds'].min,
                 compression_info['position_z_bounds'].max,
                 compression_info['position_z_bounds'].max - compression_info['position_z_bounds'].min]
            ]

            obj_compression_inf.scale["uv0_scale"] = [
                [compression_info["texcoord_u0_bounds"].min, compression_info["texcoord_u0_bounds"].max,
                 compression_info["texcoord_u0_bounds"].max - compression_info["texcoord_u0_bounds"].min],
                [compression_info["texcoord_v0_bounds"].min, compression_info["texcoord_v0_bounds"].max,
                 compression_info["texcoord_v0_bounds"].max - compression_info["texcoord_v0_bounds"].min]
            ]

            obj_compression_inf.scale["uv1_scale"] = [
                [compression_info["texcoord_u1_bounds"].min, compression_info["texcoord_u1_bounds"].max,
                 compression_info["texcoord_u1_bounds"].max - compression_info["texcoord_u1_bounds"].min],
                [compression_info["texcoord_v1_bounds"].min, compression_info["texcoord_v1_bounds"].max,
                 compression_info["texcoord_v1_bounds"].max - compression_info["texcoord_v1_bounds"].min]
            ]

            obj_compression_inf.scale["uv2_scale"] = [
                [compression_info['texcoord_u2_bounds '].min, compression_info['texcoord_u2_bounds '].max,
                 compression_info['texcoord_u2_bounds '].max - compression_info['texcoord_u2_bounds '].min],
                [compression_info['texcoord_v2_bounds '].min, compression_info['texcoord_v2_bounds '].max,
                 compression_info['texcoord_v2_bounds '].max - compression_info['texcoord_v2_bounds '].min]
            ]
            self.obj_render_model.render_geometry.compression_info.append(obj_compression_inf)
