import tkinter as tk
from tkinter import filedialog
from cst_python_lib.subject import *  # E:\\CST Studio Suite 2020\\AMD64\\python_cst_libraries
from cst_python_lib.materials import Materials
from cst.interface import DesignEnvironment
from cst_python_lib.postcal import Cal
from numpy.lib.scimath import sqrt 



def load_data_from_csv(filename):
    df = pd.read_csv(filename)
    return df

def wcs_face(component:str,name:str,faceid:int) -> None:
    line_break = '\n'
    sCommand = ['Pick.PickFaceFromId("%s:%s", "%d" )'%(component,name,faceid),'WCS.AlignWCSWithSelected "Face"']
    sCommand = line_break.join(sCommand)
    modelers.add_to_history('wcs_face', sCommand)

def get_row_data(df, i):
    row = df.iloc[i]
    ri1 = row['ri1']
    ro1 = row['ro1']
    ri2 = row['ri2']
    ro2 = row['ro2']
    ri3 = row['ri3']
    ro3 = row['ro3']
    rot1 = row['rot1']
    rot2 = row['rot2']
    x1 = row['x1']
    return ri1, ro1, ri2, ro2, ri3, ro3, rot1, rot2, x1

def cylinder(name,component,material,ro,ri,zrange):
        line_break = '\n'#换行
        zmin, zmax = zrange
        sCommand = ['With Cylinder ',
                '.Reset',
                '.Name "%s" '%name,
                '.Component "%s"'%component,
                '.Material "%s"'%material ,
                '.OuterRadius "%s"'%ro ,
                '.InnerRadius "%s"'%ri ,
                '.Axis "z"' ,
                '.Zrange "%s", "%s"'%(zmin,zmax) ,
                '.Xcenter "0"' ,
                '.Ycenter "0"' ,
                '.Segments "0"' ,
                '.Create',
                'End With'] 
        sCommand = line_break.join(sCommand)
        modelers.add_to_history('cylinder', sCommand)

def brick(name,component,material,xrange,yrange,zrange):
    line_break = '\n'#换行
    xmin, xmax = xrange
    ymin, ymax = yrange
    zmin, zmax = zrange
    sCommand = ['With Brick',
            '.Reset',
            '.Name "%s" '%name,
            '.Component "%s" '%component,
            '.Material "%s"'%material ,
            '.Xrange "%s", "%s"' %(xmin,xmax),
            '.Yrange "%s", "%s"'%(ymin,ymax) ,
            '.Zrange "%s", "%s"'%(zmin,zmax) ,
            '.Create',
            'End With'] 
    sCommand = line_break.join(sCommand)
    modelers.add_to_history('Brick', sCommand)


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
basic_setting.init_metasurface(Fre_start=0.1, Fre_stop=2.5)
mws.save(path=fullname, allow_overwrite=True)
set_parameter = Set_parameter(modeler=modelers)
# 创建材料
material = Materials(modeler = modelers)
material.imp_materials("PI")
material.imp_materials("Aluminum")
shape = Shape(modelers)
P=120
set_parameter.add_param("P",P)
wcs = WCS(modelers)
document = Document(modeler=modelers)
wcs.wcs_global()

# 读取CSV文件
filename = 'generated_data_2th.csv'
df = load_data_from_csv(filename)
#建模
i = 2554
ri1, ro1, ri2, ro2, ri3, ro3, rot1, rot2, x1 = get_row_data(df, i)
wcs_face('PI','sub', faceid=1)
cylinder("c1",'c1',"Aluminum",ro1,ri1,[0,0.2])
cylinder("c2",'c2',"Aluminum",ro2,ri2,[0,0.2])
cylinder("c3",'c3',"Aluminum",ro3,ri3,[0,0.2])
#yz坐标系
line_break = '\n'#换行
sCommand = ['With WCS',
        '.SetNormal "1", "0", "0"',
        '.SetUVector "0", "1", "0"',
        '.ActivateWCS "local" ',
        'End With']
sCommand = line_break.join(sCommand)
modelers.add_to_history('yz_WCS',sCommand)
angleu,component = rot1,"c2"

#旋转上开口角1
modelers.add_to_history('rotatev',f'WCS.RotateWCS "v", "{angleu}/2" ')
#切第一次
modelers.add_to_history('shape_slice',f'Solid.SliceComponent "{component}" ')
#旋转上开口角2
modelers.add_to_history('rotatev',f'WCS.RotateWCS "v", "-{angleu}" ')
#切第二次
modelers.add_to_history('shape_slice',f'Solid.SliceComponent "{component}" ')
modelers.add_to_history('d1','Solid.Delete "c2:c2_1"')


modelers.add_to_history('d1','WCS.AlignWCSWithGlobalCoordinates')
modelers.add_to_history('yz_WCS',sCommand)
angleu,component = rot2,"c3"

#旋转上开口角1
modelers.add_to_history('rotatev',f'WCS.RotateWCS "v", "{angleu}/2" ')
#切第一次
modelers.add_to_history('shape_slice',f'Solid.SliceComponent "{component}" ')
#旋转上开口角2
modelers.add_to_history('rotatev',f'WCS.RotateWCS "v", "-{angleu}" ')
#切第二次
modelers.add_to_history('shape_slice',f'Solid.SliceComponent "{component}" ')
modelers.add_to_history('d1','Solid.Delete "c3:c3_2"')
modelers.add_to_history('d1','WCS.AlignWCSWithGlobalCoordinates')
wcs_face('PI','sub', faceid=1)
brick('b1','b1','Aluminum',[-ro1,ro1],[-(sqrt(ri3**2+(ro1/2)**2)),0],[0,0.2])
modelers.add_to_history('d1','WCS.AlignWCSWithGlobalCoordinates')
wcs_face('PI','sub', faceid=1)
brick('b2','b2','Aluminum',[-x1,x1],[sqrt(ro2**2-x1**2),P/2],[0,0.2])
        #运行仿真
modelers.add_to_history('ComponentDelete','Solid.Add "b2:b2", "c2:c2"')
modelers.add_to_history('ComponentDelete','Solid.Add "c2:c2_1_1", "c2:c2_2"')
modelers.add_to_history('ComponentDelete','Solid.Add "b2:b2", "c2:c2_1_1"')
modelers.add_to_history('ComponentDelete','Solid.Add "b1:b1", "c1:c1"')
modelers.add_to_history('ComponentDelete','Solid.Add "c3:c3", "c3:c3_1"')
modelers.add_to_history('ComponentDelete','Solid.Add "c3:c3", "c3:c3_1_1"')
modelers.add_to_history('ComponentDelete','Solid.Add "b1:b1", "c3:c3"')