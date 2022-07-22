import binascii

import gf
from exporters.to.image.dds_utilts.dds import *


class DdsFile:
    def __init__(self):
        self.magic: np.uint32 = np.uint32(0x20534444)  # 0
        self.header: DDS_HEADER = None
        self.header10: DDS_HEADER_DXT10 = None
        self.bdata: bytes = b''
        self.bdata2: bytes = b''

    def loadDefaultValues(self, p_format):
        form = DXGI_FORMAT(p_format).name
        use_h_10 = False
        if '_BC' in form:
            use_h_10 = True

        self.header = DDS_HEADER()
        self.header10 = DDS_HEADER_DXT10()
        self.header.size = 124
        self.header.flags = (0x1 + 0x2 + 0x4 + 0x1000) + 0x8
        self.header.height = 1
        self.header.width = 1
        # self.header.pitchOrLinearSize = *
        self.header.depth = 0
        self.header.mipMapCount = 0
        self.header.reserved1 = [0] * 11
        _ddspf = DDS_PIXELFORMAT()
        _ddspf.size = 32
        _ddspf.flags = 5
        _ddspf.RGBBitCount = 32
        _ddspf.RBitMask = 0xFF
        _ddspf.GBitMask = 0xFF00
        _ddspf.BBitMask = 0xFF0000
        _ddspf.ABitMask = 0xFF000000

        self.header.caps = 0x1000
        self.header.caps2 = 0
        self.header.caps3 = 0
        self.header.caps4 = 0
        self.header.reserved2 = 0
        """
        Four-character codes for specifying compressed or custom formats. Possible values include: DXT1, DXT2, 
        DXT3, DXT4, or DXT5. A FourCC of DX10 indicates the prescense of the DDS_HEADER_DXT10 extended header, 
        and the dxgiFormat member of that structure indicates the true format. When using a four-character code, 
        dwFlags must include DDPF_FOURCC.
         """
        if '_BC' in form:
            _ddspf.flags = 0x1 + 0x4  # contains alpha data + contains compressed RGB data
            _ddspf.fourCC = int.from_bytes(b'\x44\x58\x31\x30', byteorder='little')
            self.header10.dxgiFormat = np.uint32(p_format)
            self.header10.resourceDimension = np.uint32(D3D10_RESOURCE_DIMENSION.D3D10_RESOURCE_DIMENSION_TEXTURE2D)
            # Compressed BCn
            self.header10.miscFlag = 0
            self.header10.arraySize = 1
        else:
            # Uncompressed
            self.header.dwPFFlags = 0x1 + 0x40  # contains alpha data + contains uncompressed RGB data
            self.header.dwPFFourCC = 0
            self.header10.miscFlag = 0
            self.header10.arraySize = 1
            self.header10.miscFlags2 = 0x1
        self.header.ddspf = _ddspf



    def getBinaryData(self):
        tem_bytes: bytes = b''
        flipped = "".join(
            gf.get_flipped_hex(gf.fill_hex_with_zeros(hex(np.uint32(self.magic))[2:], 8), 8))
        tem_bytes += binascii.unhexlify(flipped)
        obj = self.header
        b_header = self._getBinaryDataOfObj(obj)
        if len(b_header) != self.header.size:
            raise Exception('Hedear size modify')
        tem_bytes += b_header
        if self.header10 is not None:
            obj = self.header10
            b_header10 = self._getBinaryDataOfObj(obj)
            tem_bytes += b_header10

        tem_bytes += self.bdata
        tem_bytes += self.bdata2
        return tem_bytes

    def _getBinaryDataOfObj(self, obj):
        tem_bytes: bytes = b''
        isFromObj = False
        for f in fields(obj):
            if f.type == np.uint32:
                isFromObj = False
                flipped = "".join(
                    gf.get_flipped_hex(gf.fill_hex_with_zeros(hex(np.uint32(getattr(obj, f.name)))[2:], 8), 8))
            elif f.type == List[np.uint32]:
                flipped = ''
                isFromObj = False
                for val in getattr(obj, f.name):
                    flipped += "".join(
                        gf.get_flipped_hex(gf.fill_hex_with_zeros(hex(np.uint32(val))[2:], 8), 8))
            else:
                isFromObj = True
                tem_bytes += self._getBinaryDataOfObj(getattr(obj, f.name))
            if not isFromObj:
                tem_bytes += binascii.unhexlify(flipped)

        return tem_bytes
