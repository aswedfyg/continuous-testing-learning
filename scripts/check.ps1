$ErrorActionPreference = "Stop" # 设置错误处理为停止脚本执行

$Python = ".\.venv\Scripts\python.exe" # 定义 Python 可执行文件的路径，假设使用虚拟环境

Write-Host "==> Ruff check" 
& $Python -m ruff check . # 运行 Ruff 检查当前目录下的所有 Python 文件

Write-Host "==> Smoke tests"
& $Python -m pytest -m smoke -v --html=reports/smoke.html --self-contained-html # 运行标记为 smoke 的测试，并生成 HTML 报告

Write-Host "==> API regression tests"
& $Python -m pytest -m "api and regression" -v --html=reports/api-regression.html --self-contained-html # 运行标记为 api 和 regression 的测试，并生成 HTML 报告

Write-Host "==> UI regression tests"
& $Python -m pytest -m "ui and regression" -v --html=reports/ui-regression.html --self-contained-html # 运行标记为 ui 和 regression 的测试，并生成 HTML 报告

Write-Host "==> All local checks passed"
