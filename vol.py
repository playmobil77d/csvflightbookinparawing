# -*- coding: utf-8 -*-

import time

class PyVolException(Exception):
    pass

class Vol():
    def __init__(self, ddate, deco, atterro, aile, duration,
                 vtype="Vol local", hdeco="", conddeco="", condvol="", condatterro="",
                 dist="", altmax="", maxgain="", gaintotal="", lowestpt="",
                 instrument=True, encadrement="Autonome", pote="", story="", photo="", note="Pas mal"):
######### Champ obligatoire :        
        self.ddate = time.strptime(ddate,"%d/%m/%Y")        
        self.deco = deco
        self.atterro = atterro
        self.aile = aile
        self.duration = duration
######### Champ Facultatif :
        self.vtype = vtype
        #self.biplace = biplace
      
        if hdeco == "" or hdeco == "-":
            self.hdeco = ""
        else:
            self.hdeco = "%s:%s" % (time.strptime(hdeco,"%H:%M").tm_hour,time.strptime(hdeco,"%H:%M").tm_min)

        if conddeco == "" or conddeco == "-":
            self.conddeco = ""
        else:
            self.conddeco = conddeco

        if condvol == "" or condvol == "-":
            self.condvol = ""
        else:
            self.condvol = condvol
      
        if condatterro == "" or condatterro == "-":
            self.condatterro = ""
        else:
            self.condatterro = condatterro
         
        if dist == "" or dist == "-":
            self.dist = ""
        else:
            self.dist = dist
         
        if altmax == "" or altmax == "-":
            self.altmax = ""
        else:
            self.altmax = altmax
          
        if lowestpt == "" or lowestpt == "-":
            self.lowestpt = ""
        else:
            self.lowestpt = lowestpt
         
        if maxgain == "" or maxgain == "-":
            self.maxgain = ""
        else:
            self.maxgain = maxgain
         
        if gaintotal == "" or gaintotal == "-":
            self.gaintotal = ""
        else:
            self.gaintotal = gaintotal
         
        self.instument = instrument
        self.encadrement = encadrement
      
        if pote == "" or pote == "-":
            self.pote = ""
        else:
            self.pote = pote
      
        if story == "" or story == "-":
            self.story = ""
        else:
            self.story = story.replace("'", "''")
         
        self.photo = photo
        self.note = note
# ne gère pas contournement, biplace, GPS,
    
    def compareAile(self, liste_aile):
        for aile in liste_aile:
            if self.aile ==  aile:
                resultcompaile = True
                break
            else:
                resultcompaile = False
        return resultcompaile
