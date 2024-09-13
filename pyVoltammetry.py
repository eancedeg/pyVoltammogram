import sys
import pandas as pd
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QListWidgetItem, QMessageBox, QMenu
from ui.VoltamUI import Ui_VoltammetryWindow
from plot.volplot import MplCanvas
from parser.volffile import Voltammogram
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class VoltWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_VoltammetryWindow()
        self.ui.setupUi(self)
        self.file = ''

        # Matplotlib
        self.matplotlib_widget = MplCanvas(self.ui.plotwidget)
        self.toolbar = NavigationToolbar(self.matplotlib_widget, self)

        layout = QVBoxLayout(self.ui.plotwidget)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.matplotlib_widget)

        # Events
        self.ui.actionOpenFile.triggered.connect(self.openfile)
        self.ui.cycles.itemClicked.connect(self.update_plot)
        self.ui.savecycle.clicked.connect(self.savecycle)

    def savecycle(self):
        if self.ui.cycles.count():
            currentitem = self.ui.cycles.currentItem()
            x_data, y_data = currentitem.data(100)
            itemdf = pd.DataFrame({'Potential': x_data, 'Current': y_data})

            if self.file:
                filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '',
                                                          'CSV Files(*.csv);;All Files(*)')
                if filename:
                    if filename.endswith('.csv'):
                        itemdf.to_csv(filename, index=None)
                    else:
                        itemdf.to_csv(f'{filename}.csv', index=None)
                else:
                    QMessageBox.warning(self, 'File Error', 'You need to select file name path to save '
                                                            'cycle')
            else:
                QMessageBox.warning(self, 'Data warning', 'There are no voltammogram file loaded')
        else:
            QMessageBox.warning(self, 'Cycles Warning', 'There are no cycles opened')

    def openfile(self):
        file_name = QFileDialog.getOpenFileName(self, 'Select File ...', '',
                                                'Text Files (*.txt);;All Files (*)')
        if file_name[0]:
            voltfile = Voltammogram(file_name[0])
            self.file = file_name[0]

            # Fill Data
            self.ui.initv.setText(f'{voltfile.initvolt} V')
            self.ui.lowv.setText(f'{voltfile.lowvolt} V')
            self.ui.highv.setText(f'{voltfile.highvolt} V')
            self.ui.initpn.setText(f'{voltfile.scandir}')
            self.ui.scanrate.setText(f'{voltfile.scanrate * 1000}')
            self.ui.segments.setText(f'{voltfile.segments}')
            ##############################################

            cycles = voltfile.get_cycles()
            for cycle in range(len(cycles)):
                self.add_cycle(f'Cycle: {cycle + 1}', cycles[cycle]['Potential'], cycles[cycle]['Current'])

    def update_plot(self, item):
        mydata = item.data(100)
        if mydata:
            x_data, y_data = mydata
            self.matplotlib_widget.axes.clear()

            self.matplotlib_widget.figure.subplots_adjust(right=0.99, left=0.15)

            self.matplotlib_widget.axes.plot(x_data, y_data)
            self.matplotlib_widget.axes.set_xlabel('V (mV)')
            self.matplotlib_widget.axes.set_ylabel('i (mA)')
            self.matplotlib_widget.axes.set_title('Cyclic Voltammogram')
            self.matplotlib_widget.draw()

    def add_cycle(self, name, x_data, y_data):
        # print(f'Storing data: {name}, X -> {x_data}, Y -> {y_data}')
        item = QListWidgetItem(name)
        item.setData(100, (x_data, y_data))
        self.ui.cycles.addItem(item)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = VoltWindow(None)
    window.show()
    sys.exit(app.exec_())
