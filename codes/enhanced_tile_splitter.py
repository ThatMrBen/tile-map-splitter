#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版瓦片地图切割器
支持边缘裁剪、智能推荐等功能
"""

import os
import sys
import platform
import re
from PIL import Image


def clear_screen():
    """清屏"""
    system = platform.system()
    if system == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def wait_for_user(message="按回车键继续..."):
    """等待用户按键"""
    try:
        input(message)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)

class EnhancedTileMapSplitter:
    def __init__(self):
        self.image = None
        self.image_path = ""
        self.output_dir = ""
        self.tile_width = 0
        self.tile_height = 0
        self.start_y = 1
        self.crop_edges = False
        self.crop_left = 0
        self.crop_top = 0
        self.crop_right = 0
        self.crop_bottom = 0
    
    def get_input_output_paths(self, tutorial_mode=False, test_image_path=None):
        """获取输入输出路径"""
        clear_screen()
        print("=" * 60)
        print("                        路径配置")
        print("=" * 60)
        print()

        # 获取操作系统信息（在函数开始就获取）
        system = platform.system()

        # 获取图片路径
        while True:
            if tutorial_mode and test_image_path:
                print(f"💡 教程提示：已生成测试图片")
                print(f"   测试图片路径: {test_image_path}")
                print(f"   您可以使用此路径，或选择其他图片进行测试")
                print()

            # 根据操作系统显示路径示例
            if system == "Windows":
                example = "C:\\path\\to\\image.png"
            else:
                example = "/path/to/image.png 或 ~/Pictures/image.png"
            
            print(f"请输入图片文件路径（例如: {example}）")
            image_path = input("图片路径: ").strip()
            
            if not image_path:
                print("❌ 错误：请输入图片路径")
                continue
            
            # 处理用户主目录路径
            image_path = os.path.expanduser(image_path.strip('"\''))
            
            if not os.path.exists(image_path):
                print(f"❌ 错误：文件不存在 - {image_path}")
                continue
            
            try:
                with Image.open(image_path) as img:
                    img.verify()
                self.image_path = image_path
                break
            except Exception as e:
                print(f"❌ 错误：无法打开图片文件 - {e}")
        
        print(f"✅ 图片路径: {self.image_path}")
        print()
        
        # 获取输出路径
        while True:
            if system == "Windows":
                example = "C:\\output\\folder"
            else:
                example = "/output/folder 或 ~/Documents/output"
            
            print(f"请输入输出目录路径（例如: {example}）")
            output_dir = input("输出路径: ").strip()
            
            if not output_dir:
                print("❌ 错误：请输入输出目录路径")
                continue
            
            # 处理用户主目录路径
            output_dir = os.path.expanduser(output_dir.strip('"\''))
            
            # 检查目录是否存在，不存在则尝试创建
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                    print(f"✅ 已创建输出目录: {output_dir}")
                except Exception as e:
                    print(f"❌ 错误：无法创建目录 - {e}")
                    continue
            
            # 检查写入权限
            test_file = os.path.join(output_dir, "test_write.tmp")
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                self.output_dir = output_dir
                break
            except Exception as e:
                print(f"❌ 错误：没有写入权限 - {e}")
        
        print(f"✅ 输出路径: {self.output_dir}")
        return True
    
    def load_and_analyze_image(self):
        """加载并分析图片"""
        try:
            self.image = Image.open(self.image_path)
            print(f"✅ 图片加载成功")
            print(f"   尺寸: {self.image.width} x {self.image.height} 像素")
            print(f"   格式: {self.image.format}")
            print(f"   模式: {self.image.mode}")
            return True
        except Exception as e:
            print(f"❌ 图片加载失败: {e}")
            return False
    
    def configure_edge_cropping(self):
        """配置边缘裁剪"""
        clear_screen()
        print("=" * 60)
        print("                    边缘裁剪设置")
        print("=" * 60)
        print()

        # 确保图片已加载
        if not self.image:
            print("正在加载图片...")
            try:
                self.image = Image.open(self.image_path)
            except Exception as e:
                print(f"❌ 图片加载失败: {e}")
                return False

        # 显示图片解析结果
        print("图片解析结果：")
        self.load_and_analyze_image()
        print()

        print("有时图片边缘可能有不需要的内容（如边框、水印等）")
        print("您可以选择裁剪掉这些边缘部分。")
        print()
        
        crop_choice = input("是否需要裁剪图片边缘？(y/n): ").strip().lower()
        
        if crop_choice == 'y':
            self.crop_edges = True
            print()
            print("请输入要裁剪的像素数（留空表示0）:")

            try:
                top = input("上边缘裁剪多少像素: ").strip()
                self.crop_top = int(top) if top else 0

                bottom = input("下边缘裁剪多少像素: ").strip()
                self.crop_bottom = int(bottom) if bottom else 0

                left = input("左边缘裁剪多少像素: ").strip()
                self.crop_left = int(left) if left else 0

                right = input("右边缘裁剪多少像素: ").strip()
                self.crop_right = int(right) if right else 0
                
                # 计算裁剪后的尺寸
                new_width = self.image.width - self.crop_left - self.crop_right
                new_height = self.image.height - self.crop_top - self.crop_bottom
                
                if new_width <= 0 or new_height <= 0:
                    print("❌ 错误：裁剪参数过大，会导致图片尺寸为0")
                    self.crop_edges = False
                    return
                
                print(f"✅ 裁剪后尺寸: {new_width} x {new_height} 像素")
                
            except ValueError:
                print("❌ 错误：请输入有效的数字")
                self.crop_edges = False
        else:
            self.crop_edges = False
            print("跳过边缘裁剪")

    def get_tile_size_recommendations(self):
        """获取瓦片尺寸推荐"""
        # 计算实际图片尺寸（考虑裁剪）
        if self.crop_edges:
            width = self.image.width - self.crop_left - self.crop_right
            height = self.image.height - self.crop_top - self.crop_bottom
        else:
            width = self.image.width
            height = self.image.height
        
        # 常见的瓦片尺寸
        common_sizes = [16, 24, 32, 48, 64, 96, 128, 256]
        recommendations = []
        
        for size in common_sizes:
            if width >= size and height >= size:
                cols = width // size
                rows = height // size
                if cols > 0 and rows > 0:
                    remainder_w = width % size
                    remainder_h = height % size
                    perfect = remainder_w == 0 and remainder_h == 0
                    recommendations.append({
                        'size': size,
                        'cols': cols,
                        'rows': rows,
                        'total': cols * rows,
                        'remainder_w': remainder_w,
                        'remainder_h': remainder_h,
                        'perfect': perfect
                    })
        
        return recommendations, width, height
    
    def configure_tile_size(self):
        """配置瓦片尺寸"""
        clear_screen()
        print("=" * 60)
        print("                       瓦片尺寸设置")
        print("=" * 60)
        print()

        # 先加载图片以获取尺寸信息
        if not self.image:
            print("正在加载图片...")
            try:
                self.image = Image.open(self.image_path)
            except Exception as e:
                print(f"❌ 图片加载失败: {e}")
                return False

        # 显示图片解析结果
        print("图片解析结果：")
        self.load_and_analyze_image()

        # 显示裁剪信息
        if self.crop_edges:
            print(f"✅ 已应用边缘裁剪")
            print(f"   原始尺寸: {self.image.width} x {self.image.height} 像素")
            cropped_width = self.image.width - self.crop_left - self.crop_right
            cropped_height = self.image.height - self.crop_top - self.crop_bottom
            print(f"   裁剪后尺寸: {cropped_width} x {cropped_height} 像素")
        else:
            print("ℹ️  未应用边缘裁剪")
        print()

        recommendations, width, height = self.get_tile_size_recommendations()

        print(f"用于切割的图片尺寸: {width} x {height} 像素")
        print()
        print("推荐的瓦片尺寸:")
        print("-" * 50)
        
        for i, rec in enumerate(recommendations[:5], 1):  # 只显示前5个推荐
            status = "✅ 完美整除" if rec['perfect'] else f"⚠️  剩余 {rec['remainder_w']}x{rec['remainder_h']} 像素"
            print(f"{i}. {rec['size']}x{rec['size']} -> {rec['cols']}列 x {rec['rows']}行 = {rec['total']}个瓦片 {status}")
        
        print("-" * 50)
        print()
        
        while True:
            size_input = input("请输入瓦片尺寸（格式：宽x高，如32x32）: ").strip()

            # 解析瓦片尺寸
            pattern = r'^(\d+)x(\d+)$'
            match = re.match(pattern, size_input)

            if not match:
                print("❌ 错误：格式不正确，请使用 数字x数字 格式（如：32x32）")
                continue
            
            self.tile_width = int(match.group(1))
            self.tile_height = int(match.group(2))
            
            if self.tile_width <= 0 or self.tile_height <= 0:
                print("❌ 错误：瓦片尺寸必须大于0")
                continue
            
            if self.tile_width > width or self.tile_height > height:
                print("❌ 错误：瓦片尺寸不能大于图片尺寸")
                continue
            
            # 计算切割结果
            cols = width // self.tile_width
            rows = height // self.tile_height
            remainder_w = width % self.tile_width
            remainder_h = height % self.tile_height
            
            print(f"✅ 瓦片尺寸: {self.tile_width} x {self.tile_height}")
            print(f"   网格: {cols}列 x {rows}行")
            print(f"   总瓦片数: {cols * rows}")
            
            if remainder_w > 0 or remainder_h > 0:
                print(f"⚠️  警告: 图片无法完全整除")
                if remainder_w > 0:
                    print(f"   宽度剩余: {remainder_w} 像素")
                if remainder_h > 0:
                    print(f"   高度剩余: {remainder_h} 像素")
                print("   剩余部分将被忽略")
                
                if not input("是否继续？(y/n): ").strip().lower() == 'y':
                    continue
            
            break
        
        # 获取起始Y值
        print()
        start_y_input = input("请输入起始Y值（默认为1，直接回车使用默认值）: ").strip()
        if start_y_input:
            try:
                self.start_y = int(start_y_input)
                if self.start_y < 1:
                    print("起始Y值设为1")
                    self.start_y = 1
            except ValueError:
                print("无效输入，使用默认值1")
                self.start_y = 1
        else:
            self.start_y = 1
        
        print(f"✅ 起始Y值: {self.start_y}")

    def perform_splitting(self):
        """执行切割操作"""
        clear_screen()
        print("=" * 60)
        print("                         执行切割")
        print("=" * 60)
        print()
        
        # 应用边缘裁剪
        if self.crop_edges:
            print("应用边缘裁剪...")
            left = self.crop_left
            top = self.crop_top
            right = self.image.width - self.crop_right
            bottom = self.image.height - self.crop_bottom
            self.image = self.image.crop((left, top, right, bottom))
            print(f"✅ 裁剪完成，新尺寸: {self.image.width} x {self.image.height}")
        
        # 计算切割参数
        cols = self.image.width // self.tile_width
        rows = self.image.height // self.tile_height
        total_tiles = cols * rows
        
        # 创建输出文件夹
        image_name = os.path.splitext(os.path.basename(self.image_path))[0]
        output_folder = os.path.join(self.output_dir, f"{image_name}_tiles")
        os.makedirs(output_folder, exist_ok=True)
        
        print(f"输出文件夹: {output_folder}")
        print(f"开始切割 {total_tiles} 个瓦片...")
        print()
        
        # 执行切割
        tile_count = 0
        for row in range(rows):
            for col in range(cols):
                # 计算瓦片位置
                left = col * self.tile_width
                top = row * self.tile_height
                right = left + self.tile_width
                bottom = top + self.tile_height
                
                # 切割瓦片
                tile = self.image.crop((left, top, right, bottom))
                
                # 计算文件名
                x = col + 1
                y = self.start_y + row
                filename = f"{x}_{y}.png"
                filepath = os.path.join(output_folder, filename)
                
                # 保存瓦片
                try:
                    tile.save(filepath, "PNG")
                    tile_count += 1
                    
                    # 显示进度
                    progress = (tile_count / total_tiles) * 100
                    print(f"进度: {tile_count}/{total_tiles} ({progress:.1f}%) - {filename}")
                    
                except Exception as e:
                    print(f"❌ 保存失败 {filename}: {e}")
                    return False
        
        print()
        print(f"✅ 切割完成！共生成 {tile_count} 个瓦片")
        print(f"保存位置: {output_folder}")
        return True
    
    def run(self, tutorial_mode=False, test_image_path=None):
        """运行主程序"""
        try:
            # 1. 获取输入输出路径
            if not self.get_input_output_paths(tutorial_mode, test_image_path):
                return False

            wait_for_user("路径配置完成，按回车键继续...")

            # 2. 配置边缘裁剪
            self.configure_edge_cropping()

            # 3. 配置瓦片尺寸
            self.configure_tile_size()

            wait_for_user("配置完成，按回车键开始切割...")

            # 4. 执行切割
            success = self.perform_splitting()

            return success

        except Exception as e:
            print(f"❌ 程序运行出错: {e}")
            return False

def show_welcome():
    """显示欢迎界面"""
    clear_screen()
    print("=" * 60)
    print("                      瓦片地图切割器")
    print("                    Tile Map Splitter")
    print("=" * 60)
    print()
    print("欢迎使用瓦片地图切割器！")
    print("这是一个用于将大图片切割成小瓦片的工具。")
    print()
    print("支持功能：")
    print("• 智能瓦片尺寸推荐")
    print("• 边缘裁剪功能")
    print("• 实时切割进度显示")
    print("• 跨平台兼容")
    print()
    print("由本先森Ben（ThatMrBen）研发")
    print("他的github主页：https://github.com/ThatMrBen")
    print("项目主页：https://github.com/ThatMrBen/tile-map-splitter")
    print("喜欢的话点一个star~")
    print("=" * 60)

def ask_continue(message="是否继续？"):
    """询问用户是否继续"""
    while True:
        choice = input(f"{message} (y/n): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            print("程序已退出")
            sys.exit(0)
        else:
            print("请输入 y 或 n")

def select_mode():
    """选择使用模式"""
    clear_screen()
    print("=" * 60)
    print("                       选择使用模式")
    print("=" * 60)
    print()
    print("请选择使用模式:")
    print()
    print("1. 教程/测试模式")
    print("   - 自动生成测试图片")
    print("   - 详细的操作引导")
    print("   - 适合初次使用和学习")
    print()
    print("2. 生产模式")
    print("   - 直接开始切割操作")
    print("   - 需要自己准备图片")
    print("   - 适合熟练用户")
    print()
    print("=" * 60)

    while True:
        try:
            choice = input("请输入选择 (1-2): ").strip()
            if choice == '1':
                return 'tutorial'
            elif choice == '2':
                return 'production'
            else:
                print("无效选择，请输入 1 或 2")
        except KeyboardInterrupt:
            print("\n程序被用户中断")
            sys.exit(0)

def run_tutorial_mode():
    """运行教程/测试模式"""
    clear_screen()
    print("=" * 60)
    print("                       教程/测试模式")
    print("=" * 60)
    print()

    # 询问是否生成测试文件
    print("教程模式将生成一个测试图片用于演示切割功能。")
    if ask_continue("是否生成教程/测试文件？"):
        print("正在生成测试文件...")

        # 生成测试图片
        try:
            from example_generator import create_example_tilemap
            image_path = create_example_tilemap()
            print(f"✅ 测试图片生成成功: {image_path}")
        except Exception as e:
            print(f"❌ 测试图片生成失败: {e}")
            wait_for_user()
            return False

        print()
        print("📋 教学提示:")
        print(f"   - 测试图片已保存到: {image_path}")
        print("   - 建议瓦片尺寸: 32x32")
        print("   - 图片尺寸: 128x96 像素")
        print("   - 预期结果: 4列 x 3行 = 12个瓦片")
        print("   - 您可以复制上面的路径，或选择其他图片")

        if ask_continue("是否开始教学？"):
            splitter = EnhancedTileMapSplitter()
            return splitter.run(tutorial_mode=True, test_image_path=image_path)

    return False

def run_production_mode():
    """运行生产模式"""
    clear_screen()
    print("=" * 60)
    print("                         生产模式")
    print("=" * 60)
    print()
    print("生产模式将直接启动切割器，请确保您已准备好要切割的图片。")
    print()

    if ask_continue("是否开始切割操作？"):
        splitter = EnhancedTileMapSplitter()
        return splitter.run(tutorial_mode=False)

    return False

def main():
    """主函数"""
    try:
        # 1. 显示欢迎界面
        show_welcome()
        if not ask_continue("是否开始使用瓦片地图切割器？"):
            return

        # 2. 选择使用模式
        mode = select_mode()
        clear_screen()

        # 3. 根据模式运行程序
        if mode == 'tutorial':
            success = run_tutorial_mode()
        else:
            success = run_production_mode()

        # 4. 程序结束
        print()
        print("=" * 60)
        if success:
            print("程序执行完成")
        else:
            print("程序执行中断")
        print("感谢使用瓦片地图切割器！")

    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序发生错误: {e}")

    wait_for_user("按回车键退出...")

if __name__ == "__main__":
    main()
