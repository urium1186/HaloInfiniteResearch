from tag_reader.tag_instance import TagInstance
from tag_reader.readers.base_template import BaseTemplate


class Material(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mat ')
        self.json_str_base = '{"swatches":[]}'

    def load(self):
        super().load()

    def onInstanceLoad(self, instance: TagInstance):
        super(Material, self).onInstanceLoad(instance)
        if instance.tagDef.N == 'material parameters':
            if len(instance.childs) != 0 and not str(self.in_game_path).__contains__('_gear_'):
                #if not len(instance.childs) == 6:
                #    print(f"{len(instance.childs)} {self.in_game_path}")
                c_param = 0
                for item in instance.childs:
                    faund = False
                    if instance.parent.childs[0]['material shader'].parse is not None:
                        for mat_param in instance.parent.childs[0]['material shader'].parse.first_child[
                            'material parameters'].childs:

                            if item['parameter name'].value == mat_param['parameter name'].value:
                                c_param += 1
                                faund = True
                                break
                    if not faund:
                        debug=True
                    # ['bitmap', 'real', 'int', 'bool', 'color', 'scalar gpu property', 'color gpu property', 'string', 'preset']
                    parameter_type = item['parameter type'].selected
                    try:
                        temp = None

                        if parameter_type == 'int' or parameter_type == 'bool':
                            temp = item['int/bool']
                        if parameter_type == 'color gpu property':
                            temp = item['color']
                        if parameter_type == 'scalar gpu property':
                            temp = item['real']
                        if parameter_type == 'preset':
                            assert False
                        else:
                            temp = item[parameter_type]
                    except:
                        debug = True

                if c_param == len(instance.childs):
                    debug = True
                else:
                    debug = True
        elif instance.tagDef.N== 'style info':

            if instance.childrenCount !=0:
                assert instance.childrenCount==1
                if instance.childs[0]['region name'].value in ['326D0638', 'C1E58CB9', '1B61B6F2']:
                    debug = True
