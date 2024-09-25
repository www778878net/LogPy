import re
import subprocess
from pathlib import Path

def get_current_branch():
    return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()

def increment_patch_version():
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text(encoding='utf-8')
    
    version_pattern = r'version = "([\d.]+)"'
    match = re.search(version_pattern, content)
    if match:
        current_version = match.group(1)
        version_parts = current_version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        new_version = '.'.join(version_parts)
        
        new_content = re.sub(version_pattern, f'version = "{new_version}"', content)
        pyproject_path.write_text(new_content, encoding='utf-8')
        print(f"版本从 {current_version} 更新到 {new_version}")
    else:
        print("在 pyproject.toml 中未找到版本信息")
        return

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    try:
        stdout_str = stdout.decode('utf-8')
    except UnicodeDecodeError:
        stdout_str = stdout.decode('gbk')
    try:
        stderr_str = stderr.decode('utf-8')
    except UnicodeDecodeError:
        stderr_str = stderr.decode('gbk')
    
    if process.returncode != 0:
        print(f"执行命令时出错: {command}")
        print(stderr_str)
        raise Exception(stderr_str)
    return stdout_str

def ensure_ssh_agent_running():
    print("正在检查 SSH 代理状态...")
    try:
        result = run_command("sc query ssh-agent")
        if "RUNNING" in result:
            print("SSH 代理已经在运行")
            return
        
        print("正在启动 SSH 代理...")
        run_command("sc start ssh-agent")
        print("SSH 代理启动成功")
    except Exception as e:
        print(f"处理 SSH 代理时出错: {e}")
        print("请确保已安装 OpenSSH 并手动启动 SSH 代理")
        exit(1)

def main():
    current_branch = get_current_branch()
    if current_branch != 'main':
        print(f"当前分支是 {current_branch}。发布过程只能在 main 分支上运行。")
        exit(1)

    # 检查 SSH 代理状态
    ensure_ssh_agent_running()

    # 运行测试
    print("正在运行测试...")
    run_command("pytest")

    # 增加补丁版本号
    increment_patch_version()

    # 构建项目
    print("正在构建项目...")
    run_command("poetry build")

    # 发布项目
    print("正在发布项目...")
    run_command("poetry publish")

    # 提交版本更新并推送到远程仓库
    print("正在提交版本更新并推送到远程仓库...")
    run_command("git add pyproject.toml")
    run_command('git commit -m "Bump version"')
    try:
        run_command("git push origin main")
        print("成功推送到远程仓库")
    except Exception as e:
        print(f"推送到远程仓库失败: {e}")
        print("请检查您的 Git 配置和仓库访问权限")
        exit(1)

    print("发布过程成功完成。")

if __name__ == "__main__":
    main()