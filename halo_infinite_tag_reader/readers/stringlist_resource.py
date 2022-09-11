from halo_infinite_tag_reader.readers.base_template import BaseTemplate
from halo_infinite_tag_reader.common_tag_types import TagInstance, readStringInPlace


class StringListResource(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'uslg_r')
        self.json_str_base = '{"root":[]}'

    def load(self):
        super().load()

    def onInstanceLoad(self, instance: TagInstance):
        super(StringListResource, self).onInstanceLoad(instance)
        if instance.tagDef.N == "array_0":
           debug=1
           init_adress = instance.content_entry.data_reference.offset_plus + instance.content_entry.data_reference.size
           for x in instance.childs:
               offset_temp = init_adress + x['offset'].value
               x['name'].extra_data = {"str_":readStringInPlace(self.tag_parse.f,offset_temp, True)}