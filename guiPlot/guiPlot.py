#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('WXAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas

import pylab, wx, random, numpy as np

class GeraNum(object):
    def __init__(self, init = 0, mult = 1):
        self.num = init
        self.mult = mult

    def update(self):
        self.num += random.uniform(-0.5, 0.5) * self.mult
        return self.num

class MainWindow(wx.Frame):
    ''' baseado em https://github.com/eliben/code-for-blog/blob/master/2008/wx_mpl_dynamic_graph.py '''

    def __init__(self, titulo):
        # cria uma nova janela
        wx.Frame.__init__(self, parent=None, title=titulo, size=(1280, 720))

        self.elementos = 100 # tamanho da lista

        # inicia a sequência randomica
        self.geranum = GeraNum()
        self.data = [self.geranum.update()]

        self.configMenu()
        self.configPanel()

        self.draw_timer = wx.Timer(self) # temporizador para a atualização dos dados
        self.Bind(wx.EVT_TIMER, self.drawPlot, self.draw_timer) # associa o temporizador à função drawPlot
        self.draw_timer.Start(100) # intervalo: 0.1s

        self.Centre() # app centralizada
        self.Show() # mostra a app

    def configMenu(self):
        menu_file = wx.Menu() # menu File

        item_save = menu_file.Append(wx.ID_SAVE, "&Save plot\tCtrl-S", "Save plot to file") # Save -> ctrl S
        self.Bind(wx.EVT_MENU, self.onSavePlot, item_save) # associa o item_save à função onSavePlot()

        item_quit = menu_file.Append(wx.ID_EXIT, "&Quit\tCtrl-Q", "Quit application") # Quit -> ctrl Q
        self.Bind(wx.EVT_MENU, self.onQuit, item_quit) # associa item_quit à função onQuit()

        self.menubar = wx.MenuBar() # barra de menu
        self.menubar.Append(menu_file, "&File") # adiciona File à barra de menu
        self.SetMenuBar(self.menubar)

        # self.CreateStatusBar() # barra de status

    def configPanel(self):
        self.panel = wx.Panel(self)

        self.initPlot() # configura o gráfico

        self.canvas = FigCanvas(self.panel, wx.ID_ANY, self.fig)

        self.vbox = wx.BoxSizer()
        self.vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW) # resize

        self.panel.SetSizer(self.vbox)

    def initPlot(self):
        self.fig = Figure((3.0, 3.0), dpi=100) # 3x3 in, 100 dpi

        self.axes = self.fig.add_subplot(111)
        self.axes.grid(True, color='gray')

        c = (_map(54, 0, 255, 0, 1),)*3 # cinza: hex #363636 ou RGB(54,54,54)

        self.axes.set_axis_bgcolor(c) # background(54)
        # self.axes.set_title('Title', size=12)

        # marcadores
        pylab.setp(self.axes.get_xticklabels(), fontsize=8, family="sans-serif")
        pylab.setp(self.axes.get_yticklabels(), fontsize=8, family="sans-serif")

        c = (_map(255, 0, 255, 0, 1), _map(220, 0, 255, 0, 1), _map(15, 0, 255, 0, 1)) # amarelo: hex #ffdc0f ou RGB(255,220,15)

        self.plot_data = self.axes.plot(self.data, linewidth=1, color=c)[0] # linha

    def drawPlot(self, evet):

        self.data.append(self.geranum.update()) # próximo número aleatório

        # mantém a lista de dados com N elementos
        if len(self.data) > self.elementos:
            del self.data[0: -self.elementos]

        # máx e min dos eixos
        xmax = len(self.data) if len(self.data) > self.elementos else self.elementos
        xmin = xmax - self.elementos

        ymin = round(min(self.data), 0) - 1
        ymax = round(max(self.data), 0) + 1

        # define os limites dos eixos
        self.axes.set_xbound(lower=xmin, upper=xmax)
        self.axes.set_ybound(lower=ymin, upper=ymax)

        self.plot_data.set_xdata(np.arange(len(self.data)))
        self.plot_data.set_ydata(np.array(self.data))

        self.canvas.draw()

    def onSavePlot(self, event):
        pass

    def onQuit(self, event):
        self.Destroy() # fecha a app

def _map(value, start1, stop1, start2, stop2):
    ''' baseada na função map()  - Processing - https://www.processing.org/reference/map_.html '''
    return start2 + (stop2 - start2) * (float(value - start1) / (stop1 - start1))

def main():
    app = wx.App(False) # cria uma nova app sem redirecionar stdout/stderr para uma janela
    app.frame = MainWindow("mavPyX4")
    app.MainLoop() # inicia a app

if __name__ == '__main__':
    main()