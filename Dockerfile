# 构建阶段
FROM hub.bds100.com/python:3.10-slim as builder

# 设置工作目录
WORKDIR /app

# 使用阿里云镜像源
RUN rm -rf /etc/apt/sources.list.d/* && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm main non-free contrib" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bookworm-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm-updates main non-free contrib" >> /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 配置pip使用阿里云镜像源
COPY pip.conf /etc/pip.conf

# 分层安装依赖
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 运行阶段
FROM hub.bds100.com/python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=musicWeb.settings \
    TZ=Asia/Shanghai

# 使用阿里云镜像源
RUN rm -rf /etc/apt/sources.list.d/* && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm main non-free contrib" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bookworm-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm-updates main non-free contrib" >> /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制Python包
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# 复制项目文件
COPY . .

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 创建日志目录
RUN mkdir -p /var/log/gunicorn && \
    mkdir -p /var/log/celery && \
    mkdir -p /var/log/celery-beat && \
    chmod -R 777 /var/log

EXPOSE 8000

CMD ["gunicorn", "innrg.wsgi:application", "--bind", "0.0.0.0:8000"]
