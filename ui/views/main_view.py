import codecs
import json
import pathlib
import time

from PySide6.QtCore import QEvent, QThreadPool
from PySide6.QtWidgets import QMenu, QGroupBox, QFrame, QFormLayout, QFileDialog

from commons.logs import Log
from commons.tag_group_extension_map import map_ext
from configs.config import Config
from exporters.model.biped_exporter import BipedExporter
from exporters.model.exporter_factory import ExporterFactory
from tag_reader.readers.biped import Biped
from tag_reader.readers.reader_factory import ReaderFactory
from tag_reader.var_names import getMmr3HashFromInt, TAG_NAMES
from ui.View import View
from ui.dir_proxy import DirProxy
from ui.multithread.worker import Worker
from ui.views.list_obj_view import Ui_List_Obj_View
from ui.views.simple_obj_view import Ui_GroupBox_View
from ui.ui_main import Ui_MainWindow


class F_Ui_MainWindow(Ui_MainWindow):
    def __init__(self):
        super(F_Ui_MainWindow, self).__init__()
        # self.model = QFileSystemModel()
        self.dirProxy = DirProxy()
        # self.dirProxy.dirModel.directoryLoaded.connect(lambda: self.treeView.expandAll())
        self.dirProxy.setNameFilters(["*.model"])  # <- filtering all files and folders with "*.ai"
        self.dirProxy.createFilterList()
        self.dirProxy.dirModel.setRootPath(Config.BASE_UNPACKED_PATH.replace('\\', '/'))
        # self.treeModel = TreeModel(self.getInitialData())
        # self.model.setNameFilters(["model"])
        # self.model.setNameFilterDisables(False);
        # self.model.setRootPath(Config.BASE_UNPACKED_PATH.replace('\\', '/'))
        self.temp_widget = None
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def getInitialData(self) -> dict:
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
        frame1 = QFrame(self.scrollArea)
        self.temp_widget = Ui_List_Obj_View()
        self.temp_widget.setupUi(frame1)
        self.scrollArea.widget().layout().addWidget(frame1)
        self.temp_widget = Ui_GroupBox_View()
        temp = QGroupBox()
        self.actionFrom_Json_Them.triggered["bool"].connect(self.actionFromJsonTheme)
        self.temp_widget.setupUi(temp, {"temp": "asdasd",
                                        "asdasd": 21321,
                                        "temp1": "asdasd",
                                        "asdasd1": 21321,

                                        "asdaqwsd": 21321,
                                        "tempq1": "asdasd",
                                        "asdqwasd1": 21321,

                                        })
        self.scrollArea.widget().layout().addWidget(temp)
        frame2 = QFrame()
        temp_frame2 = Ui_List_Obj_View()
        temp_frame2.setupUi(frame2)
        self.scrollArea.widget().layout().addWidget(frame2)
        #temp.layout().addWidget(frame2)
        #temp.layout().setWidget(10, QFormLayout.LabelRole, frame2)
        Log.AddSubscribersForOnPrint(self.printInStatusBar)

    def actionFromJsonTheme(self):
        fname = QFileDialog.getOpenFileName(self.parent(), 'Open file',
                                            Config.WEB_DOWNLOAD_DATA, "Json files (*007-*.json)")

        filepath = fname[0]
        self.execute_export_from_json_theme(filepath)


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

        if event.type() == QEvent.ContextMenu and source is self.treeView:
            menu = QMenu()
            menu.addAction('View')
            menu.addAction('Export')
            menu.addAction('Export Json')
            sel_mod_index = source.selectionModel().currentIndex()
            # if self.model.isDir(sel_mod_index):
            #    return True

            temp = menu.exec(event.globalPos())
            if temp:
                if temp.text() == "Export":
                    item = self.treeView.model().itemData(sel_mod_index)
                    filename = self.treeView.model().filePath(sel_mod_index)
                    self.oh_no(filename)
                elif temp.text() == "View":
                    pass

                elif temp.text() == "Export Json":
                    filename = self.treeView.model().filePath(sel_mod_index)
                    parse_model = ReaderFactory.create_reader(filename)
                    parse_model.load()
                    json_export = parse_model.toJson()
                    saveTo = Config.EXPORT_JSON + filename.replace('/', "\\") + '.json'
                    out = pathlib.Path(saveTo.replace(saveTo.split('\\')[-1], ''))
                    out.mkdir(parents=True, exist_ok=True)
                    with open(saveTo, 'wb') as fw:
                        json.dump(json_export, codecs.getwriter('utf-8')(fw), ensure_ascii=False)
                        fw.close()
                    print(saveTo)
                    self.statusbar.showMessage(f"Save to {saveTo}")
            return True
        return super().eventFilter(source, event)

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            progress_callback.emit(n * 100 / 4)

        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def execute_export(self, filename):
        Log.Print(filename)
        parse = ReaderFactory.create_reader(filename)
        parse.load()
        exporter = ExporterFactory.create_exporter(parse)
        exporter.export()

    def execute_export_from_json_theme(self, json_path):
        Log.Print(json_path)
        try:
            with open(json_path, 'rb') as f:
                data = json.load(f)
            ref_id = getMmr3HashFromInt(data['TagId'])
            filename = TAG_NAMES[ref_id]
            parse = ReaderFactory.create_reader(filename)
            parse.load()
            model_parser = None
            exporter = ExporterFactory.create_exporter(parse)
            if isinstance(exporter, BipedExporter):
                exporter.exportByThemeJson(json_path,data)
        except Exception as e:
            Log.Print(str(e))



    def oh_no(self, filename):
        # Pass the function to execute
        worker = Worker(self.execute_export, filename)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)


class MainView(View):
    def __init__(self):
        super(MainView, self).__init__(F_Ui_MainWindow())

    def setupUi(self, Window):
        super(MainView, self).setupUi(Window)
        self.qt_ui.setupUi(Window)

    def assign_model(self):
        pass
