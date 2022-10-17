import codecs
import fnmatch
import json
import os
import pathlib

from IPython.core.inputtransformer import tr
from PySide6.QtCore import QDir, QEvent, QSortFilterProxyModel
from PySide6.QtWidgets import QFileSystemModel, QMenu

from commons.logs import Log
from commons.tag_group_extension_map import map_ext
from configs.config import Config
from exporters.model.exporter_factory import ExporterFactory
from tag_reader.readers.reader_factory import ReaderFactory
from ui.View import View
from ui.simpletreemodel import TreeModel
from ui.ui_main import Ui_MainWindow


class DirProxy(QSortFilterProxyModel):
    nameFilters = ''

    def __init__(self):
        super().__init__()
        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(Config.BASE_UNPACKED_PATH.replace('\\', '/'))
        self.dirModel.setFilter(
            QDir.NoDotAndDotDot | QDir.Dirs | QDir.Files)  # <- added QDir.Files to view all files
        self.filterList = []

        self.setSourceModel(self.dirModel)

    def filePath(self, index):
        source = self.index(index.row(), 0, index.parent())
        path = []
        str_path = ""
        while source.row()!=-1:
            path.append(self.itemData(source))
            parcial_path = self.itemData(source)[0]
            str_separetor = '/'
            if parcial_path.__contains__("."):
                str_separetor = ''
            str_path = parcial_path + str_separetor+str_path
            source = source.parent()

        str_path = str_path.replace(parcial_path+'/', '')


        # t = self.dirModel.filePath(index)
        return str_path


    def createFilterList(self):
        path = Config.BASE_UNPACKED_PATH.replace('\\', '/')
        temp = pathlib.Path(path).rglob(self.nameFilters[0])
        for path_r in temp:
            dir_path = os.path.dirname(str(path_r))
            if not self.filterList.__contains__(dir_path):
                self.filterList.append(dir_path)

            if not self.filterList.__contains__(str(path_r)):
                self.filterList.append(str(path_r))

    def setNameFilters(self, filters):
        if not isinstance(filters, (tuple, list)):
            filters = [filters]
        self.nameFilters = filters
        self.invalidateFilter()

    def hasChildren(self, parent):
        sourceParent = self.mapToSource(parent)
        if not self.dirModel.hasChildren(sourceParent):
            return False
        qdir = QDir(self.dirModel.filePath(sourceParent))
        return bool(qdir.entryInfoList(qdir.NoDotAndDotDot | qdir.AllEntries | qdir.AllDirs))

    def filterAcceptsRow(self, row, parent):
        source = self.dirModel.index(row, 0, parent)
        if source.isValid():
            s_temp = self.dirModel.filePath(source)
            #return self.filterList.__contains__(s_temp)
            return  self.recursiveFind(self.dirModel.filePath(source))
        return True

    def recursiveFind(self, path: str):
        if path.__contains__(Config.BASE_UNPACKED_PATH.replace('\\', '/')[0:-1]):
            if os.path.isdir(path):

                #if self.nameFilters:
                #   qdir.setNameFilters(self.nameFilters)
                temp = pathlib.Path(path).rglob(self.nameFilters[0])
                for path_r in temp:
                    return True
                return False
            elif self.nameFilters:  # <- index refers to a file
                return fnmatch.fnmatch(path, self.nameFilters[0])
        return False


class F_Ui_MainWindow(Ui_MainWindow):
    def __init__(self):
        super(F_Ui_MainWindow, self).__init__()
        #self.model = QFileSystemModel()
        self.dirProxy = DirProxy()
        #self.dirProxy.dirModel.directoryLoaded.connect(lambda: self.treeView.expandAll())
        self.dirProxy.setNameFilters(["*.model"])  # <- filtering all files and folders with "*.ai"
        self.dirProxy.createFilterList()
        self.dirProxy.dirModel.setRootPath(Config.BASE_UNPACKED_PATH.replace('\\', '/'))
        #self.treeModel = TreeModel(self.getInitialData())
        #self.model.setNameFilters(["model"])
        #self.model.setNameFilterDisables(False);
        #self.model.setRootPath(Config.BASE_UNPACKED_PATH.replace('\\', '/'))

    def getInitialData(self)->dict:
        result = {}
        path = Config.BASE_UNPACKED_PATH
        temp = pathlib.Path(path).rglob(f"*.*")
        for path_r in temp:
            debug = True
        return result
        for key in map_ext:
            temp = pathlib.Path(path).rglob(f"*.{map_ext[key]}")
            for path_r in temp:
                result[key] = ['']
                break
        return result




    def setupUi(self, MainWindow):
        super(F_Ui_MainWindow, self).setupUi(MainWindow)
        self.treeView.installEventFilter(self)

        self.treeView.setModel(self.dirProxy)
        root_index = self.dirProxy.dirModel.index(Config.BASE_UNPACKED_PATH.replace('\\', '/'))
        proxy_index = self.dirProxy.mapFromSource(root_index)
        self.treeView.setRootIndex(proxy_index)
        """
        self.treeView.setModel(self.treeModel )
        """
        self.treeView.expanded.connect(self.tree_expanded)
        self.lineEdit.setText("*.model")
        self.lineEdit.editingFinished.connect(self.editingFinishedFilter)
        Log.AddSubscribersForOnPrint(self.printInStatusBar)

    def printInStatusBar(self, message):
        self.statusbar.showMessage(message)

    def editingFinishedFilter(self):
        print(self.lineEdit.text())
        self.dirProxy.setNameFilters([self.lineEdit.text()])

    def tree_expanded(self, index):

        item = self.treeView.model().itemData(index)
        debug = index
        self.treeView.resizeColumnToContents(0)

    def eventFilter(self, source, event):

        if event.type() == QEvent.ContextMenu  and source is self.treeView:
            menu = QMenu()
            menu.addAction('View')
            menu.addAction('Export')
            menu.addAction('Export Json')
            sel_mod_index = source.selectionModel().currentIndex()
            #if self.model.isDir(sel_mod_index):
            #    return True

            temp = menu.exec(event.globalPos())
            if temp:
                if temp.text() == "Export":
                    item = self.treeView.model().itemData(sel_mod_index)
                    filename = self.treeView.model().filePath(sel_mod_index)
                    parse = ReaderFactory.create_reader(filename)
                    parse.load()
                    exporter = ExporterFactory.create_exporter(parse)
                    exporter.export()
                elif temp.text() == "View":
                    pass

                elif temp.text() == "Export Json":
                    filename = self.treeView.model().filePath(sel_mod_index)
                    parse_model = ReaderFactory.create_reader(filename)
                    parse_model.load()
                    json_export = parse_model.toJson()
                    saveTo = Config.EXPORT_JSON + filename.replace('/',"\\") + '.json'
                    out = pathlib.Path(saveTo.replace(saveTo.split('\\')[-1], ''))
                    out.mkdir(parents=True, exist_ok=True)
                    with open(saveTo, 'wb') as fw:
                        json.dump(json_export, codecs.getwriter('utf-8')(fw), ensure_ascii=False)
                        fw.close()
                    print(saveTo)
                    self.statusbar.showMessage(f"Save to {saveTo}")
            return True
        return super().eventFilter(source, event)


class MainView(View):
    def __init__(self):
        super(MainView, self).__init__(F_Ui_MainWindow())

    def setupUi(self, Window):
        super(MainView, self).setupUi(Window)
        self.qt_ui.setupUi(Window)

    def assign_model(self):
        pass
