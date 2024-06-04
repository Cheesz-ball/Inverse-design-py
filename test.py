import tkinter as tk
from tkinter import filedialog
from cst_python_lib.subject import *  # E:\\CST Studio Suite 2020\\AMD64\\python_cst_libraries
from cst_python_lib.materials import Materials
from cst.interface import DesignEnvironment
from cst_python_lib.postcal import Cal


cal = Cal()

path = r"C:\Users\CHEESZ\OneDrive\Github\Inverse-design-py"
filename = "test"
fullname = os.path.join(path, filename)

de = DesignEnvironment()
mws = de.new_mws()
mws.save(path=fullname, allow_overwrite=True)
modelers = mws.model3d
# 基础设置
basic_setting = Basic(modeler=modelers)
basic_setting.init_metasurface(Fre_start=0.1, Fre_stop=2, num=1000)
mws.save(path=fullname, allow_overwrite=True)
set_parameter = Set_parameter(modeler=modelers)
# 创建材料
material = Materials(modeler = modelers)
material.imp_materials("PI")
material.imp_materials("Aluminum")
shape = Shape(modelers)
P=220
set_parameter.add_param("P",P)
wcs = WCS(modelers)
document = Document(modeler=modelers)
wcs.wcs_global()
shape.brick('sub','PI',"Polyimide (lossy)",['-P/2','P/2'],['-P/2','P/2'],[0,30])
########################修改结构绘制代码#########################

R,r,w,l,x2,x1 = [92,  61, 14, 40, -7, -20]
shape.Qshape(5,R,r,w,l,x2,x1,0.2)

