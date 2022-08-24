from commons.enums_struct_def import PcVertexBuffersFormat


def readVertexBuffer(b_format: PcVertexBuffersFormat):
    if b_format == PcVertexBuffersFormat.real:
        readRealBuffer()


def readRealBuffer():
    return []
