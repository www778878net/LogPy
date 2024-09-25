import re
import subprocess
from pathlib import Path

def increment_patch_version():
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    version_pattern = r'version = "([\d.]+)"'
    match = re.search(version_pattern, content)
    if match:
        current_version = match.group(1)
        version_parts = current_version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        new_version = '.'.join(version_parts)
        
        new_content = re.sub(version_pattern, f'version = "{new_version}"', content)
        pyproject_path.write_text(new_content)
        print(f"Version updated from {current_version} to {new_version}")
    else:
        print("Version not found in pyproject.toml")
        return

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(stderr.decode())
        exit(1)
    return stdout.decode()

def main():
    # 增加补丁版本号
    increment_patch_version()

    # 构建项目
    print("Building project...")
    run_command("poetry build")

    # 发布项目
    print("Publishing project...")
    run_command("poetry publish")

    print("Release process completed successfully.")

if __name__ == "__main__":
    main()