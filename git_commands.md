# Git 命令指南

## 初始化Git仓库并上传到GitHub

1. 初始化Git仓库：
git init

2. 添加所有文件：
git add .

3. 创建第一次提交：
git commit -m "Initial commit: Cross-platform Tile Map Splitter tool"

4. 添加远程仓库：
git remote add origin https://github.com/ThatMrBen/tile-map-splitter.git

5. 推送到GitHub：
git push -u origin main

## 后续更新

1. 添加修改的文件：
git add .

2. 提交更改：
git commit -m "描述你的更改"

3. 推送到GitHub：
git push

## 常用Git命令

- 查看状态：git status
- 查看提交历史：git log
- 查看差异：git diff
- 创建分支：git checkout -b new-branch
- 切换分支：git checkout branch-name
- 合并分支：git merge branch-name

## 注意事项

- .gitignore 文件已配置，会自动忽略 __pycache__ 等不需要的文件
- 确保在GitHub上创建了对应的仓库
- 第一次推送使用 -u 参数设置上游分支
