#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

class MainWindow(wx.Frame):
    def __init__(self, titulo):
        wx.Frame.__init__(self, parent=None, title=titulo, size=(1280, 720)) # cria uma nova janela

        self.config_panel()

        self.Centre()
        self.Show()

    def config_panel(self):
        self.panel = wx.Panel(self)

def main():
    app = wx.App(False) # cria uma nova app sem redirecionar stdout/stderr para a janela
    app.frame = MainWindow("mavPyX4")
    app.MainLoop() # inicia a app

if __name__ == '__main__':
    main()
