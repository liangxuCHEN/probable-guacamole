# 产品生命周期管理系统

## 项目概述

本系统旨在追踪产品的完整生命周期，从生产到销售再到用户激活。通过二维码技术实现唯一标识管理，并提供出货记录、激活记录及保修状态查询等功能。系统支持产品维修管理，确保售后服务的高效运作。

## 核心功能

1. **产品信息管理**
   - 录入产品基础信息（名称、型号、规格等）
   - 管理产品类型和详细规格

2. **二维码生成**
   - 为每个产品生成唯一的二维码
   - 支持批量生成产品二维码

3. **出货管理**
   - 记录产品出货时间及代理商信息
   - 支持批量出货操作

4. **产品激活**
   - 用户扫码后输入个人信息完成激活
   - 自动计算并生成保修期

5. **保修状态查询**
   - 通过二维码ID查询产品是否在保修期内
   - 支持通过客户邮箱或手机号查询

6. **维修管理**
   - 维修记录：绑定产品ID，记录维修原因、时间、处理结果
   - 维修状态跟踪和更新

7. **操作记录**
   - 自动记录所有关键操作
   - 提供完整的操作历史查询

## 技术栈

- **后端框架**: Django + Django REST Framework
- **认证方式**: JWT (JSON Web Token)
- **数据库**: PostgreSQL
- **API风格**: RESTful API

## 系统架构

系统采用前后端分离架构：

- 后端提供RESTful API接口
- 前端负责用户界面展示和交互
- 使用JWT进行用户认证和授权
- 数据库存储所有业务数据

## 数据模型

系统包含以下主要数据模型：

1. **User**: 用户模型，区分代理商、客户和员工
2. **ProductType**: 产品类型表
3. **Product**: 产品二维码表
4. **OperationRecord**: 操作记录表
5. **RepairRecord**: 维修记录表

## API接口

### 用户管理

- `POST /api/login/`: 用户登录
- `GET /api/users/me/`: 获取当前用户信息

### 产品类型管理

- `GET /api/product-types/`: 获取所有产品类型
- `POST /api/product-types/`: 创建新产品类型
- `GET /api/product-types/{id}/`: 获取特定产品类型详情
- `PUT /api/product-types/{id}/`: 更新产品类型
- `DELETE /api/product-types/{id}/`: 删除产品类型

### 产品管理

- `GET /api/products/`: 获取所有产品
- `POST /api/products/`: 创建单个产品
- `GET /api/products/{id}/`: 获取特定产品详情
- `PUT /api/products/{id}/`: 更新产品
- `DELETE /api/products/{id}/`: 删除产品
- `POST /api/products/bulk_create/`: 批量创建产品
- `POST /api/products/bulk_shipping/`: 批量发货
- `POST /api/products/activate/`: 激活产品
- `POST /api/products/check_warranty/`: 查询保修状态

### 操作记录管理

- `GET /api/operation-records/`: 获取所有操作记录
- `GET /api/operation-records/{id}/`: 获取特定操作记录详情

### 维修记录管理

- `GET /api/repair-records/`: 获取所有维修记录
- `POST /api/repair-records/`: 创建维修记录
- `GET /api/repair-records/{id}/`: 获取特定维修记录详情
- `PUT /api/repair-records/{id}/`: 更新维修记录
- `DELETE /api/repair-records/{id}/`: 删除维修记录
- `POST /api/repair-records/{id}/complete_repair/`: 完成维修

## 安装和配置

### 前提条件

- Python 3.8+
- PostgreSQL
- uv (Python包管理器)

### 安装步骤

1. 克隆仓库
   ```bash
   git clone <repository-url>
   cd innrg
   ```

2. 创建并激活虚拟环境
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. 安装uv包管理器
   ```bash
   pip install uv
   ```

4. 使用uv安装依赖
   ```bash
   uv pip install -r requirements.txt
   # 或者使用pyproject.toml
   uv pip install -e .
   ```

5. 配置数据库
   ```bash
   # 在settings.py中配置数据库连接
   ```

