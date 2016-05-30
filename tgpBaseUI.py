'''
Created on June 2, 2014

@author: Eyal
'''

import maya.cmds as mc
from functools import partial

class BaseUI(object):
  
    def __init__(self):
       
        self.widgets={}
        self.window="baseWindow"
        self.title="Base Window"
        self.winSize=(500,350)
        
        
        self.createUI()
        
    def createUI(self,*args):
        
        
        #check if window and prefs exist. If yes, delete
        
        if mc.window(self.window, exists=True):
            mc.deleteUI(self.window, window=True)
        elif mc.windowPref(self.window, exists=True):
            mc.windowPref(self.window, remove=True) 
     
        #create the main window UI
        self.window=mc.window(self.window, title=self.title, 
                              widthHeight=self.winSize, 
                              sizeable=False, menuBar=True,
                              mnb=True, mxb=False)
        
        '''
        # create menu
        mc.menu(label="Edit")
        mc.menuItem(label="Reset", command=self.tgpRestart)
        '''
        #self.tabForm=mc.formLayout(bgc=(0.5,0.21,0.71))
        
       
        self.mainForm=mc.formLayout(numberOfDivisions=100)
        
        self.tagLine=mc.text(label = "Tin Girl Tools")
        self.mainColumnLayout=mc.columnLayout(rs=5,bgc=(0.21,0.21,0.21))
        
        #attach UI elements to mainForm layout
        mc.formLayout(self.mainForm, edit=True, 
                      attachForm=(
                                  (self.mainColumnLayout,"top",0),
                                  (self.mainColumnLayout,"right",0),
                                  (self.mainColumnLayout,"left",0),
                                  (self.mainColumnLayout,"bottom",30),
                                  (self.tagLine,"left",0),
                                  (self.tagLine,"right",0)
                                  ),
                      attachControl=(
                                     (self.tagLine,"top",
                                      10,self.mainColumnLayout)
                                     )
                      )
        #create custom UI elements
        
        self.createCustom(self)
        mc.setParent("..")
        
        
        
        # CONSIDER USING IF NECESSARY
        self.createCommon(self)
        mc.setParent("..")
        
        #show the window
        mc.showWindow(self.window)


    def createCommon(self,*args):
        
        #create common UI elements for all class instances
        #create default buttons
        self.cmdButtonsSize=((self.winSize[0]-30)/2,30)
        
        
        self.createButton=mc.button(label="Create",
                                    width=self.cmdButtonsSize[0],
                                    height=self.cmdButtonsSize[1],
                                    bgc=(0.3,0.7,0.4),
                                    command=partial(self.createButtonCmd)
                                    )
        self.cancelButton=mc.button(label="Cancel",
                                    width=self.cmdButtonsSize[0],
                                    height=self.cmdButtonsSize[1],
                                    bgc=(0.4,0.4,0.4),
                                    command=self.cancelButtonCmd)
        
       
        mc.formLayout(self.mainForm, e=True, af=([self.createButton,"left",5],
                                                [self.createButton,"bottom",35],
                                                [self.cancelButton,"right",5],
                                                [self.cancelButton,"bottom",35]
                                                    ),
                                                ac=([self.cancelButton,"left",5,
                                                     self.createButton])
                      )
        
       
        return
        

      
    
    def createCustom(self,*args):
        #create custom UI elements per class instance
        print "Custom window"
        #pass
    
    def createButtonCmd(self,*args):
        # override create command
        print "Button"
        
        #pass  
    
    def cancelButtonCmd(self,*args):
        #close the window
        mc.deleteUI(self.window,window=True)
        
    






'''  
    
    def resetCmd(self,*args):
        print "restart"
        
        #pass
        
    
    def createCommon(self,*args):
        
        #create common UI elements for all class instances
        #create default buttons
        self.cmdButtonsSize=((self.winSize[0]-30)/2,30)
        
        
        self.createButton=mc.button(label="Create",
                                    width=self.cmdButtonsSize[0],
                                    height=self.cmdButtonsSize[1],
                                    command=self.createButtonCmd
                                    )
        self.cancelButton=mc.button(label="Cancel",
                                    width=self.cmdButtonsSize[0],
                                    height=self.cmdButtonsSize[1],
                                    command=self.cancelButtonCmd)
        
        #attach buttons to tabForm
        
        
        mc.formLayout(self.mainForm, e=True, af=([self.createButton,"left",5],
                                                [self.createButton,"bottom",5],
                                                [self.cancelButton,"right",5],
                                                [self.cancelButton,"bottom",5]
                                                    ),
                                                ac=([self.cancelButton,"left",5,
                                                     self.createButton])
                      )
        
       
        return
   '''   
