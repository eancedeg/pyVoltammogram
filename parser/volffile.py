from datetime import datetime
import pandas as pd


class Voltammogram(object):
    def __init__(self, file):
        self.file = file
        self.date = ''
        self.technique = ''
        self.voltdata = []

        line = 'Data'
        data_section = False
        header = True
        with open(self.file) as volt:
            while line:
                if header:
                    # Date
                    line = volt.readline().strip()
                    self.date = datetime.strptime(line, '%b. %d, %Y   %H:%M:%S')

                    # Technique
                    self.technique = volt.readline().strip()

                    for i in range(6):
                        volt.readline()

                    # Voltammogram parameters
                    self.initvolt = float(volt.readline().split('=')[1])
                    self.highvolt = float(volt.readline().split('=')[1])
                    self.lowvolt = float(volt.readline().split('=')[1])
                    self.scandir = volt.readline().split('=')[1].strip()
                    self.scanrate = float(volt.readline().split('=')[1])
                    self.segments = int(volt.readline().split('=')[1])
                    self.sample_interval = float(volt.readline().split('=')[1])

                    while not data_section:
                        line = volt.readline()
                        if 'Potential/V, Current/A' in line:
                            line = volt.readline()
                            header = False
                            data_section = True
                if data_section:
                    line = volt.readline()
                    if line:
                        linedata = [[float(v.strip()), float(i.strip())] for v, i in [line.split(',')]]
                        self.voltdata.append(linedata[0])
        self.voltdata = pd.DataFrame(self.voltdata, columns=['Potential', 'Current'])

    def get_cycles(self):
        index_df = self.voltdata[self.voltdata['Potential'] == self.lowvolt]
        indexes = index_df.index
        numcycles = len(indexes.tolist()) + 1

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


if __name__ == '__main__':
    v = Voltammogram('../src/cv sb-5(-1800a1400) 200 mvs.txt')
    print(v.voltdata)
