# Windows 部署与排错（PowerShell / CMD）

本项目后端基于 Python，首次部署只需要跑起 `backend/app.py`，前端资源已内置在 `frontend/`，无需额外构建。

## 0) 环境要求

- Windows 10/11
- Python 3.10+（3.9 及以下不支持）
- Git

建议使用虚拟环境（`.venv`），避免污染全局 Python。

## 1) 下载仓库

PowerShell：

```powershell
git clone https://github.com/ringhyacinth/Star-Office-UI.git
cd Star-Office-UI
```

## 2) 创建虚拟环境并安装依赖（推荐）

PowerShell：

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python -m pip install -r backend\requirements.txt
```

如果你机器上装的是 3.11/3.12/3.13，把上面的 `-3.10` 改成对应版本即可。也可以先用 `py -0p` 查看已安装的 Python 列表。

如果你没有安装 Python Launcher（`py`），也可以用：

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r backend\requirements.txt
```

## 3) 初始化状态文件（首次）

PowerShell：

```powershell
Copy-Item state.sample.json state.json
```

CMD：

```bat
copy state.sample.json state.json
```

## 4) 启动后端

PowerShell（推荐）：

```powershell
cd backend
..\.\.venv\Scripts\python app.py
```

看到类似 “Running on http://127.0.0.1:19000” 后，打开：

- http://127.0.0.1:19000

## 5) 切换状态（验证工作流）

回到项目根目录执行：

PowerShell：

```powershell
cd ..
.\.venv\Scripts\python set_state.py writing "正在整理文档"
.\.venv\Scripts\python set_state.py error "发现问题，排查中"
.\.venv\Scripts\python set_state.py idle "待命中"
```

## 6) 可选：生产环境配置（强烈建议）

复制 `.env.example` 为 `.env`，并设置强随机的 `FLASK_SECRET_KEY` 与 `ASSET_DRAWER_PASS`。

PowerShell：

```powershell
Copy-Item .env.example .env
```

CMD：

```bat
copy .env.example .env
```

## 7) 可选：运行 Smoke Test

确保后端已在另一个终端运行，然后执行：

```powershell
.\.venv\Scripts\python scripts\smoke_test.py --base-url http://127.0.0.1:19000
```

## 常见问题

### 1) 浏览器打不开 19000

- 确认终端里后端没有报错，并且地址是 `http://127.0.0.1:19000`
- Windows Defender 防火墙可能会弹窗拦截 Python，请选择允许访问
- 若你修改为局域网访问（`0.0.0.0`），请确认端口放行与路由规则

### 2) 报错提示缺少依赖

优先确认你运行的是虚拟环境里的 Python：

- `.\.venv\Scripts\python -V`

然后重新安装依赖：

- `.\.venv\Scripts\python -m pip install -r backend\requirements.txt`

