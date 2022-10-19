import fnmatch
import os
import pathlib

from PySide6.QtCore import QSortFilterProxyModel, QDir
from PySide6.QtWidgets import QFileSystemModel

from configs.config import Config


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
        while source.row() != -1:
            path.append(self.itemData(source))
            parcial_path = self.itemData(source)[0]
            str_separetor = '/'
            if parcial_path.__contains__("."):
                str_separetor = ''
            str_path = parcial_path + str_separetor + str_path
            source = source.parent()

        str_path = str_path.replace(parcial_path + '/', '')

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
            # return self.filterList.__contains__(s_temp)
            return self.recursiveFind(self.dirModel.filePath(source))
        return True

    def recursiveFind(self, path: str):
        if path.__contains__(Config.BASE_UNPACKED_PATH.replace('\\', '/')[0:-1]):
            if os.path.isdir(path):

                # if self.nameFilters:
                #   qdir.setNameFilters(self.nameFilters)
                temp = pathlib.Path(path).rglob(self.nameFilters[0])
                for path_r in temp:
                    return True
                return False
            elif self.nameFilters:  # <- index refers to a file
                return fnmatch.fnmatch(path, self.nameFilters[0])
        return False
