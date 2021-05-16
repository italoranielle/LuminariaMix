# -*- coding: utf-8 -*-
"""
Created on Sat May  1 21:00:08 2021

@author: pc_lab
"""

from tkinter import *
import audio2rgb
import os
import time

class Application:
    def __init__(self, master=None):
        
        self.torgb = audio2rgb.ToRGB()
        
        self.ctTitulo = Frame(master)
        self.ctTitulo["pady"] = 10
        self.ctTitulo.pack()
        
        self.ctList = Frame(master)  
        self.ctList["padx"] = 20
        self.ctList.pack()
        
        self.ctTipo = Frame(master)
        self.ctTipo["pady"] = 10
        self.ctTipo["padx"] = 20
        self.ctTipo.pack()
        
        
        
        
        self.lbTitulo = Label(self.ctTitulo, text="Luminária mix")
        self.lbTitulo["font"] = ("Arial", "10", "bold")
        self.lbTitulo.pack()
        
        self.scrollbar = Scrollbar(self.ctList)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        
        self.lbLista = Listbox(self.ctList)
        self.lbLista["height"] = 7
        self.lbLista["width"] = 52
        self.lbLista.config(yscrollcommand = self.scrollbar.set)
        self.listarMusicas()
        self.lbLista.pack()
        
        self.btAnt = Button(self.ctTipo)
        self.btAnt["text"] = "Anterior"
        self.btAnt["height"] = 5
        self.btAnt["width"] = 10
        self.btAnt["command"] = self.anterior
        self.btAnt.pack(side=LEFT)
        
        self.btPlay = Button(self.ctTipo)
        self.btPlay["text"] = "Play"
        self.btPlay["height"] = 5
        self.btPlay["width"] = 10
        self.btPlay["command"] = self.lerArquivo
        self.btPlay.pack(side=LEFT)
        
        self.btPrx = Button(self.ctTipo)
        self.btPrx["text"] = "Proximo"
        self.btPrx["height"] = 5
        self.btPrx["width"] = 10
        self.btPrx["command"] = self.proximo
        self.btPrx.pack(side=LEFT)
        
        self.btMic = Button(self.ctTipo)
        self.btMic["text"] =  "microfone"
        self.btMic["height"] = 5
        self.btMic["width"] = 10
        self.btMic["command"] = self.lerMicrofone
        self.btMic.pack(side=LEFT)
        
           
    def btStatus(self):    
        if self.torgb.playing:
            self.btPlay["text"] = "Parar"
        else:
            self.btPlay["text"] = "Play"

    
    def lerMicrofone(self):
        self.torgb.playMic()
        self.btStatus()

        
    def lerArquivo(self):
        self.torgb.playFile(arquivo = r'./musicas/'+ str(self.lbLista.get(self.lbLista.curselection())))
        time.sleep(0.1)
        self.btStatus()
        
    def listarMusicas(self):
        musicas = [arq for arq in os.listdir(r'./musicas') if arq.lower().endswith(".wav")]
        n = 0
        for musica in musicas:
            self.lbLista.insert(n,musica)
            n+=1
            
    def proximo(self):
        self.btStatus()
        self.torgb.setPause()
        try:
            selecionado = self.lbLista.curselection()[0]
            self.lbLista.select_set(selecionado+1)
            self.lbLista.selection_clear(selecionado)
        except:
            self.lbLista.activate(0)
        self.torgb.playFile(arquivo = r'./musicas/'+ str(self.lbLista.get(self.lbLista.curselection()))) 

        
    def anterior(self):
        self.btStatus()
        self.torgb.setPause()
        time.sleep(0.1)
        try:
            selecionado = self.lbLista.curselection()[0]
            self.lbLista.select_set(selecionado-1)
            self.lbLista.selection_clear(selecionado)
        except:
            self.lbLista.activate(0)
        self.torgb.playFile(arquivo = r'./musicas/'+ str(self.lbLista.get(self.lbLista.curselection())))

    
        
root = Tk()
Application(root)
root.mainloop()