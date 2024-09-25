#!/bin/bash

# 获取当前工作目录
work_dir=$(git rev-parse --show-toplevel)

# 获取远程仓库地址
remote_repo=$(git config --get remote.origin.url)

# 获取当前分支
current_branch=$(git symbolic-ref --short HEAD)

# 获取操作人
operator=$(git config user.name)

# 打印获取到的信息
echo "Post-push 钩子开始执行"
echo "工作目录: $work_dir"
echo "远程仓库: $remote_repo"
echo "当前分支: $current_branch"
echo "操作人: $operator"

cd "$work_dir"

# 如果当前分支是 main，则切换回 develop 分支
if [ "$current_branch" = "main" ]; then
    echo "当前分支是 main。切换回 develop 分支..."
    git checkout develop
    if [ $? -ne 0 ]; then
        echo "切换回 develop 分支失败"
        exit 1
    fi
    echo "成功切换回 develop 分支"
# 如果当前分支是 develop，则切换到 main 分支
elif [ "$current_branch" = "develop" ]; then
    echo "当前分支是 develop。切换到 main 分支..."
    git checkout main
    if [ $? -ne 0 ]; then
        echo "切换到 main 分支失败"
        exit 1
    fi
    echo "成功切换到 main 分支"
fi

# 在这里可以添加其他需要在 push 后执行的操作
# 例如：发送通知、更新文档、触发构建等

echo "Post-push 钩子执行完成"