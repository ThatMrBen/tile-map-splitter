# 瓦片地图切割器 (Tile Map Splitter)

![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

一个用于将大图片切割成小瓦片的Python工具，适用于游戏开发、地图处理等场景。

## 📑 目录

- [功能特点](#-功能特点)
- [项目结构](#-项目结构)
- [快速开始](#-快速开始)
- [使用模式](#-使用模式)
- [完整操作流程](#-完整操作流程)
- [输入格式说明](#-输入格式说明)
- [使用示例](#-使用示例)
- [跨平台兼容性](#-跨平台兼容性)
- [系统要求](#-系统要求)
- [贡献](#-贡献)
- [许可证](#-许可证)

## ✨ 功能特点

- 🖼️ 支持多种图片格式（PNG, JPG, BMP等）
- 🔍 自动识别网格行列数
- ⚙️ 自定义瓦片尺寸
- 📍 自定义起始Y坐标
- 📝 按照 `x_y` 格式命名瓦片
- 📁 自动创建输出文件夹
- 🛡️ 完善的错误处理和用户提示

## 📁 项目结构

```
tile-map-splitter/
├── 同志们点这里/                         # 启动器目录
│   ├── Windows用户点这里.bat             # Windows一键启动
│   ├── LinuxMac用户点这里.sh             # Linux/Mac一键启动
│   ├── LinuxMac用户首次使用先点这里.sh    # Linux/Mac权限设置
│   └── 使用说明.txt                      # 简化使用说明
├── codes/                               # 源代码目录
│   ├── enhanced_tile_splitter.py        # 增强版主程序（完整功能）
│   ├── example_generator.py             # 测试图片生成器
│   └── requirements.txt                 # Python依赖
├── test-picture/                        # 测试图片目录（运行时自动创建）
├── .gitignore                           # Git忽略文件
├── LICENSE                              # MIT许可证
├── README.md                            # 项目说明文档
└── git_commands.md                      # Git命令指南
```

## 🚀 快速开始

### 安装依赖

```bash
pip install -r codes/requirements.txt
```

或者直接安装Pillow：
```bash
pip install Pillow
```

### 使用方法

1. 克隆或下载项目：
```bash
git clone https://github.com/ThatMrBen/tile-map-splitter.git
cd tile-map-splitter
```

2. 安装依赖：
```bash
# Windows/Linux/Mac
pip install -r codes/requirements.txt
```

3. 启动程序：

**Windows:**
```bash
# 双击运行
同志们点这里/Windows用户点这里.bat
```

**Linux/Mac:**
```bash
# 首次使用需要设置权限
双击 同志们点这里/LinuxMac用户首次使用先点这里.sh

# 然后启动
双击 同志们点这里/LinuxMac用户点这里.sh
```

## 🎯 使用模式

### 教程/测试模式
- 自动生成测试图片
- 详细的操作引导
- 边缘裁剪教学
- 智能瓦片尺寸推荐
- 适合初次使用和学习

### 生产模式
- 直接开始切割操作
- 需要自己准备图片
- 完整的专业功能
- 适合熟练用户

## 📝 完整操作流程

### 1. 启动阶段
- 显示欢迎界面
- 询问是否进行环境检测
- 系统环境检测（Python、依赖库、权限）
- 询问是否继续

### 2. 模式选择
- 教程/测试模式 或 生产模式
- 清屏后进入对应流程

### 3. 教程/测试模式流程
- 询问是否生成测试文件
- 生成测试图片并显示教学提示
- 询问是否开始教学

### 4. 路径配置（两种模式共同）
- 输入图片路径（必须手动输入，无默认值）
- 输入输出目录（必须手动输入，无默认值）

### 5. 边缘裁剪设置
- 询问是否需要裁剪图片边缘
- 如需要，依次询问：
  - 上边缘裁剪多少像素
  - 下边缘裁剪多少像素
  - 左边缘裁剪多少像素
  - 右边缘裁剪多少像素

### 6. 瓦片尺寸设置
- 显示智能推荐的瓦片尺寸
- 用户输入瓦片尺寸（格式：数字x数字）
- 检查是否能整除，不能则给出警告
- 设置起始Y值

### 7. 执行切割
- 显示切割进度
- 完成后显示结果
- 按任意键退出

## 输入格式说明

### 1. 输出目录
- 支持绝对路径和相对路径
- 支持用户主目录路径（`~`）
- 可以直接粘贴文件夹路径
- **Windows示例**：`C:\Files\Codes\tile-map-splitter` 或 `.\output`
- **Linux/Mac示例**：`/home/user/projects` 或 `~/Documents` 或 `./output`
- 程序会自动验证目录是否存在和是否有写入权限

### 2. 图片路径
- 支持绝对路径和相对路径
- 支持用户主目录路径（`~`）
- 支持拖拽文件到命令行窗口
- 可以直接粘贴图片路径
- **Windows示例**：`C:\path\to\image.png` 或 `.\image.png`
- **Linux/Mac示例**：`/home/user/Pictures/image.png` 或 `~/Pictures/image.png` 或 `./image.png`

### 3. 瓦片尺寸
- 格式：`数字x数字`
- 例如：`32x32`、`64x64`、`16x24`
- 必须是正整数

### 4. 确认操作
- 输入 `y` 确认切割
- 输入 `n` 取消操作

### 5. 起始Y值
- 默认为1（直接回车使用默认值）
- 可以输入任何大于等于1的整数
- 例如：`1`、`10`、`100`

## 输出说明

- 瓦片保存在：`[用户指定目录]\[图片名]_tiles\`
- 命名格式：`x_y.png`
  - x：列号，从1开始递增
  - y：行号，从起始Y值开始递增
- 文件格式：PNG

## 💡 使用示例

### 快速测试流程

1. **生成测试图片**：
```bash
python codes/example_generator.py
```

2. **运行切割器**：
```bash
python codes/tile_map_splitter.py
```

3. **输入示例**：
- 输出目录：直接回车（使用默认路径）
- 图片路径：`test-picture/example_tilemap.png`
- 瓦片尺寸：`32x32`
- 确认切割：`y`
- 起始Y值：直接回车（默认为1）

4. **结果**：
- 网格：4列 x 3行
- 生成12个瓦片：
  ```
  1_1.png  2_1.png  3_1.png  4_1.png
  1_2.png  2_2.png  3_2.png  4_2.png
  1_3.png  2_3.png  3_3.png  4_3.png
  ```

## 错误处理

程序会在以下情况终止运行：
- 图片文件不存在或无法打开
- 瓦片尺寸格式不正确
- 瓦片尺寸过大（无法切割出任何瓦片）
- 起始Y值不是有效数字
- 用户选择取消操作

## 注意事项

1. 如果图片尺寸不能被瓦片尺寸整除，剩余部分将被忽略
2. 程序会显示剩余像素的提示信息
3. 输出文件夹会自动创建，如果已存在会覆盖同名文件
4. 建议在切割前备份原图片

## 📋 系统要求

- Python 3.6+
- Pillow库
- 支持Windows、macOS、Linux

## 🌍 跨平台兼容性

### Windows
- 支持标准Windows路径格式：`C:\path\to\file`
- 支持相对路径：`.\folder\file`

### Linux/Mac
- 支持Unix路径格式：`/path/to/file`
- 支持用户主目录：`~/Documents/file`
- 支持相对路径：`./folder/file`

### 通用特性
- 自动处理路径分隔符
- 支持用户主目录展开（`~`）
- 跨平台的文件权限检查

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔗 相关链接

- [Python官网](https://www.python.org/)
- [Pillow文档](https://pillow.readthedocs.io/)

---

如果这个工具对你有帮助，请给个⭐️支持一下！
