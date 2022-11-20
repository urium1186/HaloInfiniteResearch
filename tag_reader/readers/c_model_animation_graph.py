import io
import struct


from tag_reader.readers.base_template import BaseTemplate


class ModelAnimationGraph(BaseTemplate):
    def __init__(self, filename):
        super().__init__(filename, 'jmad')
        self.json_str_base = '{}'

    def load(self):
        super().load()

    def toJson(self):
        super().toJson()

    def onInstanceLoad(self, instance):
        super(ModelAnimationGraph, self).onInstanceLoad(instance)


    def readAnimationFuctionData(self, animation, bin_data=None):
        if not animation['name'].str_value.__contains__("menu:stance"):
            return
            #pass

        tag_resource_groups = self.first_child['tag resource groups'].childs
        resource_group = tag_resource_groups[animation['resource group'].value]
        resource_member_index = animation['resource member index'].value
        group_member = resource_group['tag_resource'].childs[0]['group_members'].childs[resource_member_index]
        data_sizes = {
            'static_node_flags': group_member['static_node_flags'].value,
            'animated_node_flags': group_member['animated_node_flags'].value,
            'movement_data': group_member['movement_data'].value,
            'pill_offset_data': group_member['pill_offset_data'].value,
            'default_data': group_member['default_data'].value,
            'uncompressed_data': group_member['uncompressed_data'].value,
            'compressed_data': group_member['compressed_data'].value,
            'blend_screen_data': group_member['blend_screen_data'].value,
            'object_space_offset_data': group_member['object_space_offset_data'].value,
            'ik_chain_event_data': group_member['ik_chain_event_data'].value,
            'ik_chain_control_data': group_member['ik_chain_control_data'].value,
            'ik_chain_pole_vector_data': group_member['ik_chain_pole_vector_data'].value,
            'uncompressed_object_space_data': group_member['uncompressed_object_space_data'].value,
            'fik_anchor_data': group_member['fik_anchor_data'].value,
            'uncompressed_object_space_node_flags': group_member['uncompressed_object_space_node_flags'].value,
            'compressed_event_curve': group_member['compressed_event_curve'].value,
            'compressed_static_pose': group_member['compressed_static_pose'].value,
            'user_parameter': group_member['user_parameter'].value,
        }
        if bin_data is None:
            animation_data = group_member['animation_data']
            animation_data.readBinData()
            bin_data = animation_data.bin_data

        bin_stream = io.BytesIO(bin_data)
        data_bins = {
            'static_node_flags': bin_stream.read(group_member['static_node_flags'].value),
            'animated_node_flags': bin_stream.read(group_member['animated_node_flags'].value),
            'movement_data': bin_stream.read(group_member['movement_data'].value),
            'pill_offset_data': bin_stream.read(group_member['pill_offset_data'].value),
            'default_data': bin_stream.read(group_member['default_data'].value),
            'uncompressed_data': bin_stream.read(group_member['uncompressed_data'].value),
            'compressed_data': bin_stream.read(group_member['compressed_data'].value),
            'blend_screen_data': bin_stream.read(group_member['blend_screen_data'].value),
            'object_space_offset_data': bin_stream.read(group_member['object_space_offset_data'].value),
            'ik_chain_event_data': bin_stream.read(group_member['ik_chain_event_data'].value),
            'ik_chain_control_data': bin_stream.read(group_member['ik_chain_control_data'].value),
            'ik_chain_pole_vector_data': bin_stream.read(group_member['ik_chain_pole_vector_data'].value),
            'uncompressed_object_space_data': bin_stream.read(group_member['uncompressed_object_space_data'].value),
            'fik_anchor_data': bin_stream.read(group_member['fik_anchor_data'].value),
            'uncompressed_object_space_node_flags': bin_stream.read(group_member['uncompressed_object_space_node_flags'].value),
            'compressed_event_curve': bin_stream.read(group_member['compressed_event_curve'].value),
            'compressed_static_pose': bin_stream.read(group_member['compressed_static_pose'].value),
            'user_parameter': bin_stream.read(group_member['user_parameter'].value),
        }
        rest_in_pos = bin_stream.tell()
        rest = animation_data.byteLengthCount-rest_in_pos
        assert rest == 0

        bin_stream.seek(0)

        self.readAnimatedNodeFlags(data_bins['animated_node_flags'], animation['frame count'].value, animation['node count'].value)

        deug = True


    def readAnimatedNodeFlags(self, bin_data, frame_count, node_count):
        if len(bin_data) == 0:
            return
        bin_stream = io.BytesIO(bin_data)
        bin_hex = bin_data.hex()

        sh_1 = struct.unpack('h', bin_stream.read(2))[0]
        sh_2 = struct.unpack('h', bin_stream.read(2))[0]

        int_1 = struct.unpack('i', bin_stream.read(4))[0]

        float_1 = struct.unpack('f', bin_stream.read(4))[0]
        float_2 = struct.unpack('f', bin_stream.read(4))[0]

        int_2 = struct.unpack('i', bin_stream.read(4))[0]
        int_3 = struct.unpack('i', bin_stream.read(4))[0]
        int_4 = struct.unpack('i', bin_stream.read(4))[0]
        int_5 = struct.unpack('i', bin_stream.read(4))[0]



        if  sh_1 == 10:
            header_size = 36
            char_1 = struct.unpack('4s', bin_stream.read(4))[0]
            array_address_1 = []
            datas = []
            for i in range(sh_2):
                int_n = struct.unpack('i', bin_stream.read(4))[0]
                array_address_1.append(int_n + header_size)
            assert int_n <= int_2
            current_pos_1 = bin_stream.tell()
            for i in range(sh_2):
                sub_bin =  bin_stream.read(int_4)
                if int_4 == 36:
                    bin_stream_temp = io.BytesIO(sub_bin)
                    data_temp = [
                        struct.unpack('h', bin_stream_temp.read(2))[0],
                        struct.unpack('i', bin_stream_temp.read(4))[0],
                        bin_stream_temp.read(6).hex(),
                        struct.unpack('i', bin_stream_temp.read(4))[0],
                        bin_stream_temp.read(6).hex(),
                        struct.unpack('i', bin_stream_temp.read(4))[0],
                        bin_stream_temp.read(6).hex(),
                        struct.unpack('i', bin_stream_temp.read(4))[0],
                    ]
                    bin_stream_temp.close()
                    datas.append(data_temp)
            current_pos_2 = bin_stream.tell()
            array_address_2 = []
            for o in range(int_1):
                int_m = struct.unpack('i', bin_stream.read(4))[0]
                array_address_2.append(int_m+header_size)

            debug = True
        elif sh_1 == 3:
            arra_1 = []
            arra_2 = []
            int_6 = struct.unpack('i', bin_stream.read(4))[0]
            int_7 = struct.unpack('i', bin_stream.read(4))[0]
            int_8 = struct.unpack('i', bin_stream.read(4))[0]
            int_9 = struct.unpack('i', bin_stream.read(4))[0]

            temp = divmod(int_6, frame_count)
            assert temp[0] == 4 and temp[1] == 0
            temp1 = divmod(int_4, frame_count)
            assert temp1[0] == 8 and temp1[1] == 0
            temp2 = divmod(int_5, frame_count)
            assert temp2[0] == 12 and temp2[1] == 0
            if sh_2 != 0:
                for k in range(sh_2):
                    arra_1_temp= bin_stream.read(int_4)
                    arra_1_array = []
                    bin_stream_temp = io.BytesIO(arra_1_temp)
                    for j in range(frame_count):

                        arra_1_array.append([
                            struct.unpack('d', bin_stream_temp.read(8))[0],
                        ])
                    bin_stream_temp.close()
                    arra_1.append(arra_1_array)

                assert (int_2 - 48)/sh_2 == int_4
            if int_1!=0:
                test = bin_stream.tell()
                assert test  == int_2
                bin_stream.seek(int_2)

                for j in range(int_1):
                    bin_temp = bin_stream.read(int_5)
                    bin_temp_hex =bin_temp.hex()
                    arra_2_array = []
                    bin_stream_temp = io.BytesIO(bin_temp)
                    for j in range(frame_count):
                        arra_2_array.append([
                            struct.unpack('f', bin_stream_temp.read(4))[0],
                            struct.unpack('f', bin_stream_temp.read(4))[0],
                            struct.unpack('f', bin_stream_temp.read(4))[0],
                        ])
                    bin_stream_temp.close()
                    try:
                        arra_2.append(arra_2_array)
                    except:
                        debug = True


                assert int_5==(int_3 - int_2) / int_1

            debug = True
