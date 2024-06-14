# -----------------------------------------------------------------------------
# 导入所需模块
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
import cst
import time 
import random
import csv
import os
import glob
import re
from cst.interface import DesignEnvironment 
import matplotlib.pyplot as plt
import psutil
import sys
import pygetwindow as gw
from PIL import Image
import threading
import pygetwindow as gw
import win32gui
import cv2
from scipy.ndimage import binary_erosion
from scipy.spatial import ConvexHull
import ast

# -----------------------------------------------------------------------------
# 选择文件根目录
# -----------------------------------------------------------------------------
path = r"C:\Users\CHEESZ\Desktop\Test"
# 创建文件夹
folders = ["CST_DOC", "CST_OUTPUT", "PIC", "PROGRESS"]
folder_paths = []
for folder in folders:
    folder_path = os.path.join(path, folder)
    os.makedirs(folder_path, exist_ok=True)
    folder_paths.append(folder_path)
print("文件夹已创建：CST_DOC, CST_OUTPUT, PIC, PROGRESS")
# print("文件夹路径：", folder_paths)
# -----------------------------------------------------------------------------
# CST库环境设置
# -----------------------------------------------------------------------------
def import_from_previous():
    if os.path.exists('previous_import.txt'):
        with open('previous_import.txt', 'r') as file:
            previous_import = file.read()

            # 使用 threading.Event 来实现超时
            user_input = threading.Event()
            answer = None  # 初始化 answer 变量

            def get_user_choice():
                nonlocal user_input, answer
                answer = input('是否使用上次导入的地址 ' + previous_import + ' ? (y/n): ')
                user_input.set()  # 用户输入完成，设置 Event 信号

            # 创建并启动线程
            user_input_thread = threading.Thread(target=get_user_choice)
            user_input_thread.start()
            time.sleep(0.5)
            print('\n')
            # 倒计时等待用户输入，最多等待 10 秒
            for i in range(2, -1, -1):
                if user_input.is_set():
                    break
                print(f"还有{i}s时间决定")
                time.sleep(1)

            # 判断用户是否输入完成
            if user_input.is_set():
                # 用户输入完成，返回相应的结果
                if answer.lower() == 'y':
                    return previous_import
                elif answer.lower() == 'n':
                    return None

            # 用户未在超时时间内输入，自动使用上次导入的地址
            return previous_import

    return None


def save_previous_import(address):
    '''保存最后一次导入的地址'''

    with open('previous_import.txt', 'w') as file:
        file.write(address)

def get_import_address():
    '''返回导入地址'''

    previous_import = import_from_previous()
    if previous_import:
        return previous_import

    address = input('请输入cst库地址(如E:\\CST Studio Suite 2020\\AMD64\\python_cst_libraries)：')
    save_previous_import(address)
    return address

def load_data_from_csv(filename):
    df = pd.read_csv(filename)
    return df

def convert_str_to_array(coord_str):
    # 将字符串转换为数组
    return np.array(ast.literal_eval(coord_str))

def get_row_data(df, row_index):
    row = df.iloc[row_index - 1]  # 索引从0开始，所以需要减1
    x_coords1 = convert_str_to_array(row['x_coords1'])
    y_coords1 = convert_str_to_array(row['y_coords1'])
    x_coords2 = convert_str_to_array(row['x_coords2'])
    y_coords2 = convert_str_to_array(row['y_coords2'])
    x_coords3 = convert_str_to_array(row['x_coords3'])
    y_coords3 = convert_str_to_array(row['y_coords3'])
    x_coords4 = convert_str_to_array(row['x_coords4'])
    y_coords4 = convert_str_to_array(row['y_coords4'])
    
    return x_coords1, y_coords1, x_coords2, y_coords2, x_coords3, y_coords3, x_coords4, y_coords4

# 执行
address = get_import_address()
if '%s'%address not in sys.path:
    sys.path.append('%s'%address)
sys.path = list(set(sys.path))
# -----------------------------------------------------------------------------
# CST常用函数
# -----------------------------------------------------------------------------

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

