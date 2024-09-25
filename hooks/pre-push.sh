#!/bin/bash

# 生成唯一的执行 ID
EXECUTION_ID=$(date +%s%N)

# 获取当前工作目录
work_dir=$(git rev-parse --show-toplevel)

# 获取远程仓库地址
remote_repo=$(git config --get remote.origin.url)

# 获取当前分支
current_branch=$(git symbolic-ref --short HEAD)

# 获取操作人
operator=$(git config user.name)

# 打印获取到的信息
echo "Pre-push 钩子开始执行 (执行 ID: $EXECUTION_ID)"
echo "工作目录 : $work_dir"
echo "远程仓库: $remote_repo"
echo "当前分支: $current_branch"
echo "操作人: $operator"

cd "$work_dir"

# 激活虚拟环境
source .venv/Scripts/activate

if [ "$current_branch" = "main" ]; then
    echo "当前分支是 main。运行... (执行 ID: $EXECUTION_ID)"
    echo "运行测试... (执行 ID: $EXECUTION_ID)"
    pytest
    if [ $? -ne 0 ]; then
        echo "测试失败，推送已中止 (执行 ID: $EXECUTION_ID)"
        exit 1
    fi
    echo "测试通过成功 (执行 ID: $EXECUTION_ID)"  
 

 

else
    echo "当前分支是 $current_branch。跳过 pytest 和 mypy 检查。 (执行 ID: $EXECUTION_ID)"
fi

echo "Pre-push 钩子执行成功 (执行 ID: $EXECUTION_ID)"
exit 0