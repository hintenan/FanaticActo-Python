import sys, csv, time, datetime
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont


class ActoData():
    def __init__(self):
        self.BWPix = 5
        self.BHPix = 10
        self.BINPERHR = 12
        self.HRPERDAY = 24
        self.BINPERDAY = self.BINPERHR * self.HRPERDAY
        self.BWSpace = 1
        self.BHSpace = 3
        self.BINSEP = 1
        self.ActoCSV = []
        self.lenDay = 0
        self.startDay = 0

    def readActoCSV(self):
        print('get')
        get = np.loadtxt(open("runner11.csv","rb"), delimiter=",", skiprows=0)
        print('get end')
        self.rawEpoch = get[:, 1]
        self.dt = np.diff(self.rawEpoch)
        plt.figure(10)
        plt.hist(self.dt, bins=np.linspace(0, 1, 101))
        plt.show()
        #print(self.rawEpoch)

    def data2Hist(self):
        result = time.localtime(self.rawEpoch[0])
        zerotime = self.rawEpoch[0] - (result.tm_hour * 60 * 60 + result.tm_min * 60 + result.tm_sec)
        print(zerotime)
        data = self.rawEpoch - zerotime - 8*60*60
        data = data / 60 / 60
        hrs = data % 24
        indDay = np.floor(data / 24)
        indDay = indDay.astype(int)
        self.lenDay = indDay[-1] + 1
        print(indDay[-1])
        self.actoHist = np.zeros(shape = (indDay[-1] + 1, 24), dtype=int)
        self.actoHistPix = np.zeros(shape = (indDay[-1] + 1, 24), dtype=int)
        for i in range(self.lenDay):
            hist, bin_edges = np.histogram(hrs[indDay == i], bins=range(25))
            #print(hist)
            self.actoHist[i, :] = hist
            maxh = np.max(hist)
            self.actoHistPix[i, :] = np.ceil(hist * 10 / (maxh + (maxh == 0)))

    def hist2Graph(self):
        actoHistPix  = self.actoHistPix

        iDay = np.arange(self.lenDay)

        indR2 = (iDay + 1) * self.BHPix + iDay * self.BHSpace # Basement
        indR1 = np.transpose(indR2 + 1 - np.transpose(self.actoHistPix))
        print(indR1)
        """
        jBin = np.arange(app.BINPERDAY * 2);
        if (app.BINSEP && app.BWSpace)
            indC1 = 1 + app.BWPix * jBin + app.BWSpace * np.fix(jBin/app.BINSEP) # Left
            indC2 = app.BWPix * jBin + app.BWSpace * np.fix(jBin/app.BINSEP)  # Right
        else
            indC1 = 1 + app.BWPix * (jBin - 1); % Left
            indC2 = a
        if 1:#app.BinSep:
            WIDTHFULLDAY = self.BINPERDAY * self.BWPix + self.BWSpace * ((self.BINPERDAY / self.BINSEP) - 1)
            oneDayPic = ones(self.BHPix, WIDTHFULLDAY, 3)
            oneDaySep = ones(self.BHSpace, WIDTHFULLDAY, 3)
        else:
            WIDTHFULLDAY = self.BINPERDAY * self.BWPix
            oneDayPic = ones(self.BHPix, WIDTHFULLDAY, 3)
            oneDaySep = ones(self.BHSpace, WIDTHFULLDAY, 3)

        # color gradien
        self.tmpbin = np.zeros(shape = (10, 5, 3))
        plt.imshow(np.ones(shape=(100, 100, 3)))
        plt.show()
        """

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("FanaticActo")

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.line = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        LoadFileButton = QPushButton('Load File', self)
        LoadFileButton.clicked.connect(self.LoadFileButtonClicked)
        LoadFileButton.setFont(QFont('Helvetica Neue', 16))
        LoadFileButton.resize(120, 60)
        LoadFileButton.move(80, 60)

        self.actoData = ActoData()


    def LoadFileButtonClicked(self):
        self.loadFile()

    def loadFile(self):
        self.actoData.readActoCSV()
        self.actoData.data2Hist()
        self.actoData.hist2Graph()





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
