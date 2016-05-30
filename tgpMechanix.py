'''
Created on Jan 31, 2014

@author: Eyal
'''
import maya.cmds as mc
from math import *
from functools import partial
from tgpBaseTabUI import BaseTabUI as UI


#create UI class

class MechanixUI(UI):
    def __init__(self):
       
        self.window="mxWindow"
        self.title="tgpMechanix 1.00"
        self.winSize=(330,250)
        
        self.numberOfTabs=2
        self.name=["Spring","Piston"]
        
        #create a dictionary for the tabs
        self.tabs={}
        self.createUI()

    def createCustom(self,name,*args):
        
        
        self.tabVer=mc.tabLayout(self.tabs["uiTabs"],edit=True,
                             tabLabel=(self.tabForm,"{0}".format(name)))
        
        self.rigType=("{0}".format(name))
        
        #customize the UI to match the rig type
        if (self.rigType==self.name[0]):
                       
            mc.text(label="1. Create positioning locators")
            self.posButton=mc.button(label="Position Locators",
                                     w=(self.winSize[0]-16),
                                     h=40, bgc=(0.85,0.65,0.25),
                                     command=partial(self.checkObj,self.name[0],
                                                     "radius_CTRL","setSpring")
                                     )
            mc.text(label="2. Adjust radius of spring")
            mc.text(label="3. Click Create")
           
           
        elif (self.rigType==self.name[1]):
                        
            mc.text(label="1. Create positioning locators (at full piston extension)")
            self.posButton=mc.button(label="Position Locators",
                                     w=(self.winSize[0]-16),
                                     h=40, bgc=(0.85,0.65,0.25),
                                     command=partial(self.checkObj,self.name[1],"topRod_CTRL","setPiston")
                                     )
            mc.text(label="2. Adjust radius & position of top piston rod")
            mc.text(label="3. Adjust radius & position of bottom piston rod")
            mc.text(label="3. Click Create")
                

    def createButtonCmd(self,name,*args):
        selName=("{0}".format(name))
        
        if (selName==self.name[0]):
            #check that spring has been created
            if mc.objExists("radius_CTRL"):
                
                #pass info to create spring
                self.makeSpring()                
                
            else:
                mc.warning("Spring guides are missing!")
                
         
        elif (selName==self.name[1]):
            #check that spring has been created
            if mc.objExists("topRod_CTRL"):
                
                #pass info to create piston
                self.makePiston()                
                
            else:
                mc.warning("Piston guides are missing!")
                
    def cancelButtonCmd(self,*args):
        # 1. check if guides are present in tmp_GRP
        # 2. if yes, prompt user to proceed with cancellation or return go back to script
        if (mc.objExists("mxTmp_GRP")):
            confirmStatus=mc.confirmDialog( title="Confirm exit", message="Guides are present.\nAre you sure you want to exit?",
                              button=["Yes","No"], defaultButton="Yes",
                              cancelButton="No", dismissString="No" )
            if confirmStatus=="Yes":
                mc.delete(self.tmpGrp)
                mc.deleteUI(self.window,window=True)
            
        else:
            mc.deleteUI(self.window,window=True)            
        
    def set_connector(self,name):
    
        #create locators 
        self.baseLoc=mc.spaceLocator(name="baseLoc_{0}".format(name))[0]
        self.topLoc=mc.spaceLocator(name="topLoc_{0}".format(name))[0]
               
        #create the connecting curve
        self.conCurve=mc.curve(name="conCurve_{0}".format(name), d=1, p=[(0,0,0),(0,0,0)])
        mc.setAttr(self.conCurve+".template",1) #template the curve
        
        #move topLoc to arbitrary position at y=10 
        self.topPos=mc.move(0,10,0,self.topLoc)
                
        #connect the curve between the locators
        mc.connectAttr(self.baseLoc+".t",self.conCurve+".cv[0]", force=True)
        mc.connectAttr(self.topLoc+".t",self.conCurve+".cv[1]",force=True)
        
        #create distanceNode
        self.dNode=mc.createNode("distanceBetween", name="mxConnector_DBN")
        
        #attach the distanceNode between the locators
        mc.connectAttr(self.topLoc+".worldMatrix[0]",self.dNode+".inMatrix1",force=True)
        mc.connectAttr(self.baseLoc+".worldMatrix[0]",self.dNode+".inMatrix2",force=True)
        
        #return
    
    ##########################
    # SPRING SECTION         #
    ##########################
    
    
    def setSpring(self,*args):
        
        self.springName="spring"
    
        #create a set to put all of the spring elements inside
        self.springSetName="spring_SET"
        if mc.objExists(self.springSetName):
            print (self.springSetName + " exists.")
        else:
            mc.sets(name=self.springSetName)
        
        #create guides
        self.set_connector(self.springName)
            
        #create radius circle
        self.radCntrl=mc.circle(name="radius_CTRL",c=(0,0,0), nr=(0,1,0), 
                                sw=360, r=3, d=3, ut=0, tol=0.01, s=8, ch=1)
        #create springRadius attribute
        mc.addAttr(self.radCntrl, sn="sr", ln="springRadius", k=1, defaultValue=3.0, min=0.1, max=15)
        
        #connect the springRadius attribute to the circle
        mc.connectAttr("radius_CTRL.springRadius", "{0}.radius".format(self.radCntrl[1]))
        
        #position radCntrl between locators and aim
        
        mc.pointConstraint(self.baseLoc, self.topLoc,self.radCntrl[0])
        mc.aimConstraint(self.topLoc,self.radCntrl[0],aimVector=(0,1,0))
        
        self.lockHide(self.radCntrl[0])
        
        #create tmp group for easy deletion
        mc.select(self.baseLoc,self.topLoc,self.conCurve,self.radCntrl)
        self.selSpringObjs=mc.ls(sl=True,type="transform")
        
        self.createTmp(self.selSpringObjs)
        

    #create the spring
    def makeSpring(self,*args):
        
        
        self.springRadius=mc.getAttr("{0}.springRadius".format(self.radCntrl[0]))
        
        #get diameter (width)
        self.upWidth=self.springRadius*2
        
        #create base spring mesh using polyHelix
        self.springBase=mc.polyHelix(c=20,h=4,w=self.upWidth, r=0.2,sa=24,sco=24,
                                     sc=0,ax=(0,1,0),rcp=0,cuv=3,ch=1,
                                     name="springGeo")
        
        mc.pointConstraint(self.baseLoc,self.topLoc,self.springBase[0])
        mc.aimConstraint(self.topLoc,self.springBase[0],aimVector=(0,1,0))
        
        #connect height attribute of helix to distance node
        mc.connectAttr("{0}.distance".format(self.dNode),"{0}.height".format(self.springBase[1]),  force=True)
        
        mc.delete(self.radCntrl)
       
        mc.select(self.baseLoc,self.topLoc,self.conCurve,self.springBase)
        #select all spring parts        
        self.selection=mc.ls(sl=True)

        #loop through the parts and rename them accordingly    
        for x in self.selection:
            mc.rename(x,(x+"_#"))
    
        #create a group for the springs
        self.springGrp=mc.group(name="spring_GRP_#")
        #delete tmp group
        mc.delete(self.tmpGrp)
        #add GRP elements to set
        mc.sets(self.springGrp, add=self.springSetName)
        
        
    ##########################
    # PISTON SECTION         #
    ##########################
    
    def setPiston(self,*args):
        
        self.pistonName="piston"
        
        #create a set to put all of the piston elements inside
        self.pistonSetName="piston_SET"
        if mc.objExists(self.pistonSetName):
            print (self.pistonSetName + " exists.")
        else:
            mc.sets(name=self.pistonSetName)
            
        #create guides
        self.set_connector(self.pistonName)
        
        #create control circle
        self.topRod=mc.circle(name="topRod_CTRL",c=(0,0,0), nr=(0,1,0), 
                                sw=360, r=2, d=3, ut=0, tol=0.01, s=8, ch=1)
        
        self.botRod=mc.circle(name="bottomRod_CTRL",c=(0,0,0), nr=(0,1,0), 
                                sw=360, r=2, d=3, ut=0, tol=0.01, s=8, ch=1)
        
        #create radius and position attributes
        mc.addAttr(self.topRod, sn="tpr", ln="pistonRadius", k=1, defaultValue=3, min=0.1, max=15)
        mc.addAttr(self.topRod, sn="tpos", ln="position", at="double", k=1, defaultValue=0.45, min=0, max=1)
        mc.connectAttr("topRod_CTRL.pistonRadius", "{0}.radius".format(self.topRod[1]))

        #connect POC node and clean channelBox
        self.pocCon(self.pistonName, self.topRod)
        self.lockHide(self.topRod[0])
        
        #rinse and repeat for bottom rod
        mc.addAttr(self.botRod, sn="bpr", ln="pistonRadius", k=1, defaultValue=4.0, min=0.1, max=15)
        mc.addAttr(self.botRod, sn="bpos", ln="position", at="double", k=1, defaultValue=0.5, min=0, max=1)
        mc.connectAttr("bottomRod_CTRL.pistonRadius", "{0}.radius".format(self.botRod[1]))
        
        self.pocCon(self.pistonName, self.botRod)
        self.lockHide(self.botRod[0])
        
        #create tmp group for easy deletion
        mc.select(self.baseLoc,self.topLoc,self.conCurve,self.topRod,self.botRod)
        self.selPistonObjs=mc.ls(sl=True,type="transform")
        print self.selPistonObjs
        self.createTmp(self.selPistonObjs)
  
        
    def makePiston(self):
        
        #get radius & position channels from rods
        self.topRodRadius=mc.getAttr("{0}.pistonRadius".format(self.topRod[0]))
        self.topRodPos=mc.getAttr("{0}.position".format(self.topRod[0]))
        
        self.botRodRadius=mc.getAttr("{0}.pistonRadius".format(self.botRod[0]))
        self.botRodPos=mc.getAttr("{0}.position".format(self.botRod[0]))
        
        #get position of locators and controllers
        
        self.topLocPos=mc.objectCenter(self.topLoc,gl=True)
        self.topRadiusPos=mc.objectCenter(self.topRod[0],gl=True)
        
        self.botLocPos=mc.objectCenter(self.baseLoc, gl=True)
        self.botRadiusPos=mc.objectCenter(self.botRod[0],gl=True)
        
        
        #create a group for the piston
        # use Maya's #-sign to automatically add a number to the value, 
        #instead of adding a counter
        self.pistonGrp=mc.group(em=True,name="piston_GRP_#")     
        
        #create joints between locators
        
        self.setJoints(self.topLocPos, self.botLocPos, self.topRadiusPos, 
                       self.topLoc,self.baseLoc, self.topRodRadius,
                       "topRod",self.pistonGrp)
        
        self.setJoints(self.botLocPos, self.topLocPos, self.botRadiusPos, 
                       self.baseLoc,self.topLoc, self.botRodRadius,
                       "botRod",self.pistonGrp)

        #delete control curves
        mc.delete(self.topRod,self.botRod)
        
        #select piston controls
        mc.select(self.baseLoc,self.topLoc,self.conCurve)
        #select all piston parts        
        self.selection=mc.ls(sl=True)
        #loop through the parts and rename them accordingly    
        for x in self.selection:
            mc.rename(x,(x+"_#"))
        
        #parent to piston group
        self.newSel=mc.ls(sl=True)
        mc.parent(self.newSel,self.pistonGrp)
        #delete tmp group
        mc.delete(self.tmpGrp)
        #add GRP elements to set
        mc.sets(self.pistonGrp, add=self.pistonSetName)
        
        mc.select(clear=True)
        
    def setJoints(self,rootPos, endPos, ringPos,rConstLoc,bConstLoc,radius,jntName,pGroup):
        
        thickness = radius/3
        
        
        #clear selection
        mc.select(clear=True)
        #create joints
        joints=[]
        
        joints.append(mc.joint(position=rootPos,name=(jntName+"_root_JNT_#")))
        joints.append(mc.joint(position=ringPos,name=(jntName+"_end_JNT_#")))
       
        
        mc.joint(joints,edit=True,orientJoint="xyz",zeroScaleOrient=True,
                 secondaryAxisOrient="yup")
        
        #create IKhandle
        self.pistonIK=mc.ikHandle(sj=joints[0], ee=joints[1], 
                                  name=(jntName+"_IK_#"))
        
        #parent to locators
        mc.parent(joints[0],rConstLoc)
        
        #constrain to locators
        mc.pointConstraint(bConstLoc,self.pistonIK[0])
        
        
        #distance between 
        distance = sqrt( pow((rootPos[0]-ringPos[0]),2) + 
                         pow((rootPos[1]-ringPos[1]),2) + 
                         pow((rootPos[2]-ringPos[2]),2))
        
               
        #create pipe rod (polyPipe bug...must double the height)
        self.rod=mc.polyPipe(r=radius,t=thickness,h=(distance*2),
                             sa=20,ax=(0,1,0),cuv=3,ch=1,sc=0,
                             name=(jntName+"_geo_#"))
        #move pivot point to origin
        
        mc.xform(pivots=(0,(distance/-2),0))
        #aim and parent to joints
        mc.pointConstraint(joints[0],self.rod[0])
        mc.aimConstraint(joints[1],self.rod[0],aimVector=(0,1,0))
        
        #clear the list
        del joints[:]
        
        mc.select(self.pistonIK[0],self.rod[0])
        mc.ls(sl=True)[0]
        toGroup=mc.group(n=jntName+"_GRP_#")
        mc.parent(toGroup, pGroup)
        
       
        #return
        

        
    ###########################
    # MISC. SECTION           #
    ###########################        
  
    #lock & hide object transform attributes
    def lockHide(self, obj):
        # locks and hides all default transform attributes
        
        toLock=[".tx",".ty",".tz",".sx",".sy",".sz",".rx",".ry",".rz",".visibility"]
        for locked in range(len(toLock)):
            mc.setAttr ((obj+toLock[locked]),lock=True, keyable=False, channelBox=False)
        #return
    
    #connect control to curve
    def pocCon(self,name,ctrl):
        #create pointOnCurve node
        pocNode=mc.createNode("pointOnCurveInfo",name="POC_{0}".format(name))
        #connect POC to connector curve and ctrl
        mc.connectAttr(self.conCurve+".worldSpace",pocNode+".inputCurve", force=True)
        mc.connectAttr(pocNode+".position", ctrl[0]+".translate", force=True)
        mc.connectAttr(ctrl[0]+".position", pocNode+".parameter", force=True)
        
        #tangent constrain to curve
        mc.tangentConstraint(self.conCurve,ctrl[0], aim=(0,1,0), upVector=(0,0,1), wut="vector", wu=(0,1,0))
        
        #return
    
    #check if objects exists 
    def checkObj(self,name,checkObjName,runFunc,*args):
        
        getFuncName=format(runFunc)        
        
        if (mc.objExists(checkObjName)):
            mc.warning("{0} guides already exist!".format(name))
            
        else:
            # note, this getattr function is a python function, not Maya!
            self.callFunc=getattr(self,getFuncName) #will return self.getFuncName
            self.callFunc()

        #return
    
    #create tmpGrp
    def createTmp(self, selection,*args):
        if (mc.objExists("mxTmp_GRP")):
            mc.parent(selection,"mxTmp_GRP")
            mc.select(clear=True)
        else:
            mc.select(selection)
            self.tmpGrp=mc.group(name="mxTmp_GRP")
            mc.select(clear=True)
            
        #return
