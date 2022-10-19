import io
import json
import math
import os
import struct

from typing.io import BinaryIO

from commons.constant import ADDRESS_UNSET
from commons.logs import Log
from tag_reader.headers.data_reference_table import DataReference

#from tag_reader.readers.reader_factory import ReaderFactory
from tag_reader.tag_instance import TagInstance
from tag_reader.tag_reader_utils import getStringsByRef, readStringInPlace
from tag_reader.tag_layouts import TagLayouts
from tag_reader.var_names import getStrInMmr3Hash, getMmr3HashFromInt, TAG_NAMES


class DebugDataBlock(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.comment = tag.N
        pass

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        self.comment = self.tagDef.N

    def toJson(self):
        json_obj = super(DebugDataBlock, self).toJson()
        json_obj['comment'] = self.comment
        return json_obj


class Comment(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.comment = tag.N
        pass

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        self.comment = self.tagDef.N

    def toJson(self):
        return self.comment


class ArrayFixLen(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.comment = tag.N
        pass

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        self.comment = self.tagDef.N
        for entry in self.tagDef.B.keys():
            temp = tagInstanceFactoryCreate(tag=self.tagDef.B[entry], addressStart=self.addressStart,
                                            offset=entry + self.offset)
            temp.readIn(f, header)
            self.childs.append(temp)

    def toJson(self):
        json_obj = super(ArrayFixLen, self).toJson()
        json_obj['comment'] = self.comment
        return json_obj


class GenericBlock(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.comment = tag.N
        self.binary_data = None
        pass

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        self.comment = self.tagDef.N
        self.binary_data = f.read(self.tagDef.S)

    def toJson(self):
        json_obj = super(GenericBlock, self).toJson()
        json_obj['comment'] = self.comment
        json_obj['binary_data'] = self.binary_data.hex()
        return json_obj


class TagStructData(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.generateEntry = tag.P['generateEntry']
        pass

    def hasMoreTagStructData(self):
        if self.tagDef.B != {}:
            Log.Print(self.tagDef.B)

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)


class FUNCTION(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.functAddress = -1
        self.functAddress_2 = -1
        self.byteOffset = - 1
        self.byteLengthCount = - 1
        self._1st_byte = None
        self._2nd_byte = None
        self._3rd_byte = None
        self._4th_byte = None
        self.min_float = - 1
        self.max_float = - 1
        self.unknown1 = - 1
        self.unknown2 = -1
        self.unk_min = -1
        self.unk_max = -1
        self.leftover_bytes = -1
        self.curvature_bytes = []
        self.data_reference: DataReference = None
        self.bin_data = b''
        self.bin_data_hex = ""
        self.loaded_bin_data = False
        pass

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.functAddress = struct.unpack('Q', f.read(8))[0]  # ReadLong
        self.functAddress_2 = struct.unpack('Q', f.read(8))[0]  # ReadLong
        f.seek(self.addressStart + self.offset + 16)
        self.byteOffset = struct.unpack('i', f.read(4))[0]
        assert self.byteOffset == 0
        self.byteLengthCount = struct.unpack('i', f.read(4))[0]
        if self.functAddress != ADDRESS_UNSET and self.functAddress != 0 and f.tell() + self.functAddress < io.DEFAULT_BUFFER_SIZE:
            f.seek(self.functAddress)
            self._1st_byte = struct.unpack('c', f.read(1))[0]
            self._2nd_byte = struct.unpack('c', f.read(1))[0]
            self._3rd_byte = struct.unpack('c', f.read(1))[0]
            self._4th_byte = struct.unpack('c', f.read(1))[0]
            self.min_float = round(struct.unpack('f', f.read(4))[0], 4)
            self.max_float = round(struct.unpack('f', f.read(4))[0], 4)
            self.unknown1 = round(struct.unpack('f', f.read(4))[0], 4)
            self.unknown2 = round(struct.unpack('f', f.read(4))[0], 4)
            self.unk_min = round(struct.unpack('f', f.read(4))[0], 4)
            self.unk_max = round(struct.unpack('f', f.read(4))[0], 4)
            self.leftover_bytes = struct.unpack('i', f.read(4))[0]
            if self.leftoverbytes > 0:
                self.curvature_bytes = struct.unpack(f'{self.leftoverbytes}p', f.read(self.leftoverbytes))[0]

    def readBinData(self, f, header=None):
        if self.data_reference is not None:
            if not self.data_reference.loaded_bin_data:
                self.data_reference.readBinData(f)
            bin_stream = io.BytesIO(self.data_reference.bin_data)
            bin_stream.seek(self.byteOffset)
            self.bin_data = bin_stream.read(self.byteLengthCount)
            self.bin_data_hex = self.bin_data.hex()
        self.loaded_bin_data = True


class EnumGroup(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.options = []
        self.selected_index = -1
        self.selected = None

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        if self.tagDef.__class__ != TagLayouts.EnumGroup:
            return
        self.tagDef.__class__ = TagLayouts.EnumGroup
        for gvsdahb in self.tagDef.STR:
            self.options.append(self.tagDef.STR[gvsdahb])
        f.seek(self.addressStart + self.offset)
        if self.tagDef.A == 1:
            self.selected_index = struct.unpack('b', f.read(1))[0]
            """
            if (eb1.enums.Items.Count >= test_this)
            {
                eb1.enums.SelectedIndex = test_this;
            }
            else
            {
                TextBox tb = new TextBox { Text = "the enum below is broken :(" };
                parentpanel.Children.Add(tb);
            }
            """
        elif self.tagDef.A == 2:
            self.selected_index = struct.unpack('h', f.read(2))[0]
            """
            if (eb1.enums.Items.Count >= test_this)
            {
                eb1.enums.SelectedIndex = test_this;
            }
            else
            {
                TextBox tb = new TextBox { Text = "the enum below is broken :(" };
                parentpanel.Children.Add(tb);
            }
            """
        elif self.tagDef.A == 4:
            self.selected_index = struct.unpack('i', f.read(4))[0]
            """
            if (eb1.enums.Items.Count >= test_this)
            {
                eb1.enums.SelectedIndex = test_this;
            }
            else
            {
                TextBox tb = new TextBox { Text = "the enum below is broken :(" };
                parentpanel.Children.Add(tb);
            }
            """
        else:
            put_breakpoint_here = 'put_breakpoint_here'

        if self.options.__len__() > self.selected_index > -1:
            self.selected = self.options[self.selected_index]
        else:
            debug = True
            # print("the enum below is broken :(")

    def toJson(self):
        json_obj = super(EnumGroup, self).toJson()
        json_obj['selected_index'] = self.selected_index
        json_obj['selected'] = self.selected
        json_obj['options'] = self.options
        return json_obj


class FourByte(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.value = -1
        pass

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.value = struct.unpack('i', f.read(4))[0]

    def toJson(self):
        json_obj = super(FourByte, self).toJson()
        return self.value


class TwoByte(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.value = -1
        pass

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.value = struct.unpack('h', f.read(2))[0]

    def toJson(self):
        json_obj = super(TwoByte, self).toJson()
        return self.value


class Byte(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.value = -1
        pass

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.value = struct.unpack('b', f.read(1))[0]

    def toJson(self):
        json_obj = super(Byte, self).toJson()
        return self.value


class Float(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.value = -1
        pass

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.value = round(struct.unpack('f', f.read(4))[0], 2)

    def toJson(self):
        json_obj = super(Float, self).toJson()
        return self.value


class TagRef(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.in_game_path = None
        self.path = None
        self.parse = None
        self.tag_ref = None
        self.ref_id_center = None
        self.ref_id_sub = None
        self.ref_id = None
        self.ref_id_center_int = None
        self.ref_id_sub_int = None
        self.ref_id_int = None
        self.global_handle = None
        self.local_handle = None
        self.tagGroup = None
        self.tagGroupRev = None

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.global_handle = struct.unpack('q', f.read(8))[0]
        self.ref_id = f.read(4)
        self.ref_id_int = struct.unpack('i', self.ref_id)[0]
        self.ref_id = self.ref_id.hex().upper()
        self.ref_id_sub = f.read(4)
        self.ref_id_sub_int = struct.unpack('i', self.ref_id_sub)[0]
        self.ref_id_sub = self.ref_id_sub.hex().upper()
        self.ref_id_center = f.read(4)
        self.ref_id_center_int = struct.unpack('i', self.ref_id_center)[0]
        self.ref_id_center = self.ref_id_center.hex().upper()
        self.tagGroup = struct.unpack('4s', f.read(4))[0]
        if self.tagGroup != b'\xff\xff\xff\xff':
            self.tagGroupRev = self.tagGroup[::-1].decode("utf-8")
        self.local_handle = f.read(4).hex().upper()
        #self.path = getStringsByRef(header, self.ref_id, self.ref_id_sub, self.ref_id_center, self.tagGroupRev)

    def toJson(self):
        json_obj = super(TagRef, self).toJson()
        return self.path

    def loadPath(self):
        """
        temp_path = self.path
        if temp_path != self.tag_ref.str_path:
            debug = True
        """
        self.path = self.tag_ref.str_path

    def getInGamePath(self):
        if self.in_game_path is None:
            self.in_game_path = ''
            try:
                if self.path.__contains__('color_black'):
                    debug = True
                self.in_game_path = TAG_NAMES[self.ref_id]
            except KeyError as e:
                try:
                    if e.args[0] != self.ref_id_sub:
                        self.in_game_path = TAG_NAMES[self.ref_id_sub]
                    elif e.args[0] != self.ref_id_center:
                        self.in_game_path = TAG_NAMES[self.ref_id_center]
                except  KeyError as e1:
                    try:
                        if e1.args[0] != self.ref_id_center:
                            self.in_game_path = TAG_NAMES[self.ref_id_center]
                    except  KeyError as e2:
                        self.in_game_path = ''
                        #print(f"No mapped {self.path} id {self.ref_id} id_sub {self.ref_id_sub} id_center {self.ref_id_center}")


        return self.in_game_path




class Pointer(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.value = -1
        pass

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.value = struct.unpack('q', f.read(8))[0]

    def toJson(self):
        json_obj = super(Pointer, self).toJson()
        return self.value


class ResourceHandle(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.childrenCount = 1
        self.addres_dir_1 = -1
        self.value = -1
        self.str_value = ''
        self.int_value = -1
        self.content_entry = None

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.addres_dir_1 = struct.unpack('Q', f.read(8))[0]
        bin_data = f.read(4)
        self.value = bin_data.hex().upper()
        self.str_value = getStrInMmr3Hash(self.value)
        self.int_value = int.from_bytes(bin_data, byteorder="little", signed=True)
        self.childrenCount = struct.unpack('i', f.read(4))[0]
        if self.childrenCount != 0:
            debug = True


class Tagblock(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.childrenCount = -1
        self.newAddress = -1
        self.stringAddress = -1
        self.content_entry = None

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.newAddress = struct.unpack('Q', f.read(8))[0]
        self.stringAddress = struct.unpack('Q', f.read(8))[0]
        """
        string our_name = entry.Value.N;
        if (our_name == null)
        {
            tb1.tagblock_title.Text = _m.ReadString((address + entry.Key + 8).ToString("X") + ",0,0", "", 100); // this is the only thing that causes errors with unloaded tags
        }
        else
        {
            tb1.tagblock_title.Text = our_name;
        }
        """
        self.childrenCount = struct.unpack('i', f.read(4))[0]
        if self.childrenCount < 0:
            debug = True
            assert False, 'no puede tener la cantidad de hijos en -1'


class TagStructBlock(TagInstance):
    # --THIS DOESN'T WORK, DON'T USE. IF YOU WANT TO TRY TO GET IT WORKING, GOOD LUCK.
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.comment = tag.N
        self.childrenCount = 0
        pass

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        self.comment = self.tagDef.N


class String(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.string = ""

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        temp_field_data = f.read(self.tagDef.S)
        temp_field_data_hex = temp_field_data.hex()

        self.string = readStringInPlace(f, self.addressStart + self.offset)
        # Revisar ojo puede estar mal

    def toJson(self):
        json_obj = super(String, self).toJson()
        return self.string


class StringTag(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.tag_string = ""
        self.tag_string_rev = ""

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)

        self.tag_string = struct.unpack('4s', f.read(4))[0]
        self.tag_string_rev = self.tag_string[::-1].decode("utf-8")

    def toJson(self):
        json_obj = super(String, self).toJson()
        return self.string


class Flags(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.flags_value = None

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.flags_value = struct.unpack('c', f.read(1))[0]

        """
        vb9.flag1.IsChecked = flags_value.GetBit(0);
        vb9.flag2.IsChecked = flags_value.GetBit(1);
        vb9.flag3.IsChecked = flags_value.GetBit(2);
        vb9.flag4.IsChecked = flags_value.GetBit(3);
        vb9.flag5.IsChecked = flags_value.GetBit(4);
        vb9.flag6.IsChecked = flags_value.GetBit(5);
        vb9.flag7.IsChecked = flags_value.GetBit(6);
        vb9.flag8.IsChecked = flags_value.GetBit(7);
        """

    def toJson(self):
        json_obj = super(Flags, self).toJson()
        return self.options


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def hex_to_binary(hex_number: str, num_digits: int = 8) -> str:
    """
    Converts a hexadecimal value into a string representation
    of the corresponding binary value
    Args:
        hex_number: str hexadecimal value
        num_digits: integer value for length of binary value.
                    defaults to 8
    Returns:
        string representation of a binary number 0-padded
        to a minimum length of <num_digits>
    """
    return str(bin(int(hex_number, 16)))[2:].zfill(num_digits)


class FlagGroup(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.flags_value = ''
        self.options = {}

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        fdebug = "debughere"
        if self.tagDef.__class__ != TagLayouts.FlagGroup:
            return
        self.tagDef.__class__ = TagLayouts.FlagGroup
        self.generateBits(self.addressStart, self.tagDef.A, self.tagDef.MB, self.tagDef.STR, f)
        if self.flags_value == '':
            return
        for i, key_option in enumerate(self.tagDef.STR):
            if self.options.keys().__contains__(self.tagDef.STR[key_option]):
                assert False
            self.options[self.tagDef.STR[key_option]] = self.flags_value[i] == '1'
        debug = self.options

    def toJson(self):
        json_obj = super(FlagGroup, self).toJson()
        return self.options

    def generateBits(self, startAddress, amountOfBytes: int, maxBit: int, descriptions: {}, f: BinaryIO):
        """
        self.startAddress = startAddress
        self.amountOfBytes = amountOfBytes
        self.maxBit = maxBit
        """
        if maxBit == 0:
            maxBit = amountOfBytes * 8

        # spBitCollection.Children.Clear();

        maxAmountOfBytes = clamp(math.ceil(maxBit / 8), 0, amountOfBytes)
        bitsLeft = maxBit - 1;  # -1 to start at

        self.flags_value = ''
        for _byte in range(maxAmountOfBytes):

            if bitsLeft < 0:
                continue;
            amountOfBits = ((_byte * 8) - maxBit) if _byte * 8 > maxBit else 8

            addr = startAddress + _byte
            f.seek(addr)
            hex_byte = f.read(1).hex()

            self.flags_value = self.flags_value + (hex_to_binary(hex_byte))
            """
            for bit in range(amountOfBits):
                currentBitIndex = (_byte * 8) + bit
                if bitsLeft < 0:
                    continue
                # CheckBox? checkbox = null;
                s_byte = _byte
                _bit = bit
               
                checkbox = new CheckBox();
                checkbox.Margin = new
                System.Windows.Thickness(5, 0, 0, 0);
                checkbox.IsChecked = flags_value.GetBit(bit);
                checkbox.Checked += (s, e) = > Checkbox_BitIsChanged(_byte, _bit);
                checkbox.Unchecked += (s, e) = > Checkbox_BitIsChanged(_byte, _bit);
                checkbox.Content =
                descriptions != null & & descriptions.ContainsKey(currentBitIndex)
                ? descriptions[(@ byte * 8) + bit]: "Flag " + (currentBitIndex);

                // < TextBlock
                Foreground = "Black" > Only
                show
                mapped
                tags < / TextBlock >
                         checkbox.ToolTip = new
                TextBlock()
                {
                Foreground = Brushes.Black
                , Text = $"Flag Bit {currentBitIndex}, Addr = {startAddress + (@byte * 8)}:^{bit}"
                };
    
                if (checkbox != null)
                {
                spBitCollection.Children.Add(checkbox);
                }
               
                bitsLeft = bitsLeft - 1
        """


class Mmr3Hash(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.value = None
        self.str_value = ''
        self.int_value = ''

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        bin_data = f.read(4)
        self.value = bin_data.hex().upper()
        self.str_value = getStrInMmr3Hash(self.value)
        self.int_value = int.from_bytes(bin_data, byteorder="little", signed=True)
        # assert self.value == getMmr3HashFromInt(self.int_value), "Han de ser iguales"

    def toJson(self):
        super(Mmr3Hash, self).toJson()
        return {
            'value': self.value,
            'str_value': self.str_value,
            'int_value': self.int_value
        }


class RGB(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.r_value = -1
        self.g_value = -1
        self.b_value = -1

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.r_value = round(struct.unpack('f', f.read(4))[0], 4)
        self.g_value = round(struct.unpack('f', f.read(4))[0], 4)
        self.b_value = round(struct.unpack('f', f.read(4))[0], 4)

    def toJson(self):
        json_obj = super(RGB, self).toJson()
        return {
            'r_value': self.r_value,
            'g_value': self.g_value,
            'b_value': self.b_value,
        }


class ARGB(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.a_value = -1
        self.r_value = -1
        self.g_value = -1
        self.b_value = -1

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.a_value = round(struct.unpack('f', f.read(4))[0], 4)
        self.r_value = round(struct.unpack('f', f.read(4))[0], 4)
        self.g_value = round(struct.unpack('f', f.read(4))[0], 4)
        self.b_value = round(struct.unpack('f', f.read(4))[0], 4)

    def toJson(self):
        json_obj = super(ARGB, self).toJson()
        return {
            'a_value': self.a_value,
            'r_value': self.r_value,
            'g_value': self.g_value,
            'b_value': self.b_value,
        }


class BoundsFloat(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.min = -1
        self.max = -1

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.min = round(struct.unpack('f', f.read(4))[0], 4)
        self.max = round(struct.unpack('f', f.read(4))[0], 4)

    def toJson(self):
        json_obj = super(BoundsFloat, self).toJson()
        return {
            'min': self.min,
            'max': self.max,
        }


class Bounds2Byte(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.min = -1
        self.max = -1

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.min = struct.unpack('h', f.read(2))[0]
        self.max = struct.unpack('h', f.read(2))[0]
        # Reviar pq en el C leen float 4byte
        debug = "debug"

    def toJson(self):
        json_obj = super(Bounds2Byte, self).toJson()
        return {
            'min': self.min,
            'max': self.max,
        }


class Point2D_Float(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.x = -1
        self.y = -1

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.x = round(struct.unpack('f', f.read(4))[0], 4)
        self.y = round(struct.unpack('f', f.read(4))[0], 4)

    def toJson(self):
        json_obj = super(Point2D_Float, self).toJson()
        return {
            'x': self.x,
            'y': self.y,
        }


class Point2D_2Byte(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.x = -1
        self.y = -1

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.x = struct.unpack('h', f.read(4))[0]
        self.y = struct.unpack('h', f.read(4))[0]
        # Reviar pq en el C leen float 4byte
        debug = "debug"

    def toJson(self):
        json_obj = super(Point2D_2Byte, self).toJson()
        return {
            'x': self.x,
            'y': self.y,
        }


class Point3D(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.x = -1
        self.y = -1
        self.z = -1

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.x = round(struct.unpack('f', f.read(4))[0], 4)
        self.y = round(struct.unpack('f', f.read(4))[0], 4)
        self.z = round(struct.unpack('f', f.read(4))[0], 4)

    def toJson(self):
        json_obj = super(Point3D, self).toJson()
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
        }


class Quaternion(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.x = -1
        self.y = -1
        self.z = -1
        self.w = -1

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.x = round(struct.unpack('f', f.read(4))[0], 4)
        self.y = round(struct.unpack('f', f.read(4))[0], 4)
        self.z = round(struct.unpack('f', f.read(4))[0], 4)
        self.w = round(struct.unpack('f', f.read(4))[0], 4)

    def toJson(self):
        json_obj = super(Quaternion, self).toJson()
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'w': self.w,
        }


class Plane3D(TagInstance):
    def __init__(self, tag: TagLayouts.C, addressStart: int, offset: int):
        super().__init__(tag, addressStart, offset)
        self.x = -1
        self.y = -1
        self.z = -1
        self.point = -1

    def readIn(self, f: BinaryIO, header=None):
        super().readIn(f, header)
        f.seek(self.addressStart + self.offset)
        self.x = round(struct.unpack('f', f.read(4))[0], 4)
        self.y = round(struct.unpack('f', f.read(4))[0], 4)
        self.z = round(struct.unpack('f', f.read(4))[0], 4)
        self.point = round(struct.unpack('f', f.read(4))[0], 4)

    def toJson(self):
        json_obj = super(Plane3D, self).toJson()
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'point': self.point,
        }


def tagInstanceFactoryCreate(tag, addressStart, offset):
    if tag.T == "Comment":
        return Comment(tag=tag, addressStart=addressStart,
                       offset=offset)
    elif tag.T == "ArrayFixLen":
        return ArrayFixLen(tag=tag, addressStart=addressStart,
                           offset=offset)
    elif tag.T == "GenericBlock":
        return GenericBlock(tag=tag, addressStart=addressStart,
                            offset=offset)
    elif tag.T == "TagStructData":
        return TagStructData(tag=tag, addressStart=addressStart,
                             offset=offset)
    elif tag.T == "FUNCTION":
        return FUNCTION(tag=tag, addressStart=addressStart,
                        offset=offset)
    elif tag.T == "EnumGroup":
        return EnumGroup(tag=tag, addressStart=addressStart,
                         offset=offset)
    elif tag.T == "4Byte":
        return FourByte(tag=tag, addressStart=addressStart,
                        offset=offset)
    elif tag.T == "2Byte":
        return TwoByte(tag=tag, addressStart=addressStart,
                       offset=offset)
    elif tag.T == "Byte":
        return Byte(tag=tag, addressStart=addressStart,
                    offset=offset)
    elif tag.T == "Float":
        return Float(tag=tag, addressStart=addressStart,
                     offset=offset)
    elif tag.T == "TagRef":
        return TagRef(tag=tag, addressStart=addressStart,
                      offset=offset)
    elif tag.T == "Pointer":
        return Pointer(tag=tag, addressStart=addressStart,
                       offset=offset)
    elif tag.T == "Tagblock":
        return Tagblock(tag=tag, addressStart=addressStart,
                        offset=offset)
    elif tag.T == "ResourceHandle":
        return ResourceHandle(tag=tag, addressStart=addressStart,
                              offset=offset)
    elif tag.T == "TagStructBlock":
        return TagStructBlock(tag=tag, addressStart=addressStart, offset=offset)
    elif tag.T == "String":
        return String(tag=tag, addressStart=addressStart,
                      offset=offset)
    elif tag.T == "StringTag":
        return StringTag(tag=tag, addressStart=addressStart,
                         offset=offset)
    elif tag.T == "Flags":
        return Flags(tag=tag, addressStart=addressStart,
                     offset=offset)
    elif tag.T == "FlagGroup":
        return FlagGroup(tag=tag, addressStart=addressStart,
                         offset=offset)
    elif tag.T == "mmr3Hash":
        return Mmr3Hash(tag=tag, addressStart=addressStart,
                        offset=offset)
    elif tag.T == "RGB":
        return RGB(tag=tag, addressStart=addressStart,
                   offset=offset)
    elif tag.T == "ARGB":
        return ARGB(tag=tag, addressStart=addressStart,
                    offset=offset)
    elif tag.T == "BoundsFloat":
        return BoundsFloat(tag=tag, addressStart=addressStart,
                           offset=offset)
    elif tag.T == "Bounds2Byte":
        return Bounds2Byte(tag=tag, addressStart=addressStart,
                           offset=offset)
    elif tag.T == "2DPoint_Float":
        return Point2D_Float(tag=tag, addressStart=addressStart, offset=offset)
    elif tag.T == "2DPoint_2Byte":
        return Point2D_2Byte(tag=tag, addressStart=addressStart, offset=offset)
    elif tag.T == "3DPoint":
        return Point3D(tag=tag, addressStart=addressStart,
                       offset=offset)
    elif tag.T == "Quaternion":
        return Quaternion(tag=tag, addressStart=addressStart,
                          offset=offset)
    elif tag.T == "3DPlane":
        return Plane3D(tag=tag, addressStart=addressStart,
                       offset=offset)
    else:
        return TagInstance(tag=tag, addressStart=addressStart,
                           offset=offset)
