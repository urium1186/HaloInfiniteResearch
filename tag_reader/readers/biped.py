from tag_reader.readers.base_template import BaseTemplate
from tag_reader.tag_instance import TagInstance


class Biped(BaseTemplate):
    def __init__(self, filename):
        super(Biped, self).__init__(filename, 'bipd')

    def onInstanceLoad(self, instance: TagInstance):
        super(Biped, self).onInstanceLoad(instance)
        if instance.tagDef.N.__contains__('variant'):
            debug = True
