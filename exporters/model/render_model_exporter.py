import binascii
import io
import os
import struct

import numpy as np
import mathutils
import utils
from commons.classes import Chunk
from commons.debug_utils import fillDebugDict, vertx_data_arrays
from commons.enums_struct_def import PcVertexBuffersFormat
from configs.config import Config
from exporters.model.base_exporter import BaseExporter
from exporters.domain.domain_types import *
from exporters.to.fbx.export_to_fbx import FbxModel
from tag_reader.readers.render_model import RenderModel


class ExportBy(IntFlag):
    MESH_LIST = 0
    REGION = 1


class RenderModelExporter(BaseExporter):

    def __init__(self, render_model: RenderModel):
        super(RenderModelExporter, self).__init__()
        self.coun_index_dic = {}
        self.export_by_regions = False
        self.flipUv = True
        self.render_model = render_model
        self.obj_render_model: ObjRenderModel = ObjRenderModel()
        self._chunk_data = None
        self._chunk_data_map = {}
        self.render_model_inst = None
        self.export_separate_files = True
        self.split_in_parts = False
        self.minLOD = 0
        self.maxLOD = 0
        self.filepath_export = Config.MODEL_EXPORT_PATH
        self.export_skl = True
        self.filterArmorCore = utils.CoreArmor.ALL
        self.import_weights = True
        self.debug_dict = {}

    def readVertBlockDesc(self, vert_block_desc, m_v_t_index):
        offset = vert_block_desc['offset'].value
        size = vert_block_desc['byte width'].value
        sub_data = self.getChunkDataBy(offset, size)
        # sub_data = self._chunk_data[offset:offset + size]
        vertex_count = vert_block_desc['count'].value
        vertex_stride = vert_block_desc['stride'].value
        vertex_usage = vert_block_desc['usage'].selected_index
        vertex_usage_str = vert_block_desc['usage'].selected
        vertex_format = vert_block_desc['format'].selected_index
        vertex_format_str = vert_block_desc['format'].selected
        bin_stream = io.BytesIO(sub_data)

        if vertex_format == PcVertexBuffersFormat.wordVector4DNormalized:
            return self.readWordVector4DNormalized(bin_stream, vertex_count, vertex_stride, m_v_t_index)
        elif vertex_format == PcVertexBuffersFormat.wordVector2DNormalized:
            n = 0
            if vertex_usage == PcVertexBuffersUsage.UV0:
                n = 0
            elif vertex_usage == PcVertexBuffersUsage.UV1:
                n = 1
            elif vertex_usage == PcVertexBuffersUsage.UV2:
                n = 2
            return self.readWordVector2DNormalized(bin_stream, vertex_count, n, vertex_stride, m_v_t_index)
        elif vertex_format == PcVertexBuffersFormat.wordVector2DNormalized:
            return self.readWordVector2DNormalized(bin_stream, vertex_count, 1, vertex_stride, m_v_t_index)
        elif vertex_format == PcVertexBuffersFormat.byteARGBColor:
            return self.readByteARGBColor(bin_stream, vertex_count, vertex_stride, m_v_t_index)
        elif vertex_format == PcVertexBuffersFormat.f_10_10_10_2_signedNormalizedPackedAsUnorm:
            return self.readF_10_10_10_2_signedNormalizedPackedAsUnorm(bin_stream, vertex_count, vertex_stride,
                                                                       m_v_t_index)
        elif vertex_format == PcVertexBuffersFormat.byteUnitVector3D:
            return self.readByteUnitVector3D(bin_stream, vertex_count, vertex_stride, m_v_t_index)
        elif vertex_format == PcVertexBuffersFormat.byteVector4D:
            return self.readByteVector4D(bin_stream, vertex_count, vertex_stride, m_v_t_index)
        elif vertex_format == PcVertexBuffersFormat.f_10_10_10_normalized:
            return self.readF_10_10_10_normalized(bin_stream, vertex_count, vertex_stride, m_v_t_index)
        elif vertex_format == PcVertexBuffersFormat.real:
            return self.readReal(bin_stream, vertex_count, vertex_stride, m_v_t_index)
        else:
            array = [0.0] * vertex_count

            return array

    def readByteARGBColor(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
        vertx_pos_array = []
        f_from_bytes = int.from_bytes
        for x in range(vertex_count):
            chunk_data = bin_stream.read(vertex_stride)
            A = f_from_bytes(chunk_data[0:1], 'little')
            R = f_from_bytes(chunk_data[1:2], 'little')
            G = f_from_bytes(chunk_data[2:3], 'little')
            B = f_from_bytes(chunk_data[3:4], 'little')

            vertx_pos_array.append((A, R, G, B))

        return vertx_pos_array

    def readWordVector4DNormalized(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
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

    def readWordVector2DNormalized(self, bin_stream, vertex_count, n, vertex_stride, m_v_t_index):
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

    def readReal(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
        vert_data_array = []
        f_from_bytes = int.from_bytes
        for x in range(vertex_count):
            chunk_data = bin_stream.read(vertex_stride)
            vert_data_array.append(struct.unpack('f', chunk_data)[0])

        return vert_data_array

    def readByteUnitVector3D(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
        vert_data_array = []
        f_from_bytes = int.from_bytes
        for x in range(vertex_count):
            chunk_data = bin_stream.read(vertex_stride)
            x = f_from_bytes(chunk_data[0:1], 'little', signed=False)
            y = f_from_bytes(chunk_data[1:2], 'little', signed=False)
            z = f_from_bytes(chunk_data[2:3], 'little', signed=False)
            vert_data_array.append((x, y, z))
        return vert_data_array

    def readByteVector4D(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
        vert_data_array = []
        f_from_bytes = int.from_bytes
        for x in range(vertex_count):
            chunk_data = bin_stream.read(vertex_stride)
            x = f_from_bytes(chunk_data[0:1], 'little')
            y = f_from_bytes(chunk_data[1:2], 'little')
            z = f_from_bytes(chunk_data[2:3], 'little')
            w = f_from_bytes(chunk_data[3:4], 'little')
            vert_data_array.append((x, y, z, w))
        return vert_data_array

    def readF_10_10_10_normalized(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
        vert_data_array = []
        f_from_bytes = int.from_bytes
        for x in range(vertex_count):
            chunk_data = bin_stream.read(vertex_stride)
            binary_string = binascii.unhexlify(chunk_data.hex())
            x_big = f_from_bytes(chunk_data[0:1], 'big')
            x_big_bit = '{:>08b}'.format(x_big)
            y_big = f_from_bytes(chunk_data[1:2], 'big')
            y_big_bit = '{:>08b}'.format(y_big)
            z_big = f_from_bytes(chunk_data[2:3], 'big')
            z_big_bit = '{:>08b}'.format(z_big)
            w_big = f_from_bytes(chunk_data[3:4], 'big')
            w_big_bit = '{:>08b}'.format(w_big)
            full = f'{x_big_bit}{y_big_bit}{z_big_bit}{w_big_bit}'
            temp = f_from_bytes(chunk_data[0:4], 'little')
            data = f_from_bytes(chunk_data[0:4], 'little')
            m = ((data & 0x3FF) / 1023 - 0.5) / 2 ** 0.5
            n = ((((data >> 10) & 0x3FF) - 0.5) / 1023) / 2 ** 0.5
            o = ((((data >> 20) & 0x3FF) - 0.5) / 1023) / 2 ** 0.5
            p = (data >> 30)

            m1 = ((data & 0x3FF) / 1023)
            n1 = ((((data >> 10) & 0x3FF)) / 1023)
            o1 = ((((data >> 20) & 0x3FF)) / 1023)
            p1 = (data >> 30) / 3
            temp_bin = '{:<032b}'.format(temp)[::-1]  # format(temp, "b").zfill(32, ) [::-1]
            n = 10
            chunks = [full[i:i + n] for i in range(0, len(full), n)]
            if len(chunks) < 4:
                debug = True
            v1 = temp & 0x3ff
            v11 = int(chunks[0][::-1], 2)  # [::-1]

            temp >>= 10
            v2 = temp & 0x3ff
            v22 = int(chunks[1][::-1], 2)  # [::-1]

            temp >>= 10
            v3 = temp & 0x3ff
            v33 = int(chunks[2][::-1], 2)  # [::-1]
            Wnormalized = (v11 / (2 ** 10 - 1), v22 / (2 ** 10 - 1), v33 / (2 ** 10 - 1))
            normalized = (m1, n1, o1)
            rest = 1 - m1 - n1 - o1
            if rest > 1 or rest < 0:
                debug = True
            vert_data_array.append(normalized)
        return vert_data_array

    def readF_10_10_10_2_signedNormalizedPackedAsUnorm(self, bin_stream, vertex_count, vertex_stride, m_v_t_index):
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
        sub_chunk_data = self.getChunkDataBy(index_block_descr['offset'].value, index_block_descr['byte width'].value)
        bin_stream = io.BytesIO(sub_chunk_data)
        f_from_bytes = int.from_bytes
        index_array = []
        for i in range(index_block_descr['count'].value):
            index = f_from_bytes(bin_stream.read(2), 'little')
            index_array.append(index)
        if index_array.__len__() < 1:
            debug = 1
        return index_array

    def export(self, export_by: ExportBy = ExportBy.MESH_LIST):
        super(RenderModelExporter, self).export()
        result = None
        if export_by == ExportBy.MESH_LIST:
            result = self._get_mesh_list()
            nodes_data = self.render_model.getBonesInfo()
            for mesh in result:
                fbx_model = FbxModel(p_skl_data=nodes_data)
                mesh.bones_data = nodes_data
                fbx_model.add(mesh)
                temp_str = self.render_model.full_filepath.split('\\')[-1].replace('.', '_')
                sub_dir = f"{temp_str}/mesh/"
                os.makedirs(f"{self.filepath_export}{sub_dir}", exist_ok=True)
                save_path = f"{self.filepath_export}{sub_dir}{mesh.name}.fbx"
                fbx_model.export(save_path, True)
            debug = True
        elif export_by == ExportBy.REGION:
            result = self._get_mesh_by_region()
            debug = True

    def _export_save(self):
        super(RenderModelExporter, self).export()
        if not self.render_model.is_loaded():
            self.render_model.load()
        self.render_model_inst = self.render_model.tag_parse.rootTagInst.childs[0]
        self.createScaleInfo()
        self.obj_render_model.name = self.render_model_inst['name'].value
        self.obj_render_model.nodes_data = self.render_model.getBonesInfo()
        mesh_resource = \
            self.render_model_inst['mesh resource groups'].childs[0]['mesh resource'].childs[0]
        self.initChunksData()
        if self.export_by_regions:
            for region in self.render_model_inst['regions'].childs:
                permutations = region['permutations'].childs
                for permutation in permutations:
                    # print("Permutation name: " + permutation['name'].value)

                    m_index_ = permutation['mesh_index'].value
                    if m_index_ == -1:
                        continue
                    fbx_model = FbxModel(p_skl_data=self.obj_render_model.nodes_data)
                    if permutation['mesh_count'].value > 1:
                        if permutation['clone_name'].value == '00000000':
                            debug = 1
                    export = False
                    temp_name = '-1'
                    mesh_name = ''
                    for m_index in range(m_index_, m_index_ + permutation['mesh_count'].value):
                        mesh = self.render_model_inst['meshes'].childs[m_index]

                        if self._chunk_data is None:
                            return
                        t_m = self.processMeshInst(mesh, mesh_resource)

                        material_path = t_m.LOD_render_data[0].parts[0].material_path
                        mesh_name = ''
                        if len(material_path.split('\\')) >= 1:
                            mesh_name += material_path.split('\\')[-1]
                        if temp_name == mesh_name:
                            continue
                        temp_name = mesh_name
                        # mesh_name = string_table.name_string.split('\\')[-2] + "." + material_path.split('\\')[-1]
                        if mesh_name == '':
                            mesh_name = "unknown mesh"
                        s_t = f"{permutation['name'].str_value}-{mesh_name}"
                        if s_t == "B21527FC-.female_osiris_techsuit_kelly":
                            debug = 1

                        if mesh_name.find(self.filterArmorCore.getString()) == -1:
                            continue

                        t_m.name = mesh_name
                        t_m.name = utils.getNamePart(t_m)
                        self.obj_render_model.meshes.append(t_m)
                        fbx_model.add(t_m)
                        export = True
                    if export:
                        temp_str = self.render_model.full_filepath.split('\\')[-1].replace('.', '_')
                        sub_dir = f"{temp_str}/{region['name'].str_value}/"
                        os.makedirs(f"{self.filepath_export}{sub_dir}", exist_ok=True)
                        save_path = f"{self.filepath_export}{sub_dir}{permutation['name'].str_value}-{mesh_name}.fbx"
                        fbx_model.export(save_path, True)
                        print(f"Saved model to {save_path}")
        else:
            filter_meshs = [7, 28, 123, 143, 220, 235, 249, 264, 275, 288, 293, 318, 326, 331, 350, 360, 402, 406, 465,
                            687, 695]
            # filter_meshs= [318]
            filter_meshs = [346]
            self.initChunksData()
            filter_by_list = True
            for m_i, mesh in enumerate(self.render_model_inst['meshes'].childs):
                if filter_by_list and not filter_meshs.__contains__(m_i):
                    continue

                if self._chunk_data is None or self._chunk_data == b'':
                    return
                t_m = self.processMeshInst(mesh, mesh_resource, m_i)

                material_path = t_m.LOD_render_data[0].parts[0].material_path
                mesh_name = ''
                if len(material_path.split('\\')) >= 1:
                    mesh_name += "."
                    mesh_name += material_path.split('\\')[-1]
                # mesh_name = string_table.name_string.split('\\')[-2] + "." + material_path.split('\\')[-1]
                if mesh_name == '':
                    mesh_name = "unknown mesh"
                print(mesh_name)

                if mesh_name.find(self.filterArmorCore.getString()) == -1:
                    continue

                if not mesh_name.__contains__(
                        'olympus_spartan_l_glove_001_s001'):  # mesh_name.find('_001_s001') == -1 or not mesh_name.find('prosthetic') == -1:
                    continue
                fbx_model = FbxModel(p_skl_data=self.obj_render_model.nodes_data)
                t_m.name = mesh_name + str(m_i)
                t_m.name = utils.getNamePart(t_m)
                self.obj_render_model.meshes.append(t_m)
                fbx_model.add(t_m)
                if self.filterArmorCore.getString() != '_':
                    item_name = self.filterArmorCore.getString()
                sub_dir = material_path.split('spartan_armor/materials/')[-1]
                sub_dir = sub_dir.replace(sub_dir.split('/')[-1], '')
                os.makedirs(f"{self.filepath_export}{sub_dir}", exist_ok=True)
                save_path = f"{self.filepath_export}{sub_dir}{t_m.name}.fbx"
                fbx_model.export(save_path, True)
                print(f"Saved model to {save_path}")

        print('end Export')

    def _get_mesh_list(self, str_filter='') -> []:
        if not self.render_model.is_loaded():
            self.render_model.load()
        if self.render_model_inst is None:
            self.render_model_inst = self.render_model.tag_parse.rootTagInst.childs[0]
        mesh_resource = \
            self.render_model_inst['mesh resource groups'].childs[0]['mesh resource'].childs[0]
        self.createScaleInfo()
        temp_mesh_s = self.render_model_inst['meshes'].childs
        self.initChunksData()
        mesh_list = []
        if self._chunk_data is None:
            return mesh_list

        for i, mesh in enumerate(temp_mesh_s):
            if False and i != 31:
                continue
            t_m = self.processMeshInst(mesh, mesh_resource)
            file_name = self.render_model.in_game_path.split('\\')[-1].replace('.', '_')
            t_m.name = f"{file_name}_mesh_{i}"
            mesh_list.append(t_m)

        return mesh_list

    def debugAnalyzeMeshInfo(self):

        if not self.render_model.is_loaded():
            self.render_model.load()
        if self.render_model_inst is None:
            self.render_model_inst = self.render_model.tag_parse.rootTagInst.childs[0]
        mesh_resource = None
        try:
            mesh_resource = \
                self.render_model_inst['mesh resource groups'].childs[0]['mesh resource'].childs[0]
        except:
            return {}

        temp_mesh_s = self.render_model_inst['meshes'].childs
        # self.initChunksData()
        result = self.analyzeMeshResource()
        assert result[0]['len_index_blocks'] >= result[0]['len_array_4']
        self.index_block = 0
        self.index_block_dict = {}
        self.vertext_block = 0
        self.vertext_block_dict = {}
        self.lod_count = 0
        self.lod_unic_count = 0
        self.mesh_lod_count = []
        mesh_unic = 0
        mesh_no_unic = 0
        self.Remap_Table = {}
        self.map_part_type = {}
        for i, mesh in enumerate(temp_mesh_s):
            t_m = self.analyzeMeshInst(mesh, mesh_resource, i)
            file_name = self.render_model.in_game_path.split('\\')[-1].replace('.', '_')
            t_m.name = f"{file_name}_mesh_{i}"
            if mesh['clone_index'].value != -1:
                mesh_unic += 1
            else:
                mesh_no_unic += 1
        print(str(result[4].keys()))
        print("Fin de análice")

    def _get_mesh_by_region(self, regions: [], str_filter='') -> {}:
        if not self.render_model.is_loaded():
            self.render_model.load()
        if self.render_model_inst is None:
            self.render_model_inst = self.render_model.tag_parse.rootTagInst.childs[0]
        mesh_resource = \
            self.render_model_inst['mesh resource groups'].childs[0]['mesh resource'].childs[0]
        self.createScaleInfo()
        temp_mesh_s = self.render_model_inst['meshes'].childs
        self.initChunksData()
        result = {}
        if self._chunk_data is None:
            return result

        for region in self.render_model_inst['regions'].childs:

            if len(regions) != 0 and not (region['name'].value in regions):
                continue
            permutations = region['permutations'].childs
            result_per = {}
            for permutation in permutations:
                # print("Permutation name: " + permutation['name'].value)

                m_index_ = permutation['mesh_index'].value
                if m_index_ == -1:
                    continue
                result_per[permutation['name'].value] = []
                mesh_list = []
                for m_index in range(m_index_,
                                     m_index_ + permutation['mesh_count'].value):
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

                    t_m.name = mesh_name
                    t_m.name = utils.getNamePart(t_m)
                    if not t_m.name.__contains__(
                            str_filter):  # False and olympus_spartan_l_armup_001_s001_2_lod_0 'olympus_spartan_l_glove_001_s001'
                        continue
                    print(mesh_name)
                    result_per[permutation['name'].value].append(t_m)

            result[region['name'].value] = result_per
        return result

    # J:\Games\Halo Infinite Stuf\Web-Json\seasson 2\info_007-000-emile-a239-ki-0903655e.json
    def overridesRegions(self, regions, to_override):
        for to_override_region in to_override:
            for i, region in enumerate(regions):
                if to_override_region['RegionId'] == region['RegionId']:
                    regions[i] = to_override_region
                    break

    def getMeshListByJson(self, data) -> []:
        array_info = data['CoreRegionData']['BaseRegionData']
        """
        self.overridesRegions(array_info,data['CoreRegionData']['BodyTypeSmallOverrides'])
        self.overridesRegions(array_info,data['CoreRegionData']['BodyTypeLargeOverrides'])
        self.overridesRegions(array_info,data['CoreRegionData']['BodyTypeLargeOverrides'])

        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticLeftArmOverrides']['Full'])
        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticLeftArmOverrides']['Half'])
        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticLeftArmOverrides']['Extremity'])

        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticRightArmOverrides']['Full'])
        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticRightArmOverrides']['Half'])
        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticRightArmOverrides']['Extremity'])

        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticLeftLegOverrides']['Full'])
        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticLeftLegOverrides']['Half'])
        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticLeftLegOverrides']['Extremity'])

        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticRightLegOverrides']['Full'])
        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticRightLegOverrides']['Half'])
        self.overridesRegions(array_info,data['CoreRegionData']['ProstheticRightLegOverrides']['Extremity'])
        """
        if not self.render_model.is_loaded():
            self.render_model.load()
        if self.render_model_inst is None:
            self.render_model_inst = self.render_model.tag_parse.rootTagInst.childs[0]
        mesh_resource = \
            self.render_model_inst['mesh resource groups'].childs[0]['mesh resource'].childs[0]
        self.createScaleInfo()
        temp_mesh_s = self.render_model_inst['meshes'].childs
        temp_mesh_r = self.render_model_inst['regions'].childs
        self.initChunksData()

        if self._chunk_data is None:
            return []
        mesh_list = []
        for region in array_info:
            region_id = region['RegionId']['m_identifier']
            permutation_id = region['PermutationId']['m_identifier']
            style_id_override = region['StyleIdOverride']['m_identifier']
            if region_id == -1:
                continue
            region_to_export = None
            permutation_to_export = None
            for render_model_region in temp_mesh_r:
                if render_model_region['name'].int_value == region_id:
                    region_to_export = render_model_region
                    for permutation in render_model_region['permutations'].childs:
                        if permutation['name'].int_value == permutation_id:
                            permutation_to_export = permutation
                            break
                    break
            if permutation_to_export is None:
                continue
            region_name = region_to_export['name'].str_value
            permu_name = permutation_to_export['name'].str_value
            per_mesh_index_1 = permutation_to_export['mesh index'].value
            if per_mesh_index_1 == -1:
                continue
            temp_name = '-1'

            m_count = permutation['mesh count'].value
            mesh_in_permutation = temp_mesh_s[per_mesh_index_1:per_mesh_index_1 + m_count]
            for m_index, mesh in enumerate(mesh_in_permutation):
                #mesh = temp_mesh_s[m_index]

                t_m = self.processMeshInst(mesh, mesh_resource)

                material_path = t_m.LOD_render_data[0].parts[0].material_path

                mesh_name = f'{region_name}_{permu_name}_mesh_{m_index}_'

                if len(material_path.split('\\')) >= 1:
                    mesh_name += material_path.split('\\')[-1]


                """    
                if temp_name == mesh_name:
                    continue
                """
                if mesh_name.__contains__('hip_gear'):
                    debug = True

                if mesh_name == '':
                    mesh_name = "unknown mesh"

                temp_name = mesh_name
                temp_mesh = mesh

                t_m.name = mesh_name
                t_m.name = utils.getNamePart(t_m)
                """
                if t_m.name.__contains__(
                        'hair') \
                        or t_m.name.__contains__('beard')\
                        or t_m.name.__contains__('lashes'):

                    # False and olympus_spartan_l_armup_001_s001_2_lod_0
                    continue
                """
                print(mesh_name)
                mesh_list.append(t_m)
                if m_count != 1:
                    debug = True
                    continue
                    sub_mesh = divmod(m_count, 2)
                    #assert sub_mesh[1] == 0, m_count
                    if m_count > 1:
                        if m_index ==1:
                            break
                    else:
                        if m_index ==1:
                            break

        return mesh_list





    def getMeshListByVariant(self, variant, model_runtime_regions) -> []:
        if not self.render_model.is_loaded():
            self.render_model.load()
        if self.render_model_inst is None:
            self.render_model_inst = self.render_model.tag_parse.rootTagInst.childs[0]
        mesh_resource = \
            self.render_model_inst['mesh resource groups'].childs[0]['mesh resource'].childs[0]
        self.createScaleInfo()
        temp_mesh_s = self.render_model_inst['meshes'].childs
        temp_mesh_r = self.render_model_inst['regions'].childs
        self.initChunksData()

        if self._chunk_data is None:
            return []
        mesh_list = []
        regions = variant['regions'].childs
        runtime_v_r_indices = variant['runtime variant region indices'].childs
        for r_r_index in runtime_v_r_indices:
            if r_r_index.value ==-1:
                continue

            model_runtime_region = model_runtime_regions[r_r_index.value]
            region = regions[r_r_index.value]
            region_name = region['region name']

            rn = temp_mesh_r[region['runtime region index'].value]
            temp_mesh_r_i = rn['permutations'].childs
            assert rn['name'].value == region_name.value
            assert len(region['permutations'].childs) == 1
            for per in region['permutations'].childs:

                per_mesh_index = per['runtime permutation index'].value

                if per_mesh_index != -1 and not (temp_mesh_r_i is None):
                    permutation = temp_mesh_r_i[per_mesh_index]
                    assert per['permutation name'].value == permutation['name'].value
                    per_mesh_index_1 = permutation['mesh index'].value
                    if per_mesh_index_1 == -1:
                        continue
                    temp_name = '-1'

                    m_count = permutation['mesh count'].value
                    mesh_in_permutation = temp_mesh_s[per_mesh_index_1:per_mesh_index_1+m_count]
                    #for m_index in range(per_mesh_index_1,
                    #                     per_mesh_index_1 + m_count):
                    for m_index, mesh in enumerate(mesh_in_permutation):
                        #mesh = temp_mesh_s[m_index]

                        t_m = self.processMeshInst(mesh, mesh_resource)

                        material_path = t_m.LOD_render_data[0].parts[0].material_path

                        mesh_name = permutation['name'].str_value+'_'+region_name.str_value+f'_mesh_{m_index}_'

                        if len(material_path.split('\\')) >= 1:
                            mesh_name += material_path.split('\\')[-1]


                        """    
                        if temp_name == mesh_name:
                            continue
                        """
                        if mesh_name.__contains__('hip_gear'):
                            debug = True

                        if mesh_name == '':
                            mesh_name = "unknown mesh"

                        temp_name = mesh_name
                        temp_mesh = mesh

                        t_m.name = mesh_name
                        t_m.name = utils.getNamePart(t_m)
                        """
                        if t_m.name.__contains__(
                                'hair') \
                                or t_m.name.__contains__('beard')\
                                or t_m.name.__contains__('lashes'):

                            # False and olympus_spartan_l_armup_001_s001_2_lod_0
                            continue
                        """
                        print(mesh_name)
                        mesh_list.append(t_m)
                        if m_count != 1:
                            debug = True
                            continue
                            sub_mesh = divmod(m_count, 2)
                            #assert sub_mesh[1] == 0, m_count
                            if m_count > 1:
                                if m_index ==1:
                                    break
                            else:
                                if m_index ==1:
                                    break
                else:
                    continue
        return mesh_list

    def analyzeMeshResource(self):
        result = []
        return result

    def initChunksData(self):
        if self._chunk_data is None:
            mesh_resource = \
                self.render_model_inst['mesh resource groups'].childs[0]['mesh resource'].childs[0]
            self._chunk_data = b""
            nChunk = 0
            ch_offset = 0
            for nChunk, chunk in enumerate(mesh_resource['Streaming Chunks'].childs):
                chunk_path = f"{self.render_model.full_filepath}[{nChunk}_mesh_resource.chunk{nChunk}]"
                temp_len = chunk['buffer end'].value - chunk['buffer start'].value
                self._chunk_data_map[ch_offset] = Chunk(chunk_path, temp_len)
                ch_offset += temp_len
                self._chunk_data += bytes(temp_len)
            assert mesh_resource['Streaming Buffers'].childs[0]['buffer size'].value == len(self._chunk_data)
            print(f"Read {nChunk} chunks ({hex(len(self._chunk_data))} bytes)")

    def initChunksDataSave(self):
        if self._chunk_data is None:
            chunk_data_map: {str: []} = {}
            more_chunks = True
            self._chunk_data = b""
            nChunk = 0
            ch_offset = 0
            while more_chunks:
                try:
                    chunk_path = f"{self.render_model.full_filepath}[{nChunk}_mesh_resource.chunk{nChunk}]"
                    temp_len = os.path.getsize(chunk_path)
                    self._chunk_data_map[ch_offset] = Chunk(chunk_path, temp_len)

                    ch_offset += temp_len
                    self._chunk_data += bytes(temp_len)
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

            print(f"Read {nChunk} chunks ({hex(len(self._chunk_data))} bytes)")

    def getChunkDataBy(self, offset, size) -> bytes:
        if self._chunk_data[offset:offset + size] != bytes(size):
            return self._chunk_data[offset:offset + size]

        keys = list(self._chunk_data_map.keys())
        init_key = 0
        if len(keys)==0:
            raise Exception("EmptyData")
        if keys.__contains__(offset):
            init_key = keys.index(offset)
        else:
            ki = 0
            while offset > keys[ki]:
                ki += 1
                if ki == len(keys) - 1:
                    break
                if ki > len(keys) - 1:
                    ki-= 1
                    break

            temp_ki = keys[ki]
            temp_off = temp_ki - offset
            if ki > 0:
                temp_ki_minus1 = keys[ki - 1]
                init_key = ki - 1

        key_to_read = [init_key]
        ki = init_key
        temp_off = offset - keys[init_key]
        total_bytes = self._chunk_data_map[keys[ki]].len - temp_off
        while size > total_bytes:
            ki += 1
            key_to_read.append(ki)
            total_bytes += self._chunk_data_map[keys[ki]].len

        data_add = b''
        for key in key_to_read:
            if self._chunk_data_map[keys[key]].data == b'':
                with open(self._chunk_data_map[keys[key]].path, 'rb') as ch_file:
                    self._chunk_data_map[keys[key]].data = ch_file.read()
                    ch_file.close()
            data_add += self._chunk_data_map[keys[key]].data

        data_return = data_add[temp_off:temp_off + size]
        if data_return != self._chunk_data[offset:offset + size]:
            debug = True
        # assert data_return==self._chunk_data[offset:offset+size], f'chunk leido incorrectamente'
        verif_len = len(self._chunk_data)
        self._chunk_data = self._chunk_data[0:offset] + data_return + self._chunk_data[offset + size:]
        assert len(self._chunk_data) == verif_len, 'se modifico mal el _chunk data'
        return self._chunk_data[offset:offset + size]

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
        if self._chunk_data is None or self._chunk_data == b'':
            chunk_data_map: {str: []} = {}
            more_chunks = True
            self._chunk_data = b""
            nChunk = 0
            ch_offset = 0
            while more_chunks:
                try:
                    chunk_path = f"{self.render_model.full_filepath}[{nChunk}_mesh_resource.chunk{nChunk}]"

                    # self._chunk_data_map[ch_offset] = Chunk(chunk_path, temp_len)
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
        obj_mesh.clone_index = mesh["clone index"].value
        obj_mesh.mesh_flags = mesh["mesh flags"].options
        obj_mesh.rigid_node_index = mesh["rigid node index"].value
        m_v_t_index = mesh["vertex type"].selected_index
        obj_mesh.vertex_type = m_v_t_index
        obj_mesh.vert_type = m_v_t_index
        obj_mesh.use_dual_quat = mesh["use dual quat"].value
        obj_mesh.index_buffer_type = mesh["index buffer type"].selected_index
        obj_mesh.clone_index = mesh["clone index"].value

        for lod_i, lod in enumerate(mesh['LOD render data'].childs):
            if not (self.minLOD <= lod_i <= self.maxLOD):
                continue
            obj_lod = ObjLOD(obj_mesh)
            vertx_blocks = {}
            min_offset = -1
            max_offset = -1
            size_sum = 0
            last_size = -1
            s_key = ''
            for xi, x in enumerate(lod['vertex buffer indices'].childs):
                temp_vert_index_block = x.value
                if temp_vert_index_block != -1:
                    vertx_block_descr = mesh_resource['pc vertex buffers'].childs[temp_vert_index_block]
                    vertex_type_ = vertx_block_descr['usage'].selected
                    vertex_buffers_usage = vertx_block_descr['usage'].selected_index
                    vertex_type_index = vertx_block_descr['format'].selected_index
                    offset = vertx_block_descr['offset'].value
                    size = vertx_block_descr['byte width'].value
                    # print(f"{m_i}-{lod_i}-{vertex_type_}")
                    # self.fillChunkDataArray(offset, size)
                    s_key += str(vertex_type_) + f'-{vertx_block_descr["format"].selected}-'

                    if vertex_buffers_usage == PcVertexBuffersUsage.BlendIndices1:
                        debug = True

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
                    obj_lod.setVertBufferArray(vertex_buffers_usage, vertx_data)
            s_t = (max_offset - min_offset) + last_size
            main_key = str(mesh["vertex type"].selected) + '<->' + str(m_v_t_index)

            fillDebugDict(main_key, s_key, vertx_data_arrays)
            if s_t == size_sum:
                debug = 1
            else:
                debug = 1
            index_buffer_index = lod['index buffer index'].value

            if index_buffer_index == -1:
                continue
            else:
                index_block_descr = mesh_resource['pc index buffers'].childs[index_buffer_index]
            s_t_1 = max_offset + last_size
            if index_block_descr['offset'].value == s_t_1:
                debug = 1
            else:
                debug = 1
            obj_lod.lod_flags = lod['lod flags'].options
            obj_lod.lod_render_flags = lod['lod render flags'].options
            obj_lod.index_buffer_index = self.readIndexBlock(index_block_descr)
            obj_lod.vertex_buffer_indices = vertx_blocks

            for part in lod['parts'].childs:
                obj_part = ObjPart()
                path_mat = part['material index'].extra_data['path']
                obj_part.index_start = part['index start'].value
                obj_part.part_type = part['part type'].value
                obj_part.index_count = part['index count'].value
                obj_part.budget_vertex_count = part['budget vertex count'].value
                obj_part.part_flags = part['part flags'].options
                obj_part.material_index = part['material index'].value
                obj_part.mat_string = path_mat
                obj_part.material_path = path_mat
                obj_lod.parts.append(obj_part)

            for subpart in lod['subparts'].childs:
                obj_subpart = ObjSubPart()
                obj_subpart.index_start = subpart['index start'].value
                obj_subpart.index_count = subpart['index count'].value
                obj_subpart.part_index = subpart['part index'].value
                obj_subpart.budget_vertex_count = subpart['budget vertex count'].value
                obj_lod.sub_parts.append(obj_subpart)

            obj_mesh.LOD_render_data.append(obj_lod)
        return obj_mesh

    def analyzeMeshInst(self, mesh, mesh_resource, m_i=-1) -> ObjMesh:
        obj_mesh = ObjMesh()
        obj_mesh.clone_index = mesh["clone index"].value
        obj_mesh.mesh_flags = mesh["mesh flags"].options
        obj_mesh.rigid_node_index = mesh["rigid node index"].value
        m_v_t_index = mesh["vertex type"].selected_index
        obj_mesh.vertex_type = m_v_t_index
        obj_mesh.vert_type = m_v_t_index
        obj_mesh.use_dual_quat = mesh["use dual quat"].value
        obj_mesh.index_buffer_type = mesh["index buffer type"].selected_index
        obj_mesh.clone_index = mesh["clone index"].value

        if mesh["clone index"].value != -1:
            temp_mesh_s = self.render_model_inst['meshes'].childs
            clone_mesh = temp_mesh_s[mesh["clone index"].value]
            assert mesh["LOD render data"].childrenCount == clone_mesh["LOD render data"].childrenCount
            assert mesh["mesh flags"].options == clone_mesh["mesh flags"].options
            assert mesh["rigid node index"].value == clone_mesh["rigid node index"].value
            assert mesh["vertex type"].selected_index == clone_mesh["vertex type"].selected_index
            assert mesh["use dual quat"].value == clone_mesh["use dual quat"].value
            assert mesh["index buffer type"].selected_index == clone_mesh["index buffer type"].selected_index
            assert mesh["pca mesh index"].value == clone_mesh["pca mesh index"].value
            assert mesh["vertex keys"].childrenCount == clone_mesh["vertex keys"].childrenCount
            assert mesh["optional LOD volume index"].value == clone_mesh["optional LOD volume index"].value

            assert mesh["lod state cache slot"].value == clone_mesh["lod state cache slot"].value

            if not mesh["Procedural Deformation Remap Table"].value == clone_mesh[
                "Procedural Deformation Remap Table"].value:
                debug = 1
        self.Remap_Table[mesh["Procedural Deformation Remap Table"].value] = 1

        info_item_array_3 = mesh_resource['Streaming Meshes'].childs[m_i]
        str_hex = str(mesh_resource['Streaming Meshes'].content_entry.bin_datas_hex[m_i])
        sub_str = str_hex[10:48]
        assert str_hex[0:8] == 'ffffffff'
        assert sub_str == 'bcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbc'
        if obj_mesh.use_dual_quat == 1:
            if info_item_array_3['int byte'].value + obj_mesh.use_dual_quat != 0:
                asd = 1

        if info_item_array_3['int byte'].value != mesh["index_buffer_type"].selected_index:
            asd = 1
        if not self.mesh_lod_count.__contains__(len(mesh['LOD_render_data'].childs)):
            self.mesh_lod_count.append(len(mesh['LOD_render_data'].childs))

        for lod_i, lod in enumerate(mesh['LOD_render_data'].childs):
            self.lod_count += 1
            for t_part in lod['parts'].childs:
                self.map_part_type[t_part['part_type'].value] = 1
            for sub_part in lod['subparts'].childs:
                self.map_part_type[sub_part['part_type'].value] = 1
            if mesh["clone_index"].value == -1:
                self.lod_unic_count += 1
            if False and not (self.minLOD <= lod_i <= self.maxLOD):
                continue
            obj_lod = ObjLOD(obj_mesh)
            vertx_blocks = {}
            min_offset = -1
            max_offset = -1
            size_sum = 0
            last_size = -1
            s_key = ''
            for xi, x in enumerate(lod['vertex_buffer_indices'].childs):
                temp_vert_index_block = x.value
                if temp_vert_index_block != -1:
                    self.vertext_block += 1

                    if self.vertext_block_dict.keys().__contains__(temp_vert_index_block):
                        clone_i = mesh['clone_index'].value
                        assert clone_i != -1, 'mesh clone reuse vertext block'
                        assert f'{clone_i}-{xi}-{temp_vert_index_block}' == self.vertext_block_dict[
                            temp_vert_index_block], 'mesh clone reuse vertext block'
                    else:
                        assert mesh['clone_index'].value == -1, 'mesh clone reuse vertext block'
                        self.vertext_block_dict[temp_vert_index_block] = f'{m_i}-{xi}-{temp_vert_index_block}'

                    vertx_block_descr = mesh_resource['pc vertex buffers'].childs[temp_vert_index_block]
                    vertex_type_ = vertx_block_descr['vertex_type'].selected
                    vertex_type_index = vertx_block_descr['vertex_type'].selected_index
                    offset = vertx_block_descr['offset'].value
                    size = vertx_block_descr['size'].value
                    # print(f"{m_i}-{lod_i}-{vertex_type_}")
                    # self.fillChunkDataArray(offset, size)
                    s_key += str(vertex_type_) + f'-{vertx_block_descr["way_to_read_type"].value}-'
                    assert vertx_block_descr["unknown_off_10_12"].value == -17220, "unknown_off_10_12"
                    assert vertx_block_descr["unknown_off_28_32"].value == 32, "unknown_off_28_32"
                    assert vertx_block_descr["unknown_off_32_36"].value == 0, "unknown_off_32_36"

                    assert vertx_block_descr["unknown_array_off_36_56"].childrenCount == 0, "unknown_array_off_36_56"
                    assert vertx_block_descr["unknown_off_56_60"].value == 0, "unknown_off_56_60"
                    assert vertx_block_descr["vertex_buffer_index"].value == xi, "vertex_buffer_index"
                    assert vertx_block_descr["vertex_type"].selected_index == xi, "vertex_type"
                    assert vertx_block_descr["vertex_type"].selected_index == vertx_block_descr[
                        "vertex_buffer_index"].value == xi, "vertex_buffer_index <-> vertex_type"
                    assert vertx_block_descr["unknown_off_64_68"].value == 0, "unknown_off_64_68"
                    assert vertx_block_descr["unknown_off_68_72"].value == 0, "unknown_off_68_72"
                    assert vertx_block_descr["unknown_off_72_76"].value == 0, "unknown_off_72_76"
                    assert vertx_block_descr["unknown_off_76_80"].value == 0, "unknown_off_76_80"
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
                    vertx_data = []  # self.readVertBlockDesc(vertx_block_descr, m_v_t_index)
                    vertx_blocks[vertex_type_] = vertx_data
                    # obj_lod.setVertBufferArray(vertex_type_index, vertx_data)
            s_t = (max_offset - min_offset) + last_size
            main_key = str(mesh["vertex_type"].selected) + '<->' + str(m_v_t_index)

            fillDebugDict(main_key, s_key, vertx_data_arrays)
            if s_t == size_sum:
                debug = 1
            else:
                debug = 1
            index_buffer_index = lod['index_buffer_index'].value

            if index_buffer_index == -1:
                continue
            else:
                index_block_descr = mesh_resource['pc index buffers'].childs[index_buffer_index]
                self.index_block += 1
                if self.index_block_dict.keys().__contains__(index_buffer_index):
                    debug = True
                    assert mesh['clone_index'].value != -1, 'mesh clone reuse index block'
                else:
                    assert mesh['clone_index'].value == -1, 'mesh clone reuse index block'
                self.index_block_dict[index_buffer_index] = 1

            s_t_1 = max_offset + last_size
            if index_block_descr['offset'].value == s_t_1:
                debug = 1
            else:
                debug = 1
            obj_lod.lod_flags = lod['lod_flags'].options
            obj_lod.lod_render_flags = lod['lod_render_flags'].options
            # obj_lod.index_buffer_index = self.readIndexBlock(index_block_descr)
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
        for compression_info in self.render_model_inst['compression info'].childs:
            obj_compression_inf = ObjCompressionInfo()
            obj_compression_inf.compression_flags = compression_info['compression flags']
            obj_compression_inf.scale["model_scale"] = [
                [compression_info['position bounds 0'].x,
                 compression_info['position bounds 0'].y,
                 compression_info['position bounds 0'].y - compression_info['position bounds 0'].x],
                [compression_info['position bounds 0'].z,
                 compression_info['position bounds 1'].x,
                 compression_info['position bounds 1'].x - compression_info['position bounds 0'].z],
                [compression_info['position bounds 1'].y,
                 compression_info['position bounds 1'].z,
                 compression_info['position bounds 1'].z - compression_info['position bounds 1'].y],
            ]

            obj_compression_inf.scale["uv0_scale"] = [
                [compression_info["texcoord bounds 0"].x, compression_info["texcoord bounds 0"].y,
                 compression_info["texcoord bounds 0"].y - compression_info["texcoord bounds 0"].x],
                [compression_info["texcoord bounds 1"].x, compression_info["texcoord bounds 1"].y,
                 compression_info["texcoord bounds 1"].y - compression_info["texcoord bounds 1"].x],
            ]

            obj_compression_inf.scale["uv1_scale"] = [
                [compression_info["texcoord bounds2 0"].x, compression_info["texcoord bounds2 0"].y,
                 compression_info["texcoord bounds2 0"].y - compression_info["texcoord bounds2 0"].x],
                [compression_info["texcoord bounds2 1"].x, compression_info["texcoord bounds2 1"].y,
                 compression_info["texcoord bounds2 1"].y - compression_info["texcoord bounds2 1"].x],
            ]

            obj_compression_inf.scale["uv2_scale"] = [
                [compression_info["texcoord bounds3 0"].x, compression_info["texcoord bounds3 0"].y,
                 compression_info["texcoord bounds3 0"].y - compression_info["texcoord bounds3 0"].x],
                [compression_info["texcoord bounds3 1"].x, compression_info["texcoord bounds3 1"].y,
                 compression_info["texcoord bounds3 1"].y - compression_info["texcoord bounds3 1"].x],
            ]
            self.obj_render_model.render_geometry.compression_info.append(obj_compression_inf)

    def createScaleInfo_save(self):
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
