from PySide6.QtWidgets import QLabel, QFormLayout

from ui.ui_simple_obj import Ui_GroupBox


class Ui_GroupBox_View(Ui_GroupBox):
    def __init__(self):
        super(Ui_GroupBox_View, self).__init__()

    def setupUi(self, GroupBox, dictonary: dict):
        super(Ui_GroupBox_View, self).setupUi(GroupBox)
        i = 0
        for key in dictonary.keys():
            if not (dictonary[key] is list) and not (dictonary[key] is dict):
                temp_label_name = QLabel(GroupBox)
                temp_label_name.setObjectName(u"label_name"+str(key))
                temp_label_name.setText(str(key))
                self.formLayout.setWidget(i, QFormLayout.LabelRole, temp_label_name)

                temp_label_value = QLabel(GroupBox)
                temp_label_value.setObjectName(u"label_value"+str(key))
                temp_label_value.setText(str(dictonary[key]))
                self.formLayout.setWidget(i, QFormLayout.FieldRole, temp_label_value)
                i+=1