6. 执行数据库迁移
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. 创建超级用户
   ```bash
   python manage.py createsuperuser
   ```

8. 运行开发服务器
   ```bash
   python manage.py runserver
   ```

## 部署指南

### 使用Gunicorn部署

1. 安装Gunicorn和Gevent
   ```bash
   uv pip install gunicorn gevent
   ```

2. 收集静态文件
   ```bash
   python manage.py collectstatic
   ```

3. 确保日志目录存在
   ```bash
   sudo mkdir -p /var/log/gunicorn
   sudo chown -R <your-user>:<your-group> /var/log/gunicorn
   ```

4. 测试Gunicorn配置
   ```bash
   gunicorn --config=gunicorn.conf.py innrg.wsgi:application
   ```

4. 调整Gunicorn配置

   根据您的服务器环境，您可能需要调整gunicorn.conf.py中的配置：
   
   ```python
   # 调整工作进程数（通常设置为CPU核心数的2-4倍）
   workers = 4  # 根据您的CPU核心数调整
   
   # 调整日志路径
   accesslog = '/path/to/your/logs/access.log'
   errorlog = '/path/to/your/logs/error.log'
   
   # 在生产环境中可能需要启用守护进程模式
   daemon = True
   ```

5. 生产环境部署
   
   创建systemd服务文件（Linux系统）:
   ```bash
   sudo nano /etc/systemd/system/innrg.service
   ```
   
   添加以下内容:
   ```
   [Unit]
   Description=Innrg Gunicorn Service
   After=network.target

   [Service]
   User=<your-user>
   Group=<your-group>
   WorkingDirectory=/path/to/innrg
   ExecStart=/path/to/venv/bin/gunicorn --config=gunicorn.conf.py innrg.wsgi:application
   
   # 添加环境变量
   Environment="DJANGO_SETTINGS_MODULE=innrg.settings"
   Environment="DJANGO_SECRET_KEY=your-secret-key"
   Environment="DJANGO_DEBUG=False"
   Environment="DATABASE_URL=postgres://user:password@localhost:5432/innrg"
   
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

5. 启动服务
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start innrg
   sudo systemctl enable innrg
   ```

6. 检查服务状态
   ```bash
   sudo systemctl status innrg
   ```

### 使用Nginx作为反向代理

1. 安装Nginx
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. 创建Nginx配置文件
   ```bash
   sudo nano /etc/nginx/sites-available/innrg
   ```
   
   添加以下内容:
   ```
   server {
       listen 80;
       server_name your-domain.com;

       location /static/ {
           alias /path/to/innrg/static/;
       }

       location /media/ {
           alias /path/to/innrg/media/;
       }

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. 启用站点配置
   ```bash
   sudo ln -s /etc/nginx/sites-available/innrg /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

4. 配置SSL（可选，推荐）
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

### 生产环境安全性配置

1. 禁用DEBUG模式
   
   在生产环境中，应该禁用Django的DEBUG模式。可以通过环境变量或直接在settings.py中设置：
   
   ```python
   # settings.py
   DEBUG = False
   ```

2. 设置安全的SECRET_KEY
   
   不要在代码中硬编码SECRET_KEY，应该通过环境变量设置：
   
   ```python
   # settings.py
   import os
   SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
   ```

3. 配置允许的主机
   
   限制可以访问您应用的主机名：
   
   ```python
   # settings.py
   ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
   ```

4. 设置适当的文件权限
   
   ```bash
   # 设置代码目录权限
   sudo chown -R <your-user>:<your-group> /path/to/innrg
   sudo chmod -R 755 /path/to/innrg
   
   # 设置敏感文件权限
   sudo chmod 600 /path/to/innrg/.env
   ```

### 监控和维护

1. 查看日志
   
   ```bash
   # 查看Gunicorn访问日志
   sudo tail -f /var/log/gunicorn/access.log
   
   # 查看Gunicorn错误日志
   sudo tail -f /var/log/gunicorn/error.log
   
   # 查看Nginx访问日志
   sudo tail -f /var/log/nginx/access.log
   
   # 查看Nginx错误日志
   sudo tail -f /var/log/nginx/error.log
   ```

