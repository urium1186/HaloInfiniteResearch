from tag_reader.readers.base_template import BaseTemplate
from tag_reader.tag_instance import TagInstance


class AttachmentConfiguration(BaseTemplate):
    def __init__(self, filename):
        super(AttachmentConfiguration, self).__init__(filename, 'ocad')

    def onInstanceLoad(self, instance: TagInstance):
        super(AttachmentConfiguration, self).onInstanceLoad(instance)