def create_polygon(Name,Curve,x_coords, y_coords,):
    line_break = '\n'  # 换行
    sCommand = [
        'With Polygon',
        '.Reset',
        f'.Name "{Name}"',
        f'.Curve "{Curve}"',
        # 第一个点使用 .Point 方法，并将坐标格式化为字符串
        f'.Point "{x_coords[0]}", "{y_coords[0]}"'
    ]

    # 其余的点使用 .LineTo 方法，并将坐标格式化为字符串
    for i in range(1, len(x_coords)):
        sCommand.append(f'.LineTo "{x_coords[i]}", "{y_coords[i]}"')

    # 如果需要闭合多边形，可能需要回到第一个点
    sCommand.append(f'.LineTo "{x_coords[0]}", "{y_coords[0]}"')

    sCommand.extend(['.Create', 
        'End With'])
    modelers.add_to_history('Polygon', line_break.join(sCommand))

def ExtrudeCurve(T,name_component,curve,name,material):
    line_break = '\n'#换行
    sCommand = ['With ExtrudeCurve',
                '.Reset ',
                f'.Name "{name}" ',
                f'.Component "{name_component}" ',
                f'.Material "{material}" ',
                f'.Thickness "{T}"' ,
                '.Twistangle "0.0"' ,
                '.Taperangle "0.0"' ,
                '.DeleteProfile "True"' ,
                f'.Curve "{curve}"' ,
                '.Create',
            'End With'] 
    sCommand = line_break.join(sCommand)
    modelers.add_to_history('ExtrudeCurve', sCommand)

def ChangeColour(name,R,G,B):
    sCommand = f'''With Material 
        .Name "{name}"
        .Folder ""
        .Colour "{R}", "{G}", "{B}" 
        .Wireframe "False" 
        .Reflection "False" 
        .Allowoutline "True" 
        .Transparentoutline "False" 
        .Transparency "0" 
        .ChangeColour 
        End With'''
    modelers.add_to_history('CC', sCommand)

def wcs_face(component:str,name:str,faceid:int) -> None:
    line_break = '\n'
    sCommand = ['Pick.PickFaceFromId("%s:%s", "%d" )'%(component,name,faceid),'WCS.AlignWCSWithSelected "Face"']
    sCommand = line_break.join(sCommand)
    modelers.add_to_history('wcs_face', sCommand)

def exdata(sp:str,type:str,format:str,path:str,name:str):
    '''
    This method is uesd to export sim data

    Args:
        sp(str):SZmax(1),Zmax(1)\n
        type(str):mag,dB,real,imag,phase
        format(str):txt,csv
    '''
    line_break = '\n'
    tree = "1D Results\\S-Parameters\\" + sp
    if type == "mag":
        sCommand=['SelectTreeItem ("%s")'%tree,
            'With Plot1D',
            '.PlotView "magnitude"',
            '.Plot',
            'End With',]
        sCommand = line_break.join(sCommand)
        modelers.add_to_history('mag', sCommand)
    else:
        print("请输入mag/dB/real/imag/phase")
    
    if format == "txt":
        line_break = '\n'
        filename = name + '.txt'
        fullname = os.path.join(path,filename)
        fixed_str = fullname.replace('\\', '//')  # 将 '\' 替换为 '//'
        # print('输出文件地址为：' + fullname)  # 输出结果
        sCommand = ['SelectTreeItem ("%s")'%tree,
            'With ASCIIExport',
            '.Reset',
            '.SetfileType "csv"',
            '.FileName ("%s")'%fixed_str,
            '.Execute',
            'End With']
        sCommand = line_break.join(sCommand)
        modelers.add_to_history('txt', sCommand)

# -----------------------------------------------------------------------------
# 小工具
# -----------------------------------------------------------------------------
# 读取指定行数据
def read_specific_row(csv_file, row_number):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader):
            if index == row_number:
                return row
            
def count_csv_files(folder_path, file_pattern):
    """计算给定文件夹中符合特定模式的CSV文件数量"""
    file_path_pattern = os.path.join(folder_path, file_pattern)
    return len(glob.glob(file_path_pattern))

# 保存 i 到文件
def save_progress(i, file_path):
    with open(file_path, 'w') as file:
        file.write(str(i))