2. 重启服务
   
   ```bash
   # 重启Gunicorn服务
   sudo systemctl restart innrg
   
   # 重启Nginx
   sudo systemctl restart nginx
   ```

3. 数据库备份
   
   ```bash
   # 备份PostgreSQL数据库
   pg_dump -U postgres innrg > innrg_backup_$(date +%Y%m%d).sql
   
   # 恢复数据库
   psql -U postgres innrg < innrg_backup.sql
   ```

### 使用Docker部署（可选）

1. 创建Dockerfile
   ```bash
   nano Dockerfile
   ```
   
   添加以下内容:
   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   RUN pip install uv

   COPY requirements.txt .
   RUN uv pip install -r requirements.txt
   RUN uv pip install gunicorn gevent

   COPY . .

   RUN mkdir -p /var/log/gunicorn
   RUN python manage.py collectstatic --noinput

   EXPOSE 8000

   CMD ["gunicorn", "--config=gunicorn.conf.py", "innrg.wsgi:application"]
   ```

2. 创建docker-compose.yml
   ```bash
   nano docker-compose.yml
   ```
   
   添加以下内容:
   ```yaml
   version: '3'

   services:
     db:
       image: postgres:14
       volumes:
         - postgres_data:/var/lib/postgresql/data/
       env_file:
         - ./.env
       environment:
         - POSTGRES_PASSWORD=postgres
         - POSTGRES_USER=postgres
         - POSTGRES_DB=innrg

     web:
       build: .
       restart: always
       depends_on:
         - db
       env_file:
         - ./.env
       volumes:
         - ./:/app
         - static_volume:/app/static
         - media_volume:/app/media
       ports:
         - "8000:8000"

     nginx:
       image: nginx:1.21
       ports:
         - "80:80"
       volumes:
         - ./nginx/conf.d:/etc/nginx/conf.d
         - static_volume:/home/app/static
         - media_volume:/home/app/media
       depends_on:
         - web

   volumes:
     postgres_data:
     static_volume:
     media_volume:
   ```

3. 启动Docker容器
   ```bash
   docker-compose up -d
   ```

### 性能优化建议

1. 配置缓存
   
   在settings.py中配置缓存系统：
   
   ```python
   # 使用Redis作为缓存后端
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
           'OPTIONS': {
               'CLIENT_CLASS': 'django_redis.client.DefaultClient',
           }
       }
   }
   ```
   
   安装必要的包：
   ```bash
   uv pip install django-redis redis
   ```

2. 数据库优化
   
   - 为频繁查询的字段添加索引
   - 使用select_related()和prefetch_related()减少数据库查询
   - 考虑使用数据库连接池：
     ```bash
     uv pip install django-db-connection-pool
     ```

3. 静态文件优化
   
   使用CDN或配置静态文件缓存：
   ```python
   # settings.py
   STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
   ```

### 自动化部署

1. 使用GitHub Actions自动部署

   创建.github/workflows/deploy.yml文件：
   ```yaml
   name: Deploy

   on:
     push:
       branches: [ main ]

   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v2
       
       - name: Set up Python
         uses: actions/setup-python@v2
         with:
           python-version: '3.10'
       
       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install uv
           uv pip install -r requirements.txt
       
       - name: Run tests
         run: |
           python manage.py test
       
       - name: Deploy to server
         uses: appleboy/ssh-action@master
         with:
           host: ${{ secrets.HOST }}
           username: ${{ secrets.USERNAME }}
           key: ${{ secrets.SSH_PRIVATE_KEY }}
           script: |
             cd /path/to/innrg
             git pull
             source venv/bin/activate
             uv pip install -r requirements.txt
             python manage.py migrate
             python manage.py collectstatic --noinput
             sudo systemctl restart innrg
   ```

2. 使用Fabric进行部署自动化
   
   安装Fabric：
   ```bash
   uv pip install fabric
   ```
   
   创建fabfile.py：
   ```python
   from fabric import task

   @task
   def deploy(c):
       # 拉取最新代码
       c.run('cd /path/to/innrg && git pull')
       
       # 更新依赖
       c.run('cd /path/to/innrg && source venv/bin/activate && uv pip install -r requirements.txt')
       
       # 执行数据库迁移
       c.run('cd /path/to/innrg && source venv/bin/activate && python manage.py migrate')
       
       # 收集静态文件
       c.run('cd /path/to/innrg && source venv/bin/activate && python manage.py collectstatic --noinput')
       
       # 重启服务
       c.run('sudo systemctl restart innrg')
   ```
   
   使用Fabric部署：
   ```bash
   fab -H user@server deploy
   ```

### 故障排除

1. Gunicorn无法启动
   
   检查日志文件：
   ```bash
   sudo tail -f /var/log/gunicorn/error.log
   ```
   
   常见问题：
   - 路径错误：确保gunicorn.conf.py中的路径正确
   - 权限问题：确保用户有权限访问所有必要的文件和目录
   - 依赖问题：确保所有必要的包都已安装

2. 静态文件未正确加载
   
   检查Nginx配置：
   ```bash
   sudo nginx -t
   ```
   
   确保静态文件已收集：
   ```bash
   python manage.py collectstatic --noinput
   ```
   
   检查静态文件目录权限：
   ```bash
   sudo chown -R www-data:www-data /path/to/static
   ```

3. 数据库连接问题
   
   检查数据库服务是否运行：
   ```bash
   sudo systemctl status postgresql
   ```
   
   检查数据库连接设置：
   ```bash
   # 确保settings.py中的数据库配置正确
   # 或者环境变量中的DATABASE_URL正确
   ```

4. 500服务器错误
   
   检查Django错误日志：
   ```bash
   sudo tail -f /var/log/gunicorn/error.log
   ```
   
   临时启用DEBUG模式进行调试（记得之后禁用）：
   ```python
   # settings.py
   DEBUG = True
   ```

5. 502 Bad Gateway错误
   
   检查Gunicorn是否正在运行：
   ```bash
   ps aux | grep gunicorn
   ```
   
   检查Nginx和Gunicorn之间的通信：
   ```bash
   # 确保Nginx配置中的proxy_pass指向正确的Gunicorn地址和端口
   ```

## 使用示例

### 查询供应商

```json
GET /api/users/agents/

