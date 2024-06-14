import numpy as np
import pandas as pd

# 定义一个函数来随机生成满足条件的整数数据
def generate_data():
    while True:
        # 随机生成整数数据
        ro3 = np.random.randint(40, 61)
        ri3 = ro3 - 5 - np.random.randint(0, 51)
        ro2 = ri3 - 10 - np.random.randint(0, 41)
        ri2 = ro2 - 5 - np.random.randint(0, 31)
        ro1 = ri2 - 10 - np.random.randint(0, 21)
        ri1 = 0
        rot1 = np.random.randint(10, 175)
        rot2 = np.random.randint(10, 175)
        x1_max = int(ri3 * np.sin(np.deg2rad(rot2 / 2))) + 1

        if ro1 < 5:
            continue
        if ri2 * np.sin(np.deg2rad(rot1 / 2)) - ro1 < 2 :
            continue
        if x1_max <= 5:
            continue  # 如果计算出的x1上限不合理，则重新生成数据
        x1 = np.random.randint(5, x1_max)
        if (x1+2)**2 > ro2**2-ri2**2:
            continue
        # 检查所有生成的参数是否大于0
        if min(ro1, ri2, ro2, ri3, ro3, rot1, rot2, x1) > 0:
            return {'ri1': ri1, 'ro1': ro1, 'ri2': ri2, 'ro2': ro2, 'ri3': ri3, 'ro3': ro3, 'rot1': rot1, 'rot2': rot2, 'x1': x1}

# 将数据保存到CSV文件
def save_data_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# 从CSV文件加载数据
def load_data_from_csv(filename):
    try:
        df = pd.read_csv(filename)
        return df.to_dict(orient='records')
    except FileNotFoundError:
        return []

# 生成唯一数据
def generate_unique_data(existing_data, num_samples):
    unique_data = existing_data
    print(len(unique_data),"unique")
    while len(unique_data) < num_samples:
        new_data = generate_data()
        if new_data not in unique_data:
            unique_data.append(new_data)
    return unique_data

# 主程序流程
filename = 'generated_data_2th.csv'
existing_data = load_data_from_csv(filename)
num_new_samples = 20000
if num_new_samples > 0:
    updated_data = generate_unique_data(existing_data, num_new_samples)
    # print(updated_data)
    save_data_to_csv(updated_data, filename)
