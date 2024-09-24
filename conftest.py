import sys
import os

# 打印 Python 路径
print("Python 路径:", sys.path)

# 设置 PYTHONPATH 环境变量
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))