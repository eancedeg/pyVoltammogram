from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
plt.style.use('ggplot')


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        figure = Figure()
        super().__init__(figure)
        self.setParent(parent)

        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel('V (mV)')
        self.axes.set_ylabel('i (mA)')
        self.axes.set_title('Cyclic Voltammogram')