# 从文件加载 i 的值
def load_progress(file_path):
    try:
        with open(file_path, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0  # 如果文件不存在，返回默认值

def crop_white_areas(image_path):
    image = Image.open(image_path)
    image_data = image.load()
    width, height = image.size

    top_crop, bottom_crop, left_crop, right_crop = 0, 0, 0, 0

    # 上边界裁剪
    for y in range(height):
        if all(image_data[x, y] == (255, 255, 255, 255) for x in range(width)):
            top_crop += 1
        else:
            break

    # 下边界裁剪
    for y in range(height-1, 0, -1):
        if all(image_data[x, y] == (255, 255, 255, 255) for x in range(width)):
            bottom_crop += 1
        else:
            break

    # 左边界裁剪
    for x in range(width):
        if all(image_data[x, y] == (255, 255, 255, 255) for y in range(height)):
            left_crop += 1
        else:
            break

    # 右边界裁剪
    for x in range(width-1, 0, -1):
        if all(image_data[x, y] == (255, 255, 255, 255) for y in range(height)):
            right_crop += 1
        else:
            break

    cropped_image = image.crop((left_crop, top_crop, width-right_crop, height-bottom_crop))
    cropped_image.save(image_path)  # 保存裁剪后的图片
    print('成功裁剪白色区域')

# -----------------------------------------------------------------------------
# 准备开始
# -----------------------------------------------------------------------------
# 调用函数加载 now
progress_file_path = os.path.join(folder_paths[3], "progress.txt")
now = load_progress(progress_file_path)
# 仿真总数量，每50个仿真在一个CST文件里（减少硬盘占用）
num_files = 30000
n_single_sim = 30
j_num = (num_files-now)//n_single_sim

for j in range(0, j_num):
    filename = f'CST{now}_{now+n_single_sim}.cst'#这里修改为仿真文件名称
    fullname = os.path.join(folder_paths[0],filename)
    # -----------------------------------------------------------------------------
    # 频率
    # -----------------------------------------------------------------------------
    Fre_start,Fre_stop = 0.1,2.5
    de = DesignEnvironment()
    mws = de.new_mws()
    mws.save(path = fullname,allow_overwrite = True)
    modelers = mws.model3d

    # 创建材料
    line_break = '\n'#换行
    sCommand =  f'''With Material
    .Reset
    .Name "Aluminum"
    .Folder ""
    .FrqType "static"
    .Type "Normal"
    .SetMaterialUnit "Hz", "mm"
    .Epsilon "1"
    .Mu "1.0"
    .Kappa "3.56e+007"
    .TanD "0.0"
    .TanDFreq "0.0"
    .TanDGiven "False"
    .TanDModel "ConstTanD"
    .KappaM "0"
    .TanDM "0.0"
    .TanDMFreq "0.0"
    .TanDMGiven "False"
    .TanDMModel "ConstTanD"
    .DispModelEps "None"
    .DispModelMu "None"
    .DispersiveFittingSchemeEps "General 1st"
    .DispersiveFittingSchemeMu "General 1st"
    .UseGeneralDispersionEps "False"
    .UseGeneralDispersionMu "False"
    .FrqType "all"
    .Type "Lossy metal"
    .MaterialUnit "Frequency", "GHz"
    .MaterialUnit "Geometry", "mm"
    .MaterialUnit "Time", "s"
    .MaterialUnit "Temperature", "Kelvin"
    .Mu "1.0"
    .Sigma "3.56e+007"
    .Rho "2700.0"
    .ThermalType "Normal"
    .ThermalConductivity "237.0"
    .SpecificHeat "900", "J/K/kg"
    .MetabolicRate "0"
    .BloodFlow "0"
    .VoxelConvection "0"
    .MechanicsType "Isotropic"
    .YoungsModulus "69"
    .PoissonsRatio "0.33"
    .ThermalExpansionRate "23"
    .ReferenceCoordSystem "Global"
    .CoordSystemType "Cartesian"
    .NLAnisotropy "False"
    .NLAStackingFactor "1"
    .NLADirectionX "1"
    .NLADirectionY "0"
    .NLADirectionZ "0"
    .Colour "1", "1", "0"
    .Wireframe "False"
    .Reflection "False"
    .Allowoutline "True"
    .Transparentoutline "False"
    .Transparency "0"
    .Create
    End With
    '''
    modelers.add_to_history('define_Al', sCommand)

    sCommand =f'''With Material 
        .Reset 
        .Name "PI"
        .Folder ""
        .Rho "0"
        .ThermalType "Normal"
        .ThermalConductivity "0"
        .SpecificHeat "0", "J/K/kg"
        .DynamicViscosity "0"
        .UseEmissivity "True"
        .Emissivity "0"
        .MetabolicRate "0.0"
        .VoxelConvection "0.0"
        .BloodFlow "0"
        .Absorptance "0"
        .MechanicsType "Unused"
        .IntrinsicCarrierDensity "0"
        .FrqType "all"
        .Type "Normal"
        .MaterialUnit "Frequency", "THz"
        .MaterialUnit "Geometry", "um"
        .MaterialUnit "Time", "ps"
        .MaterialUnit "Temperature", "K"
        .Epsilon "3.1"
        .Mu "1"
        .Sigma "0.0"
        .TanD "0.004"
        .TanDFreq "0.0"
        .TanDGiven "True"
        .TanDModel "ConstTanD"
        .SetConstTanDStrategyEps "AutomaticOrder"
        .ConstTanDModelOrderEps "3"
        .DjordjevicSarkarUpperFreqEps "0"
        .SetElParametricConductivity "False"
        .ReferenceCoordSystem "Global"
        .CoordSystemType "Cartesian"
        .SigmaM "0"
        .TanDM "0.0"
        .TanDMFreq "0.0"
        .TanDMGiven "False"
        .TanDMModel "ConstTanD"
        .SetConstTanDStrategyMu "AutomaticOrder"
        .ConstTanDModelOrderMu "3"
        .DjordjevicSarkarUpperFreqMu "0"
        .SetMagParametricConductivity "False"
        .DispModelEps "None"
        .DispModelMu "None"
        .DispersiveFittingSchemeEps "Nth Order"
        .MaximalOrderNthModelFitEps "10"
        .ErrorLimitNthModelFitEps "0.1"
        .UseOnlyDataInSimFreqRangeNthModelEps "False"
        .DispersiveFittingSchemeMu "Nth Order"
        .MaximalOrderNthModelFitMu "10"
        .ErrorLimitNthModelFitMu "0.1"
        .UseOnlyDataInSimFreqRangeNthModelMu "False"
        .UseGeneralDispersionEps "False"
        .UseGeneralDispersionMu "False"
        .NLAnisotropy "False"
        .NLAStackingFactor "1"
        .NLADirectionX "1"
        .NLADirectionY "0"
        .NLADirectionZ "0"
        .Colour "0", "1", "1" 
        .Wireframe "False" 
        .Reflection "False" 
        .Allowoutline "True" 
        .Transparentoutline "False" 
        .Transparency "0" 
        .Create
        End With
        '''

    modelers.add_to_history('define PI', sCommand)
    # 设置单位
    sCommand = '''With Units
    .Geometry "um"
    .Frequency "THz"
    .Voltage "V"
    .Resistance "Ohm"
    .Inductance "H"
    .TemperatureUnit  "Kelvin"
    .Time "ns"
    .Current "A"
    .Conductance "Siemens"
    .Capacitance "F"
    End With'''

    # 设置环境温度
    ambient_temp_command = 'ThermalSolver.AmbientTemperature "0"'
    # 设置频率范围
    freq_range_command = 'Solver.FrequencyRange "%f","%f"'  % (Fre_start,Fre_stop)
    # 绘制盒子
    draw_box_command = 'Plot.DrawBox False'
    # 设置背景属性
    background_command = '''With Background
    .Type "Normal"
    .Epsilon "1.0"
    .Mu "1.0"
    .Rho "1.204"
    .ThermalType "Normal"
    .ThermalConductivity "0.026"
    .HeatCapacity "1.005"
    .XminSpace "0.0"
    .XmaxSpace "0.0"
    .YminSpace "0.0"
    .YmaxSpace "0.0"
    .ZminSpace "0.0"
    .ZmaxSpace "0.0"
    End With'''

    # 设置波端口边界
    wave_port_command1 = '''With Port 
     .Reset 
     .PortNumber "1" 
     .Label ""
     .Folder ""
     .NumberOfModes "1"
     .AdjustPolarization "True"
     .PolarizationAngle "0.0"
     .ReferencePlaneDistance "0"
     .TextSize "50"
     .TextMaxLimit "1"
     .Coordinates "Full"
     .Orientation "zmax"
     .PortOnBound "True"
     .ClipPickedPortToBound "False"
     .Xrange "-60", "60"
     .Yrange "-60", "60"
     .Zrange "87.652395769231", "87.652395769231"
     .XrangeAdd "0.0", "0.0"
     .YrangeAdd "0.0", "0.0"
     .ZrangeAdd "0.0", "0.0"
     .SingleEnded "False"
     .WaveguideMonitor "False"
     .Create 
End With
'''

    wave_port_command2 = '''With Port 
     .Reset 
     .PortNumber "2" 
     .Label ""
     .Folder ""
     .NumberOfModes "1"
     .AdjustPolarization "True"
     .PolarizationAngle "0.0"
     .ReferencePlaneDistance "0"
     .TextSize "50"
     .TextMaxLimit "1"
     .Coordinates "Full"
     .Orientation "zmin"
     .PortOnBound "True"
     .ClipPickedPortToBound "False"
     .Xrange "-60", "60"
     .Yrange "-60", "60"
     .Zrange "-57.652395769231", "-57.652395769231"
     .XrangeAdd "0.0", "0.0"
     .YrangeAdd "0.0", "0.0"
     .ZrangeAdd "0.0", "0.0"
     .SingleEnded "False"
     .WaveguideMonitor "False"
     .Create 
End With
'''

    # 确保参数存在并设置描述
    parameter_commands = [
            'MakeSureParameterExists "theta", "0"',
            'SetParameterDescription "theta", "spherical angle of incident plane wave"',
            'MakeSureParameterExists "phi", "0"',
            'SetParameterDescription "phi", "spherical angle of incident plane wave"'
    ]
    parameter_command = line_break.join(parameter_commands)
    # 边界条件的设置
    boundary_command = '''With Boundary
        .Xmin "periodic"
        .Xmax "periodic"
        .Ymin "periodic"
        .Ymax "periodic"
        .Zmin "expanded open"
        .Zmax "expanded open"
        .Xsymmetry "none"
        .Ysymmetry "none"
        .Zsymmetry "none"
        .ApplyInAllDirections "False"
        .OpenAddSpaceFactor "0.5"
        .XPeriodicShift "0.0"
        .YPeriodicShift "0.0"
        .ZPeriodicShift "0.0"
        .PeriodicUseConstantAngles "True"
        .SetPeriodicBoundaryAngles "theta", "phi"
        .SetPeriodicBoundaryAnglesDirection "inward"
        End With
        '''

    # FDSolver设置
    solver_command = '''With Solver 
        .Method "Hexahedral"
        .CalculationType "TD-S"
        .StimulationPort "All"
        .StimulationMode "All"
        .SteadyStateLimit "-40"
        .MeshAdaption "False"
        .AutoNormImpedance "False"
        .NormingImpedance "50"
        .CalculateModesOnly "False"
        .SParaSymmetry "False"
        .StoreTDResultsInCache  "False"
        .RunDiscretizerOnly "False"
        .FullDeembedding "False"
        .SuperimposePLWExcitation "False"
        .UseSensitivityAnalysis "False"
        End With
        '''

    # Solver设置
    solver_command2 = '''With Solver 
        .Method "Hexahedral TLM"
        .SteadyStateLimit "-40"
        .StimulationPort "1"
        .StimulationMode "1"
        .AutoNormImpedance "False"
        .NormingImpedance "50"
        .StoreTDResultsInCache  "False"
        .RunDiscretizerOnly "False"
        .SuperimposePLWExcitation "False"
        .SParaSymmetry "False"
        End With'''
    solver_command3 = '''With TlmSolver 
     .UseParallelization "True"
     .MaximumNumberOfThreads "8"
     .MaximumNumberOfCPUDevices "2"
     .RemoteCalculation "False"
     .RemotePostprocessing "False"
     .UseDistributedComputing "False"
     .MaxNumberOfDistributedComputingPorts "64"
     .DistributeMatrixCalculation "True"
     .HardwareAcceleration "False"
     .MaximumNumberOfGPUs "1"
    End With'''

    # 更改求解器类型为高频频域（HF Frequency Domain）
    change_solver_type_command = 'ChangeSolverType("HF Time Domain")'

    # 将所有命令添加到模型的历史记录
    modelers.add_to_history('Units', sCommand)
    modelers.add_to_history('Ambient Temperature', ambient_temp_command)
    modelers.add_to_history('Frequency Range', freq_range_command)
    modelers.add_to_history('Draw Box', draw_box_command)
    modelers.add_to_history('Background', background_command)
    P=120
    modelers.add_to_history('global_WCS','WCS.ActivateWCS "global"')
    brick('sub','PI',"PI",[f'-{P}/2',f'{P}/2'],[f'-{P}/2',f'{P}/2'],[0,30])
    modelers.add_to_history('Wave Port1', wave_port_command1)
    modelers.add_to_history('Wave Port2', wave_port_command2)
    modelers.add_to_history('Parameter', parameter_command)
    modelers.add_to_history('Boundary', boundary_command)
    modelers.add_to_history('Mesh', 'Mesh.SetCreator "High Frequency" ')
    modelers.add_to_history('Solver', solver_command)
    modelers.add_to_history('set PBA version','Discretizer.PBAVersion "2024043024"')
    modelers.add_to_history('Mesh', 'Mesh.SetCreator "High Frequency" ')
    modelers.add_to_history('define time domain solver parameters', solver_command2)
    modelers.add_to_history('define time domain solver acceleration', solver_command3)
    sCommand = ['UseDistributedComputingForParameters "False"',
                'MaxNumberOfDistributedComputingParameters "2"',
                'UseDistributedComputingMemorySetting "False"',
                'MinDistributedComputingMemoryLimit "0"',
                'UseDistributedComputingSharedDirectory "False"',
                'OnlyConsider0D1DResultsForDC "False"',
                ]
    sCommand = line_break.join(sCommand)
    modelers.add_to_history('wcs_face', sCommand)
    modelers.add_to_history('Change Solver Type', change_solver_type_command)
    # 基础设置
    ChangeColour('PI',1,0,0)
    ChangeColour('Aluminum',"0.752941", "0.752941", "0.752941")

    first_iteration = True
    for i in range(now, now+n_single_sim):
        if first_iteration:
            windows_now = now
            first_iteration = False
        print(f"当前进度为{i}/{num_files-1}")
        # -----------------------------------------------------------------------------
        # 导入生成数据集
        # -----------------------------------------------------------------------------


        
        # 读取CSV文件
        filename = 'generated_data.csv'
        df = load_data_from_csv(filename)
        #建模

        x_coords1, y_coords1, x_coords2, y_coords2, x_coords3, y_coords3, x_coords4, y_coords4 = get_row_data(df, i)
        wcs_face('PI','sub', faceid=1)
        create_polygon("TestPolygon1", "Curve1", x_coords1 + 5, y_coords1 + 5)
        create_polygon("TestPolygon2", "Curve2", -x_coords2 - 5, y_coords2 + 5)
        create_polygon("TestPolygon3", "Curve3", -x_coords3 - 5, -y_coords3 - 5)
        create_polygon("TestPolygon4", "Curve4", x_coords4 + 5, -y_coords4 - 5)
        wcs_face('PI','sub', faceid=1)
        ExtrudeCurve("0.2","al","Curve1","al1","Aluminum")
        wcs_face('PI','sub', faceid=1)
        ExtrudeCurve("0.2","al","Curve2","al2","Aluminum")
        wcs_face('PI','sub', faceid=1)
        ExtrudeCurve("0.2","al","Curve3","al3","Aluminum")
        wcs_face('PI','sub', faceid=1)
        ExtrudeCurve("0.2","al","Curve4","al4","Aluminum")
        #运行仿真

        try:
            modelers.run_solver(timeout=200)
        except RuntimeError:
            # 忽略运行时错误
            pass
     
        exdata(sp="S2,1",type="mag",format="txt",path=folder_paths[1],name=f"output{i}")        
        modelers.add_to_history('detresult','DeleteResults')
        modelers.add_to_history('ComponentDelete','Component.Delete "al" ')
        now=i
        save_progress(now, progress_file_path)
    # mws.close()
    mws.save(allow_overwrite=True)
    de.close()
    