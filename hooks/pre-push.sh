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

if [ "$current_branch" = "develop" ]; then
    echo "当前分支是 develop。运行 pre-commit 检查... (执行 ID: $EXECUTION_ID)"

    echo "运行 TypeScript 编译... (执行 ID: $EXECUTION_ID)"
    # 获取改变的 TypeScript 文件
    changed_files=$(git diff --name-only --cached | grep '\.ts$')
    
    if [ -n "$changed_files" ]; then
        # 只编译改变的文件
        npx tsc $changed_files
        if [ $? -ne 0 ]; then
            echo "TypeScript 编译失败，提交已中止 (执行 ID: $EXECUTION_ID)"
            exit 1
        fi
    else
        echo "没有 TypeScript 文件改变，跳过编译 (执行 ID: $EXECUTION_ID)"
    fi

    echo "TypeScript 编译成功 (执行 ID: $EXECUTION_ID)"

    echo "将生成的文件添加到 Git 暂存区... (执行 ID: $EXECUTION_ID)"
    git add .
    echo "文件已添加到暂存区 (执行 ID: $EXECUTION_ID)"

    echo "切换到 main 分支并更新... (执行 ID: $EXECUTION_ID)"
    git checkout main
    #git pull origin main

    echo "获取 develop 分支最后一次提交信息... (执行 ID: $EXECUTION_ID)"
    last_commit_msg=$(git log develop -1 --pretty=%B)

    echo "合并 develop 分支，使用 --squash 选项... (执行 ID: $EXECUTION_ID)"
    git merge --squash develop

    echo "提交更改... (执行 ID: $EXECUTION_ID)"
    git commit -m "$last_commit_msg"

    echo "合并到 main 成功完成 (执行 ID: $EXECUTION_ID)"

elif [ "$current_branch" = "main" ]; then
    echo "当前分支是 main。运行... (执行 ID: $EXECUTION_ID)"
    echo "运行测试... (执行 ID: $EXECUTION_ID)"
    npm test
    if [ $? -ne 0 ]; then
        echo "测试失败，推送已中止 (执行 ID: $EXECUTION_ID)"
        exit 1
    fi
    echo "测试通过成功 (执行 ID: $EXECUTION_ID)"

    echo "切换到 develop 分支并合并 main... (执行 ID: $EXECUTION_ID)"
    git checkout develop 
    git merge main
    if [ $? -ne 0 ]; then
        echo "切换到 develop 分支并合并 main 失败，推送已中止 (执行 ID: $EXECUTION_ID)"
        exit 1
    fi
    echo "切换到 develop 分支并合并 main 成功完成 (执行 ID: $EXECUTION_ID)"

else
    echo "当前分支是 $current_branch。跳过 npm run main 和 npm run dev。 (执行 ID: $EXECUTION_ID)"
fi

echo "Pre-push 钩子执行完成 (执行 ID: $EXECUTION_ID)"