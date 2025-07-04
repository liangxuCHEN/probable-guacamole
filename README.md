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
- pip (Python包管理器)

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

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 配置数据库
   ```bash
   # 在settings.py中配置数据库连接
   ```

5. 执行数据库迁移
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. 创建超级用户
   ```bash
   python manage.py createsuperuser
   ```

7. 运行开发服务器
   ```bash
   python manage.py runserver
   ```

## 使用示例

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
