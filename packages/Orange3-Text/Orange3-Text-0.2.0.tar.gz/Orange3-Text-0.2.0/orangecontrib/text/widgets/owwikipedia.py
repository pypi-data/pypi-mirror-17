from PyQt4 import QtGui, QtCore

from Orange.widgets import gui
from Orange.widgets import settings
from Orange.widgets.widget import OWWidget, Msg
from orangecontrib.text.corpus import Corpus
from orangecontrib.text.language_codes import lang2code, code2lang
from orangecontrib.text.widgets.utils import ComboBox, ListEdit, CheckListLayout
from orangecontrib.text.wikipedia import WikipediaAPI, NetworkException


class Output:
    CORPUS = "Corpus"


class OWWikipedia(OWWidget):
    """ Get articles from wikipedia. """

    name = 'Wikipedia'
    priority = 27
    icon = 'icons/Wikipedia.svg'

    outputs = [(Output.CORPUS, Corpus)]
    want_main_area = False
    resizing_enabled = False

    label_width = 1
    widgets_width = 2

    attributes = [
        # ('Content', 'content'),
        ('Title', 'title'),
        ('Summary', 'summary'),
        ('Query', 'query'),
        ('URL', 'url'),
        ('Page ID', 'pageid'),
        ('Revision ID', 'revision_id'),
    ]

    query_list = settings.Setting([])
    language = settings.Setting('en')
    corpus_variables = settings.Setting([attr[1] for attr in attributes])
    articles_per_query = settings.Setting(10)

    info_label = 'Articles count {}'

    class Error(OWWidget.Error):
        api = Msg('Api error\n{}')
        network = Msg('Connection error\n{}')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtGui.QGridLayout()

        def progress_callback(i, c):
            QtCore.QMetaObject.invokeMethod(self, "on_progress", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(float, i), QtCore.Q_ARG(int, c))

        self.api = WikipediaAPI(on_progress=progress_callback, on_finish=self.on_finish, on_error=self.on_error)
        self.result = None

        query_box = gui.hBox(self.controlArea, 'Query')

        # Queries configuration
        layout = QtGui.QGridLayout()
        layout.setSpacing(7)

        row = 0
        query_edit = ListEdit(self, 'query_list', "Each line represents a separate query.", self)
        layout.addWidget(QtGui.QLabel('Query word list:'), row, 0, 1, self.label_width)
        layout.addWidget(query_edit, row, self.label_width, 1, self.widgets_width)

        # Language
        row += 1
        language_edit = ComboBox(self, 'language', tuple(sorted(lang2code.items())))
        layout.addWidget(QtGui.QLabel('Language:'), row, 0, 1, self.label_width)
        layout.addWidget(language_edit, row, self.label_width, 1, self.widgets_width)

        # Articles per query
        row += 1
        layout.addWidget(QtGui.QLabel('Articles per query:'), row, 0, 1, self.label_width)
        slider = gui.valueSlider(query_box, self, 'articles_per_query', box='',
                                 values=[1, 3, 5, 10, 25])
        layout.addWidget(slider.box, row, 1, 1, self.widgets_width)

        query_box.layout().addLayout(layout)
        self.controlArea.layout().addWidget(query_box)

        self.controlArea.layout().addWidget(
            CheckListLayout('Text includes', self, 'corpus_variables', self.attributes, cols=2))

        self.info_box = gui.hBox(self.controlArea, 'Info')
        self.result_label = gui.label(self.info_box, self, self.info_label.format(0))

        self.button_box = gui.hBox(self.controlArea)
        self.button_box.layout().addWidget(self.report_button)

        self.search_button = gui.button(self.button_box, self, "Search", self.search)
        self.search_button.setFocusPolicy(QtCore.Qt.NoFocus)

    def send_report(self):
        if self.result:
            items = (('Language', code2lang[self.language]),
                     ('Query', self.query_list),
                     ('Articles count', len(self.result)))
            self.report_items('Query', items)

    @QtCore.pyqtSlot()
    def search(self):
        if not self.api.running:
            self.on_start()
        else:
            self.api.disconnect()

    @QtCore.pyqtSlot()
    def on_start(self):
        self.Error.api.clear()
        self.Error.network.clear()
        self.search_button.setText("Stop")
        self.progressBarInit()
        self.result_label.setText(self.info_label.format(0))
        self.api.search(lang=self.language, queries=self.query_list, attributes=self.corpus_variables,
                        articles_per_query=self.articles_per_query, async=True)

    @QtCore.pyqtSlot(float, int)
    def on_progress(self, progress, count):
        self.progressBarSet(progress)
        self.result_label.setText(self.info_label.format(count))

    @QtCore.pyqtSlot(object)
    def on_finish(self, result):
        self.result = result
        self.send(Output.CORPUS, result)
        self.result_label.setText(self.info_label.format(len(result) if result else 0))
        self.progressBarFinished()
        self.search_button.setText("Search")

    @QtCore.pyqtSlot(Exception)
    def on_error(self, error):
        if isinstance(error, NetworkException):
            self.Error.network(str(error))
        self.on_finish(None)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    widget = OWWikipedia()
    widget.show()
    app.exec()
    widget.saveSettings()
