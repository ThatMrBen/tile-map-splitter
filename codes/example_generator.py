#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例图片生成器
用于生成测试用的瓦片地图图片
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_example_tilemap(width=128, height=96, tile_size=32, filename="example_tilemap.png", output_dir=None):
    """
    创建示例瓦片地图
    
    Args:
        width: 图片宽度
        height: 图片高度  
        tile_size: 瓦片尺寸
        filename: 输出文件名
    """
    # 创建图片
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # 计算网格
    cols = width // tile_size
    rows = height // tile_size
    
    # 绘制网格和瓦片
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink', 'lightgray']
    
    for row in range(rows):
        for col in range(cols):
            # 瓦片位置
            left = col * tile_size
            top = row * tile_size
            right = left + tile_size
            bottom = top + tile_size
            
            # 填充颜色
            color = colors[(row * cols + col) % len(colors)]
            draw.rectangle([left + 1, top + 1, right - 1, bottom - 1], fill=color)
            
            # 绘制边框
            draw.rectangle([left, top, right - 1, bottom - 1], outline='black', width=1)
            
            # 添加标签
            x_label = col + 1
            y_label = row + 1
            text = f"{x_label}_{y_label}"
            
            # 计算文字位置
            try:
                font = ImageFont.load_default()
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except:
                text_width = len(text) * 6
                text_height = 11
                font = None
            
            text_x = left + (tile_size - text_width) // 2
            text_y = top + (tile_size - text_height) // 2
            
            draw.text((text_x, text_y), text, fill='black', font=font)
    
    # 如果没有指定输出目录，询问用户
    if output_dir is None:
        import platform
        system = platform.system()
        if system == "Windows":
            example = "C:\\path\\to\\folder"
        else:
            example = "/path/to/folder 或 ~/Documents"

        print(f"请选择测试图片保存位置（例如: {example}）:")
        while True:
            output_dir = input("保存目录: ").strip()
            if not output_dir:
                print("错误：请输入保存目录")
                continue

            # 处理用户主目录路径
            output_dir = os.path.expanduser(output_dir.strip('"\''))

            # 检查目录是否存在，不存在则尝试创建
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                    print(f"✅ 已创建目录: {output_dir}")
                    break
                except Exception as e:
                    print(f"❌ 错误：无法创建目录 - {e}")
                    continue
            else:
                break

    # 保存图片到指定文件夹
    output_path = os.path.join(output_dir, filename)
    image.save(output_path, "PNG")

    print(f"示例图片已生成: {output_path}")
    print(f"图片尺寸: {width}x{height} 像素")
    print(f"瓦片尺寸: {tile_size}x{tile_size} 像素")
    print(f"网格: {cols}列 x {rows}行")
    print(f"建议切割参数: {tile_size}*{tile_size}")

    return output_path

if __name__ == "__main__":
    create_example_tilemap()
