# 接口 + UI 持续测试学习项目

这是一个给测试工程师入门持续测试流水线的练习项目。它包含一个本地小应用、接口自动化测试、UI 自动化测试、静态代码检查、HTML 测试报告和 GitHub Actions 流水线。

## 你会学到什么

1. 用 Python 创建虚拟环境并安装依赖。
2. 用 pytest 写接口测试。
3. 用 Playwright 写浏览器 UI 测试。
4. 用 Ruff 做静态代码检查。
5. 用 pytest-html 生成测试报告。
6. 用 GitHub Actions 在每次提交后自动跑测试。

## 项目结构

```text
app/                  本地被测应用
tests/api/            接口测试
tests/ui/             UI 自动化测试
reports/              本地测试报告输出目录
.github/workflows/    GitHub Actions 流水线
```

## 第 1 步：准备环境

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

## 第 2 步：启动本地应用

```bash
uvicorn app.main:app --reload
```

浏览器打开：

```text
http://127.0.0.1:8000
```

测试账号：

```text
用户名：admin
密码：password123
```

## 第 3 步：跑静态检查

```bash
ruff check .
```

## 第 4 步：跑接口测试并生成报告

```bash
pytest tests/api --html=reports/api.html --self-contained-html
```

## 第 5 步：跑 UI 测试并生成报告

```bash
pytest tests/ui --html=reports/ui.html --self-contained-html
```

UI 测试会自动启动本地应用，不需要你提前运行 `uvicorn`。

## 第 6 步：提交到 GitHub 后自动跑流水线

把项目推到 GitHub 后，每次 `push` 或 Pull Request 都会触发 `.github/workflows/ci.yml`。

流水线会执行：

1. 安装 Python 依赖。
2. 安装 Playwright Chromium 浏览器。
3. 执行 Ruff 静态检查。
4. 执行接口测试并上传 HTML 报告。
5. 执行 UI 测试并上传 HTML 报告。

## 练习任务

1. 改错密码，观察 UI 测试失败日志。
2. 给 `/products` 增加一个商品，再修改接口测试断言。
3. 新增一个接口，比如 `GET /cart`，并补充接口测试。
4. 故意写一个格式不好的 Python 文件，观察 Ruff 如何提示。

## 分支同步练习

- 从 main 创建练习分支。
- 在分支上提交改动。
- 通过 PR 合并回 main。
- 本地 main 再 pull 同步。

## 本地冲突练习

B 分支内容。
