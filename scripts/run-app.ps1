$ErrorActionPreference = "Stop" # 设置错误处理为停止脚本执行
 
$Python = ".\.venv\Scripts\python.exe" # 定义 Python 可执行文件的路径，假设使用虚拟环境

Write-Host "==> Starting local app at http://127.0.0.1:8000"
& $Python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload     
