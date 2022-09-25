class ReadTagStructException(Exception):
    def __init__(self, file_name, tag_struct):
        super(ReadTagStructException, self).__init__()
        self.file_name = file_name
        self.tag_struct = tag_struct
