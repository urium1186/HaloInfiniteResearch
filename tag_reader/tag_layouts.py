import inspect
import os
import xml.etree.ElementTree as ET


class TagLayouts:
    class C:

        def __init__(self, p_T='', p_N='', p_B=None, p_S=0, p_P={},p_E={}):
            if p_B is None:
                p_B = {}
            self.T = p_T  # T = type
            self.B = p_B  # Dictionary<long, C>? B { get set } = null  # B = blocks? i forgot what B stands for
            self.P = p_P
            self.E = p_E
            """
            #/ <summary>
            #/ Length of the tagblock
            #/ </summary>
            """
            self.S = p_S  # public long S { get set } # S = size # length of tagblock

            self.N = p_N  # N = name # our name for the block

            """
            #/ <summary>
            #/ Set during load, will be used when I add netcode 
            #/ </summary>
            """
            self.MemoryAddress = 0

            """
            #/ <summary>
            #/ The absolute offset from the base address of the tag
            #/ eg C2 will resolve to assault_rifle_mp.weapon + C2 
            #/ 
            #/ This will be recursive so the actual value might be 
            #/		assault_rifle_mp.weapon + C2 + (nested block) 12 + (nested block) 4
            #/		
            #/ This will allow us to sync up changes across the server and client without
            #/ the need to re-resolve memory addresses.
            #/ </summary>
            """

            self.AbsoluteTagOffset = ''  # # as a string we can append offsets rather than mathmatically adding them
            self.TagInstance = {}
            self.content_data = None

    class FlagGroup(C):

        def __init__(self, p_A: int = 0, p_N: str = '', p_STR={}):
            super()
            self.T = "FlagGroup"
            """
                    #/ <summary>
                    #/ Amount of bytes for flags
                    #/ </summary>
                    """
            self.A = p_A

            """
            #/ <summary>
            #/ The max bit, if 0 then defaults to A * 8
            #/ </summary>
            """
            self.MB: int = 0

            self.N = p_N

            """
            #/ <summary>
            #/ String description of the flags
            #/ </summary>
            """
            self.STR = p_STR  # public Dictionary<int, string> STR { get set } = new Dictionary<int, string>()

    class EnumGroup(C):

        def __init__(self, p_A: int = 0, p_N: str = '', p_STR={}):
            super()
            self.T = "EnumGroup"
            """
                    #/ <summary>
                    #/ Amount of bytes for enum
                    #/ </summary>
                    """
            self.A = p_A

            self.N = p_N

            """
            #/ <summary>
            #/ String description of the flags
            #/ </summary>
            """
            self.STR = p_STR

    @staticmethod
    def Tags(grouptype: str):
        r = TagLayouts.run_parse()
        return r.parse_the_mfing_xmls(grouptype)

    class run_parse:

        def __init__(self):
            self.evalutated_index_PREVENT_DICTIONARYERROR = 99999
            pass

        def parse_the_mfing_xmls(self, file_to_find: str):
            poopdict = {}

            # e still need to evalute the string and find the value withoin our plugins folder

            if file_to_find.__contains__("*"):
                file_to_find = file_to_find.replace("*", "_")

            #predicted_file = os.path.curdir + '\\plugins\\' + file_to_find + '.xml'

            filename = inspect.getframeinfo(inspect.currentframe()).filename
            path = os.path.dirname(os.path.abspath(filename))
            predicted_file = path + '\\tags\\' + file_to_find + '.xml'
            #predicted_file = path + '\\plugins\\' + file_to_find + '.xml'

            if os.path.exists(predicted_file):
                xd = ET.parse(predicted_file)
                xn = xd.getroot()
                xnl = list(xn)
                current_offset = 0
                for xntwo in xnl:
                    current_offset = current_offset + self.the_switch_statement(xntwo, current_offset,
                                                                                poopdict)  # ref poopdict

            return poopdict

        def the_switch_statement(self, xn, offset, pairs={}):

            if xn.tag == "_0":
                pairs[offset] = TagLayouts.C("String", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_1":
                pairs[offset] = TagLayouts.C("String", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_2":
                pairs[offset] = TagLayouts.C("mmr3Hash", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_3":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_4":
                pairs[offset] = TagLayouts.C("Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_5":
                pairs[offset] = TagLayouts.C("2Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_6":
                pairs[offset] = TagLayouts.C("4Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_7":
                pairs[offset] = TagLayouts.C("Pointer", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_8":
                pairs[offset] = TagLayouts.C("Float", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_9":
                pairs[offset] = TagLayouts.C("StringTag", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
                """
                // This is the special case mentioned in previous versions.
                // Example, needing to change the empty tag reference in effects to spawn AI.
                // I tested it in game and its functional.
                """

            elif xn.tag == "_A":
                childdictionary1 = {}
                for iu in range(len(xn)):
                    childdictionary1[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.EnumGroup(1, xn.attrib["v"], childdictionary1)
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_B":
                childdictionary2 = {}
                for iu in range(len(xn)):
                    childdictionary2[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.EnumGroup(2, xn.attrib["v"], childdictionary2)
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_C":
                childdictionary3 = {}
                for iu in range(len(xn)):
                    childdictionary3[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.EnumGroup(4, xn.attrib["v"], childdictionary3)
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_D":
                childdictionary4 = {}
                for iu in range(len(xn)):
                    childdictionary4[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.FlagGroup(4, xn.attrib["v"], childdictionary4)
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_E":
                childdictionary5 = {}
                for iu in range(len(xn)):
                    childdictionary5[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.FlagGroup(2, xn.attrib["v"], childdictionary5)
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_F":
                childdictionary6 = {}
                for iu in range(len(xn)):
                    childdictionary6[iu] = xn[iu].attrib["v"]
                pairs[offset] = TagLayouts.FlagGroup(1, xn.attrib["v"], childdictionary6)
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_10":  # // im not 100% on this one
                pairs[offset] = TagLayouts.C("2DPoint_2Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_11":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_12":
                raise Exception("Revisar pq se dice q es un color")
                pairs[offset] = TagLayouts.C("mmr3Hash", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_13":  # unmapped - This case isn't found in any tag file
                raise Exception("unmapped - This case isn't found in any tag file")
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_14":
                pairs[offset] = TagLayouts.C("Float", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_15":
                pairs[offset] = TagLayouts.C("Float", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_16":
                pairs[offset] = TagLayouts.C("2DPoint_Float", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_17":
                pairs[offset] = TagLayouts.C("3DPoint", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_18":
                pairs[offset] = TagLayouts.C("2DPoint_Float", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_19":
                pairs[offset] = TagLayouts.C("3DPoint", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_1A":
                pairs[offset] = TagLayouts.C("Quaternion", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_1B":
                pairs[offset] = TagLayouts.C("2DPoint_Float", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_1C":
                pairs[offset] = TagLayouts.C("3DPoint", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_1D":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_1E":
                pairs[offset] = TagLayouts.C("3DPlane", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_1F":
                pairs[offset] = TagLayouts.C("RGB", xn.attrib["v"], p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_20":
                pairs[offset] = TagLayouts.C("ARGB", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_21":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_22":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_23":
                pairs[offset] = TagLayouts.C("2Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                pairs[offset + 2] = TagLayouts.C("2Byte", xn.attrib["v"],
                                                 p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_24":
                pairs[offset] = TagLayouts.C("BoundsFloat", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_25":
                pairs[offset] = TagLayouts.C("BoundsFloat", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_26":
                pairs[offset] = TagLayouts.C("BoundsFloat", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_27":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_28":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_29":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_2A":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_2B":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_2C":
                pairs[offset] = TagLayouts.C("Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_2D":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_2E":
                pairs[offset] = TagLayouts.C("2Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_2F":
                pairs[offset] = TagLayouts.C("2Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_30":
                pairs[offset] = TagLayouts.C("4Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_31":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_32":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_33":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_34":
                length = int(xn.attrib["length"])
                if length == 1:
                    pairs[offset] = TagLayouts.C("Byte", xn.attrib["v"],
                                                 p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                elif length == 2:
                    pairs[offset] = TagLayouts.C("2Byte", xn.attrib["v"],
                                                 p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                elif length == 4:
                    pairs[offset] = TagLayouts.C("4Byte", xn.attrib["v"],
                                                 p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                else:
                    pairs[offset] = TagLayouts.C("Comment", xn.attrib["v"],
                                                 p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return length
            elif xn.tag == "_35":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("GenericBlock",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)",
                                             p_S=int(xn.attrib["length"]))
                return int(xn.attrib["length"])
            elif xn.tag == "_36":
                if xn.attrib["v"] != '':
                    pairs[offset + self.evalutated_index_PREVENT_DICTIONARYERROR] = TagLayouts.C("Comment",
                                                                                                 xn.attrib["v"])
                    self.evalutated_index_PREVENT_DICTIONARYERROR = self.evalutated_index_PREVENT_DICTIONARYERROR + 1
                else:
                    debug = 0  # debug
                return 0
            elif xn.tag == "_37":
                if xn.attrib["v"] != '':
                    pairs[offset + self.evalutated_index_PREVENT_DICTIONARYERROR] = TagLayouts.C("Comment",
                                                                                                 xn.attrib["v"])
                    self.evalutated_index_PREVENT_DICTIONARYERROR = self.evalutated_index_PREVENT_DICTIONARYERROR + 1
                else:
                    debug = 0  # debug
                return 0
            elif xn.tag == "_38":  # //struct
                """
                // --THIS WAS A TEST FOR ADDING STRUCT UI--
                //Dictionary<long, C> subthings1 = new Dictionary<long, C>();
                //XmlNodeList xnl1 = xn.ChildNodes;
                //int childnodescount = xnl1.Count;
                //long current_offset1 = offset;
                //foreach (XmlNode xntwo2 in xnl1)
                //{
                //	current_offset1 += the_switch_statement(xntwo2, current_offset1, ref subthings1);
                //}
                //pairs.Add(offset, new C { T = "TagStructBlock", N = xn.Attributes.GetNamedItem("v").InnerText + " Nodes = " + childnodescount, B = subthings1 });
                """
                temp_index = offset + self.evalutated_index_PREVENT_DICTIONARYERROR
                p_P = {"generateEntry": False}
                p_E = {}
                if xn.attrib.keys().__contains__('g'):
                    p_P = {"generateEntry": xn.attrib['g'] == "true"}
                #elif xn.attrib.keys().__contains__('db1'):
                #    p_P = {"generateEntry": xn.attrib['db5'] == '1' and xn.attrib['db3'] != "0"}
                if xn.attrib.keys().__contains__('db1'):
                    p_E['db1'] = xn.attrib['db1']
                    p_E['db2'] = xn.attrib['db2']
                    p_E['db3'] = xn.attrib['db3']
                    p_E['db4'] = xn.attrib['db4']
                    p_E['db5'] = xn.attrib['db5']
                    p_E['db6'] = xn.attrib['db6']
                    p_E['db7'] = xn.attrib['db7']
                    p_E['db8'] = xn.attrib['db8']


                pairs[temp_index] = TagLayouts.C("TagStructData", xn.attrib["v"], p_P=p_P, p_E=p_E)

                self.evalutated_index_PREVENT_DICTIONARYERROR = self.evalutated_index_PREVENT_DICTIONARYERROR + 1
                current_offset1 = current_offset_temp1 = offset
                xnl1 = list(xn)
                sub_dic = {}
                for xntwo2 in xnl1:
                    current_offset1 = current_offset1 + self.the_switch_statement(xntwo2, current_offset1, sub_dic)
                pairs[temp_index].B = sub_dic
                pairs[temp_index].S = current_offset1
                for k in sub_dic.keys():
                    pairs[k] = sub_dic[k]
                return current_offset1 - offset
            elif xn.tag == "_39":
                """
                pairs[offset + self.evalutated_index_PREVENT_DICTIONARYERROR] = TagLayouts.C("ArrayFixLen",
                                                                                             xn.attrib["v"])
                self.evalutated_index_PREVENT_DICTIONARYERROR = self.evalutated_index_PREVENT_DICTIONARYERROR + 1
                current_offset3 = current_offset_temp3 = offset
                for xntwo2 in xn:
                    current_offset3 = current_offset3 + self.the_switch_statement(xntwo2, current_offset3, pairs)

                return current_offset3 - offset
                """
                if len(xn) > 0:
                    subthings = {}
                    current_offset2 = current_offset2_temp = 0
                    for xntwo2 in xn:
                        current_offset2 = current_offset2 + self.the_switch_statement(xntwo2, current_offset2,
                                                                                      subthings)
                        # its gonna append that to the main, rather than our struct
                    pairs[offset] = TagLayouts.C("ArrayFixLen", xn.attrib["v"], subthings, current_offset2)
                else:
                    pairs[offset] = TagLayouts.C("ArrayFixLen", xn.attrib["v"],
                                                 p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return current_offset2
            elif xn.tag == "_3A":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_3B":
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_3C":
                pairs[offset] = TagLayouts.C("Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_3D":
                pairs[offset] = TagLayouts.C("2Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_3E":
                pairs[offset] = TagLayouts.C("4Byte", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_3F":
                pairs[offset] = TagLayouts.C("Pointer", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_40":
                p_E = {}
                if xn.attrib.keys().__contains__('db1'):
                    p_E['db1'] = xn.attrib['db1']
                    p_E['db2'] = xn.attrib['db2']
                    p_E['db3'] = xn.attrib['db3']
                    p_E['db4'] = xn.attrib['db4']
                    p_E['db5'] = xn.attrib['db5']
                    p_E['db6'] = xn.attrib['db6']
                    p_E['db7'] = xn.attrib['db7']
                    p_E['db8'] = xn.attrib['db8']
                if len(xn) > 0:
                    subthings = {}
                    current_offset2 = current_offset2_temp = 0
                    for xntwo2 in xn:
                        current_offset2 = current_offset2 + self.the_switch_statement(xntwo2, current_offset2,
                                                                                      subthings)
                        # its gonna append that to the main, rather than our struct
                    pairs[offset] = TagLayouts.C("Tagblock", xn.attrib["v"], subthings, current_offset2, p_E=p_E)
                else:
                    pairs[offset] = TagLayouts.C("Tagblock", xn.attrib["v"],
                                                 p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag], p_E=p_E)
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_41":
                pairs[offset] = TagLayouts.C("TagRef", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_42":
                pairs[offset] = TagLayouts.C("FUNCTION", xn.attrib["v"],
                                             p_S=TagLayouts.run_parse.group_lengths_dict[xn.tag])
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_43":  #
                subthings = {}
                current_offset2 = current_offset2_temp = 0
                p_E = {}
                if xn.attrib.keys().__contains__('db1'):
                    p_E['db1'] = xn.attrib['db1']
                    p_E['db2'] = xn.attrib['db2']
                    p_E['db3'] = xn.attrib['db3']
                    p_E['db4'] = xn.attrib['db4']
                    p_E['db5'] = xn.attrib['db5']
                    p_E['db6'] = xn.attrib['db6']
                    p_E['db7'] = xn.attrib['db7']
                    p_E['db8'] = xn.attrib['db8']
                for xntwo2 in xn:
                    current_offset2 = current_offset2 + self.the_switch_statement(xntwo2, current_offset2,
                                                                                  subthings)
                    # its gonna append that to the main, rather than our struct
                pairs[offset] = TagLayouts.C("ResourceHandle", xn.attrib["v"],
                                             subthings, current_offset2, p_E=p_E)
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_44":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_45":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]
            elif xn.tag == "_69":  # unmapped - This case isn't found in any tag file
                pairs[offset] = TagLayouts.C("Comment",
                                             xn.attrib["v"] + " (unmapped type(" + xn.tag + "), may cause errors)")
                return TagLayouts.run_parse.group_lengths_dict[xn.tag]

        group_lengths_dict = {
            "_0": 32,  # _field_string
            "_1": 256,  # _field_long_string
            "_2": 4,  # _field_string_id
            "_3": 4,  # ## Not found in any tag type
            "_4": 1,  # _field_char_integer
            "_5": 2,  # _field_short_integer
            "_6": 4,  # _field_long_integer
            "_7": 8,  # _field_int64_integer
            "_8": 4,  # _field_angle
            "_9": 4,  # _field_tag
            "_A": 1,  # _field_char_enum
            "_B": 2,  # _field_short_enum
            "_C": 4,  # _field_long_enum
            "_D": 4,  # _field_long_flags
            "_E": 2,  # _field_word_flags
            "_F": 1,  # _field_byte_flags
            "_10": 4,  # _field_point_2d -- 2 2bytes?
            "_11": 4,  # _field_rectangle_2d
            "_12": 4,  # _field_rgb_color -- hex color codes - it's technically only 3 bytes but the final byte is FF
            "_13": 4,  # _field_argb_color
            "_14": 4,  # _field_real
            "_15": 4,  # _field_real_fraction
            "_16": 8,  # _field_real_point_2d
            "_17": 12,  # _field_real_point_3d
            "_18": 8,  # _field_real_vector_2d --
            "_19": 12,  # _field_real_vector_3d
            "_1A": 16,  # _field_real_quaternion
            "_1B": 8,  # _field_real_euler_angles_2d
            "_1C": 12,  # _field_real_euler_angles_3d
            "_1D": 12,  # _field_real_plane_2d
            "_1E": 16,  # _field_real_plane_3d
            "_1F": 12,  # _field_real_rgb_color
            "_20": 16,  # _field_real_argb_color
            "_21": 4,  # _field_real_hsv_colo
            "_22": 4,  # _field_real_ahsv_color
            "_23": 4,  # _field_short_bounds
            "_24": 8,  # _field_angle_bounds
            "_25": 8,  # _field_real_bounds
            "_26": 8,  # _field_real_fraction_bounds
            "_27": 4,  # ## Not found in any tag type
            "_28": 4,  # ## Not found in any tag type
            "_29": 4,  # _field_long_block_flags
            "_2A": 4,  # _field_word_block_flags
            "_2B": 4,  # _field_byte_block_flags
            "_2C": 1,  # _field_char_block_index
            "_2D": 1,  # _field_custom_char_block_index
            "_2E": 2,  # _field_short_block_index
            "_2F": 2,  # _field_custom_short_block_index
            "_30": 4,  # _field_long_block_index
            "_31": 4,  # _field_custom_long_block_index
            "_32": 4,  # ## Not found in any tag type
            "_33": 4,  # ## Not found in any tag type
            "_34": 4,  # _field_pad ## variable length
            "_35": 4,  # 'field_skip' ## iirc
            "_36": 0,  # _field_explanation
            "_37": 0,  # _field_custom
            "_38": 0,  # _field_struct
            "_39": 32,  # _field_array
            "_3A": 4,
            "_3B": 0,  # ## end of struct or something
            "_3C": 1,  # _field_byte_integer
            "_3D": 2,  # _field_word_integer
            "_3E": 4,  # _field_dword_integer
            "_3F": 8,  # _field_qword_integer
            "_40": 20,  # _field_block_v2
            "_41": 28,  # _field_reference_v2
            "_42": 24,  # _field_data_v2

            "_43": 16,  # ok _field_resource_handle

            "_44": 4,
            "_45": 4
        }