{
    "status": "success",
    "data": [
        {
            "id": 2,
            "username": "广州代理",
            "email": "chenliangxu68@gmail.com",
            "phone": "0658214120",
            "user_type": 1,
            "wechat_profile": null
        }
    ]
}
```

### 批量创建产品

```json
POST /api/products/bulk_create/
{
  "product_type_id": 1,
  "qrcode_ids": ["QR001", "QR002", "QR003"], 
  "remark": "备注信息"
}
```

### 批量发货

```json
POST /api/products/bulk_shipping/
{
  "qrcode_ids": ["QR001", "QR002", "QR003"],
  "agent_id": 5
}
```

### 激活产品

```json
POST /api/products/activate/
{
  "qrcode_id": "QR001",
  "customer_id": 10
}
```

### 查询保修状态

```json
POST /api/products/check_warranty/
{
  "qrcode_id": "QR001"
}

# 二维码查询
GET /api/products/get_by_qrcode/?qrcode_id=112sdf
```

## 权限控制

系统实现了基于角色的权限控制：

- **管理员**: 可以执行所有操作
- **员工**: 可以查看产品信息、处理维修等
- **代理商**: 可以查看自己的产品信息
- **客户**: 可以查看自己的产品和提交维修请求

## 功能扩展建议

- **批量生成产品ID和对应二维码脚本**: 支持一次性生成多个产品二维码
- **微信小程序扫码激活**: 集成微信生态
- **图片识别激活**: 支持OCR识别激活信息
- **数据分析和报表**: 添加数据分析功能，生成销售和维修报表

## 安全措施

- 使用HTTPS加密通信
- JWT认证保护API接口
- 基于角色的权限控制
- 输入验证和数据清洗

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

[MIT License](LICENSE)
