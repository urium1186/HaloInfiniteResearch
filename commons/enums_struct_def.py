from enum import IntFlag


class TagStructType(IntFlag):
    Root = 0
    Tagblock = 1
    ExternalFileDescriptor = 2
    ResourceHandle = 3
    NoDataStartBlock = 4