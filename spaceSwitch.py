import maya.cmds as cmds

'''
	Space switch constraint for rigging
'''

def srcTxt(*args):
    global src
    src = cmds.ls(sl=1)
    cmds.textField(field, e=1, text=str(src))

def tgtTxt(*args):
    global trg
    trg = cmds.ls(sl=1)
    cmds.textField(field1, e=1, text=str(trg))

def ctlTxt(*args):
    global ctrl
    ctrl = cmds.ls(sl=1)[0]
    cmds.textField(field2, e=1, text=str(ctrl))

def chBoxOn(*args):
    cmds.textField(nfield, e=1, en=1)

def chBoxOff(*args):
    cmds.textField(nfield, e=1, en=0)

def prt(*args):
    state = cmds.checkBox(cbox, q=1, v=1)
    if not state:
        eNames = str(src).replace(",", ":").replace("[","").replace("]","").replace("u'","").replace("'", "").replace(" ","").upper()
    else:
        eNames = cmds.textField(nfield, q=1, text=1)
    
    cmds.addAttr(ctrl, ln="space", at="enum", enumName = eNames)
    cmds.setAttr(ctrl+".space", cb=1)
    
    grp = cmds.group(trg[0])
    
    cnst = cmds.parentConstraint(src, grp, mo=1)
    
    ud = cmds.listAttr(cnst, ud=1)
    
    for i in ud:
        idx = ud.index(i)
        cond = cmds.createNode("condition")
        cmds.setAttr(cond+".secondTerm", idx)
        cmds.setAttr(cond+".colorIfTrueR", 1)
        cmds.setAttr(cond+".colorIfFalseR", 0)
        cmds.connectAttr(ctrl+".space", cond+".firstTerm")
        cmds.connectAttr(cond+".outColorR", cnst[0]+"."+i)

'''
	Mel UI commands
'''

window = cmds.window('Space switch UI')
cmds.columnLayout( adjustableColumn=True )
field = cmds.textField(en=0, text = "source objects")
btn = cmds.button(label="<<<", command=srcTxt)
cbox = cmds.checkBox(label="useEnumNames", onc=chBoxOn, ofc=chBoxOff)
nfield = cmds.textField(en=0, text = "enum names (ex) ARM:HIP:WORLD")

field1 = cmds.textField(en=0, text = "target object")
btn1 = cmds.button(label="<<<", command=tgtTxt)
field2 = cmds.textField(en=0, text = "control objects")
btn2 = cmds.button(label="<<<", command=ctlTxt)
btnp = cmds.button(label="constraint", command=prt)

cmds.showWindow( window )
