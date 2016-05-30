'''
Created on Feb 9, 2014

@author: Eyal
'''

import maya.cmds as mc
from functools import partial

class BaseTabUI(object):
  
    def __init__(self):
       
        self.widgets={}
        self.window="uiWindow"
        self.title="Base Tab Window"
        self.winSize=(500,350)
        
        self.numberOfTabs=4
        self.name=["firstTab","secondTab","thirdTab","fourthTab"]
        
        #create a dictionary for the tabs
        self.tabs={}
        
        self.createUI()
        
    def createUI(self,*args):
        
        
        #check if window and prefs exist. If yes, delete
        
        if mc.window(self.window, exists=True):
            mc.deleteUI(self.window, window=True)
        elif mc.windowPref(self.window, exists=True):
            mc.windowPref(self.window, remove=True) 
            
       
        
        # error check if the numberOfTabs is equal to the name[]
        if (self.numberOfTabs!=len(self.name)):
                mc.warning("# of tabs and names are not equal!") 
                pass
        else:
            
            #create the main window UI
            self.window=mc.window(self.window, title=self.title, 
                                  widthHeight=self.winSize, 
                                  sizeable=False, menuBar=True,
                                  mnb=True, mxb=False)
            
           
            self.mainForm=mc.formLayout(numberOfDivisions=100)
            self.tagLine=mc.text(label = "Tin Girl Tools")
                                   
            self.tabs["uiTabs"]=mc.tabLayout(innerMarginWidth=20, 
                                             innerMarginHeight=20,
                                             parent=self.mainForm)
            
            #attach UI elements to mainForm layout
            mc.formLayout(self.mainForm, edit=True,
                          attachForm=(
                                      (self.tabs["uiTabs"],"top",0),
                                      (self.tabs["uiTabs"],"left",0),
                                      (self.tabs["uiTabs"],"right",0),
                                      (self.tabs["uiTabs"],"bottom",30),
                                      (self.tagLine, "left", 0),
                                      (self.tagLine, "right", 0)                                      
                                      ),
                          attachControl=(
                                         (self.tagLine,"top",10,
                                          self.tabs["uiTabs"])
                                         )
                          )
            
            
            #dynamically create number of tabs
            for x in range(self.numberOfTabs):
               
                self.tabForm=mc.formLayout(bgc=(0.21,0.21,0.21))
                
                
                #rename tabs according to name array
                self.tabName=mc.tabLayout(self.tabs["uiTabs"],edit=True,
                             tabLabel=(self.tabForm,self.name[x]), 
                             parent=self.mainForm)
                
                self.currentName=self.name[x]
                
                self.innerTabForm=mc.formLayout()
                
                mc.formLayout(self.tabForm, edit=True,
                          attachForm=(
                                      [self.innerTabForm,"top",3],
                                      [self.innerTabForm,"left",3],
                                      [self.innerTabForm,"right",3],
                                      [self.innerTabForm,"bottom",36]
                                      )
                          )
                
                #columnLayout for each tab
                self.tabColLayout=mc.columnLayout(rs=5,parent=self.innerTabForm) 

                #create custom UI elements
                self.createCustom(self.currentName)
                
                mc.formLayout(self.innerTabForm,e=True,
                              attachForm=(
                                          (self.tabColLayout,"top",3),
                                          (self.tabColLayout,"left",3),
                                          (self.tabColLayout,"right",3),
                                          (self.tabColLayout,"bottom",3)
                                           ))
                
                mc.setParent("..") #for self.tabColLayout
                
                mc.setParent("..") #for self.innerTabForm
        
                #create common UI elements
                self.createCommon(self.currentName)
                
                
                mc.setParent("..") #for self.tabName
                
            
            #show the window
            mc.showWindow(self.window)

  
    def createCommon(self,name,*args):
        
        #create common UI elements for all class instances
        #create default buttons
        self.cmdButtonsSize=((self.winSize[0]-30)/2,30)
        
        
        self.createButton=mc.button(label="Create",
                                    width=self.cmdButtonsSize[0],
                                    height=self.cmdButtonsSize[1],
                                    bgc=(0.3,0.7,0.4),
                                    command=partial(self.createButtonCmd,
                                                    self.currentName)
                                    )
        self.cancelButton=mc.button(label="Cancel",
                                    width=self.cmdButtonsSize[0],
                                    height=self.cmdButtonsSize[1],
                                    bgc=(0.4,0.4,0.4),
                                    command=self.cancelButtonCmd)
        
        #attach buttons to tabForm
        
        
        mc.formLayout(self.tabForm, e=True, af=([self.createButton,"left",5],
                                                [self.createButton,"bottom",5],
                                                [self.cancelButton,"right",5],
                                                [self.cancelButton,"bottom",5]
                                                    ),
                                                ac=([self.cancelButton,"left",5,
                                                     self.createButton])
                      )
        
       
        return
        
    
    def createCustom(self,name,*args):
        #create custom UI elements per class instance
        print ("Custom UI elements for {0}".format(name))
        pass
        
        
    def createButtonCmd(self,name,*args):
        # override create command
        print ("Create command pressed in {0}".format(name))
        
        pass  
    
    def cancelButtonCmd(self,*args):
        #close the window
        mc.deleteUI(self.window,window=True)
        






