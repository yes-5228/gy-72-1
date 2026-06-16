# 学校食堂订餐系统

Django + Vue 实现的校园食堂订餐系统，包含菜品展示、提前订餐、营养成分分析、配送管理、评价反馈等模块。项目已按前后端模块化拆分，适合继续扩展登录、支付、库存审批等功能。

## 功能模块

- 菜品展示：按供餐时段、分类筛选，展示价格、库存、热量、蛋白质、钠含量等信息。
- 提前订餐：学生填写姓名、学号、电话、配送地址、预约送达时间并提交餐盘。
- 营养分析：根据餐盘菜品汇总热量、蛋白质、脂肪、碳水、钠，并给出搭配建议。
- 配送管理：查看配送任务，更新待分配、已分配、已取餐、已送达、异常状态。
- 评价反馈：对菜品提交评分和文字评价，展示近期反馈。

## 目录结构

```text
backend/
  apps/
    menu/        # 菜品分类、菜品 API
    orders/      # 订单与订单明细 API
    nutrition/   # 营养分析 API
    delivery/    # 配送任务 API
    reviews/     # 评价 API
    common/      # 示例数据管理命令
  config/        # Django 配置与路由
frontend/
  src/
    api/         # 前端 API 封装
    components/  # 可复用组件
    pages/       # 页面模块
docker-compose.yml
```

## Docker 启动

前端 Docker 镜像默认使用已经构建好的 `frontend/dist` 目录，避免在 Docker 构建阶段拉取 `node` 镜像。首次启动前如果没有 `frontend/dist`，先执行：

```bash
cd frontend
npm install
npm run build
cd ..
```

然后启动：

```bash
docker compose up --build
```

访问地址：

- 前端：http://127.0.0.1:8080
- 后端 API：http://127.0.0.1:8000/api/
- Django Admin：http://127.0.0.1:8000/admin/

Docker 启动时会自动执行数据库迁移和 `seed_demo` 示例数据初始化。

如果构建时报 `nginx:1.27-alpine`、`python:3.12-slim`、`postgres:16-alpine` 等基础镜像拉取失败，通常是 Docker Desktop 配置的 registry mirror 不可用或被限流。报错中如果出现类似 `EOF`、`429 Too Many Requests`，请在 Docker Desktop 的 registry mirrors 中移除失效镜像源，或临时指定可用的 Nginx 基础镜像地址：

```bash
NGINX_IMAGE=可用镜像源/library/nginx:1.27-alpine docker compose build frontend
docker compose up
```

Windows PowerShell 示例：

```powershell
$env:NGINX_IMAGE="可用镜像源/library/nginx:1.27-alpine"
docker compose build frontend
docker compose up
```

## 本地开发

后端：

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 127.0.0.1:8000
```

前端：

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

访问 http://127.0.0.1:5173 进行开发调试。

## 常用 API

- `GET /api/categories/`：菜品分类
- `GET /api/dishes/`：菜品列表，支持 `meal_period`、`category`、`search`
- `POST /api/orders/`：创建提前订餐订单
- `POST /api/nutrition/analyze/`：提交 `dish_ids` 获取营养分析
- `GET/PATCH /api/deliveries/`：配送任务查询和状态更新
- `GET/POST /api/reviews/`：评价查询和提交
