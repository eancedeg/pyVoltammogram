import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QListWidgetItem
from ui.VoltamUI import Ui_VoltammetryWindow
from plot.volplot import MplCanvas
from parser.volffile import Voltammogram
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



class VoltWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_VoltammetryWindow()
        self.ui.setupUi(self)

        # Matplotlib
        self.matplotlib_widget = MplCanvas(self.ui.plotwidget)
        self.toolbar = NavigationToolbar(self.matplotlib_widget, self)

        layout = QVBoxLayout(self.ui.plotwidget)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.matplotlib_widget)

        # Events
        self.ui.actionOpenFile.triggered.connect(self.openfile)
        self.ui.cycles.itemClicked.connect(self.update_plot)

    def openfile(self):
        file_name = QFileDialog.getOpenFileName(self, 'Select File ...', '',
                                                'Text Files (*.txt);;All Files (*)')
        if file_name[0]:
            voltfile = Voltammogram(file_name[0])
            voltdata = voltfile.voltdata
            cycleindexdf = voltdata[voltdata['Potential'] == voltfile.lowvolt]
            cycleindex = cycleindexdf.index
            numcycles = len(cycleindex.tolist()) + 1

            for i in range(numcycles):
                if i == 0:
                    cycledata = voltdata.iloc[:cycleindex[i], :]
                    self.add_cycle(f'Cycle {i + 1}', cycledata['Potential'], cycledata['Current'])
                elif i == numcycles - 1:
                    cycledata = voltdata.iloc[cycleindex[i - 1]:, :]
                    self.add_cycle(f'Cycle {i + 1}', cycledata['Potential'], cycledata['Current'])
                else:
                    cycledata = voltdata.iloc[cycleindex[i - 1]: cycleindex[i], :]
                    self.add_cycle(f'Cycle {i + 1}', cycledata['Potential'], cycledata['Current'])

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
