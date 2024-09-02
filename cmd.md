# UpinfoPy 项目命令

## 安装和设置

poetry install


## 运行所有任务

poetry run all

## 构建和发布

poetry publish --build

## 其他常用命令

## 项目初始化和依赖管理

poetry new project_name    # 创建新项目
poetry init                # 在现有项目中初始化 Poetry
poetry add package_name    # 添加依赖
poetry remove package_name # 移除依赖
poetry update              # 更新所有依赖

## 构建和发布

poetry build               # 构建项目
poetry publish             # 发布项目到 PyPI

## 环境管理

poetry env use python3.9   # 指定 Python 版本
poetry shell               # 激活虚拟环境
poetry run python script.py # 在虚拟环境中运行命令

## 项目信息

poetry show                # 显示已安装的包
poetry show --tree         # 显示依赖树
poetry check               # 检查 pyproject.toml 是否有效

## 配置管理

poetry config --list       # 列出所有配置
poetry config key value    # 设置配置项

## 版本管理

poetry version             # 显示当前版本
poetry version patch       # 增加补丁版本号
poetry version minor       # 增加次版本号
poetry version major       # 增加主版本号

## 项目特定任务

poetry run test            # 运行测试
poetry run build           # 运行构建任务
poetry run install         # 运行安装任务
poetry run publish         # 运行发布任务
