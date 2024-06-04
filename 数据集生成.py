import numpy as np
import random
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import binary_erosion
from scipy.spatial import ConvexHull

def generate_8_connected_shape(canvas_size, target_area):
    canvas = np.zeros((canvas_size, canvas_size), dtype=int)
    start_x = random.randint(0, canvas_size - 1)
    start_y = random.randint(0, canvas_size - 1)
    canvas[start_x, start_y] = 1
    current_area = 1
    boundary_points = [(start_x, start_y)]
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    while current_area < target_area and boundary_points:
        bx, by = random.choice(boundary_points)
        random.shuffle(neighbors)
        expanded = False
        
        for dx, dy in neighbors:
            nx, ny = bx + dx, by + dy
            if 0 <= nx < canvas_size and 0 <= ny < canvas_size and canvas[nx, ny] == 0:
                canvas[nx, ny] = 1
                boundary_points.append((nx, ny))
                current_area += 1
                expanded = True
                break
        
        if not expanded:
            boundary_points.remove((bx, by))
    
    return canvas

def process_shape(canvas_size, target_area_min):
    target_area = random.randint(target_area_min, canvas_size * canvas_size)
    canvas = generate_8_connected_shape(canvas_size, target_area)

    # 查找轮廓
    canvas_uint8 = canvas.astype(np.uint8) * 255
    contours, _ = cv2.findContours(canvas_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到最大轮廓
    max_contour = max(contours, key=cv2.contourArea)

    # 多边形逼近
    epsilon = 0.01 * cv2.arcLength(max_contour, True)
    approx = cv2.approxPolyDP(max_contour, epsilon, True)

    # 绘制最大轮廓和多边形逼近
    max_polygon_image = np.zeros_like(canvas_uint8)
    cv2.drawContours(max_polygon_image, [approx], -1, 255, 1)

    # 检测边缘
    eroded_image = binary_erosion(canvas)
    edges = canvas - eroded_image

    # 获取边缘点的坐标
    edge_points = np.argwhere(edges)

    # 使用 ConvexHull 生成多边形轮廓
    hull = ConvexHull(edge_points)

    # 获取坐标
    x_coords = (edge_points[hull.vertices, 1]) * 10
    y_coords = (canvas_size - edge_points[hull.vertices, 0] - 1) * 10

    return x_coords, y_coords

def generate_unique_data(existing_data, n, canvas_size=6, target_area_min=9):
    data = existing_data.copy()
    data_set = set(str(entry) for entry in existing_data)

    while len(data) < len(existing_data) + n:
        x_coords1, y_coords1 = process_shape(canvas_size, target_area_min)
        x_coords2, y_coords2 = process_shape(canvas_size, target_area_min)
        x_coords3, y_coords3 = process_shape(canvas_size, target_area_min)
        x_coords4, y_coords4 = process_shape(canvas_size, target_area_min)

        entry = {
            "x_coords1": x_coords1.tolist(),
            "y_coords1": y_coords1.tolist(),
            "x_coords2": x_coords2.tolist(),
            "y_coords2": y_coords2.tolist(),
            "x_coords3": x_coords3.tolist(),
            "y_coords3": y_coords3.tolist(),
            "x_coords4": x_coords4.tolist(),
            "y_coords4": y_coords4.tolist()
        }

        entry_str = str(entry)

        if entry_str not in data_set:
            data.append(entry)
            data_set.add(entry_str)
    
    return data

def save_data_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def load_data_from_csv(filename):
    df = pd.read_csv(filename)
    data = df.to_dict(orient='records')
    return data

# 加载已有数据
filename = 'generated_data.csv'
try:
    existing_data = load_data_from_csv(filename)
except FileNotFoundError:
    existing_data = []

# 生成数据
num_new_samples = 1000
updated_data = generate_unique_data(existing_data, num_new_samples)
save_data_to_csv(updated_data, filename)
