# Generated by Django 5.2.3 on 2025-06-28 02:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='产品名称')),
                ('model_number', models.CharField(max_length=50, verbose_name='型号')),
                ('specifications', models.TextField(blank=True, null=True, verbose_name='规格')),
                ('description', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('warranty_period', models.IntegerField(default=365, verbose_name='保修期(天)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '产品类型',
                'verbose_name_plural': '产品类型',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='城市'),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='国家'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qrcode_id', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='二维码ID')),
                ('shipping_date', models.DateTimeField(blank=True, null=True, verbose_name='出货日期')),
                ('activation_date', models.DateTimeField(blank=True, null=True, verbose_name='激活日期')),
                ('warranty_start_date', models.DateTimeField(blank=True, null=True, verbose_name='保修开始日期')),
                ('warranty_end_date', models.DateTimeField(blank=True, null=True, verbose_name='保修结束日期')),
                ('status', models.IntegerField(choices=[(1, '已生成'), (2, '已出货'), (3, '已激活'), (4, '维修中'), (5, '已报废')], default=1, verbose_name='状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('agent', models.ForeignKey(blank=True, limit_choices_to={'user_type': 1}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_products', to=settings.AUTH_USER_MODEL, verbose_name='代理商')),
                ('customer', models.ForeignKey(blank=True, limit_choices_to={'user_type': 2}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_products', to=settings.AUTH_USER_MODEL, verbose_name='客户')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='productApp.producttype', verbose_name='产品类型')),
            ],
            options={
                'verbose_name': '产品',
                'verbose_name_plural': '产品',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OperationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_type', models.IntegerField(choices=[(1, '创建产品'), (2, '产品出货'), (3, '产品激活'), (4, '维修登记'), (5, '维修完成'), (6, '报废处理')], verbose_name='操作类型')),
                ('description', models.TextField(blank=True, null=True, verbose_name='操作描述')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='操作时间')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operations', to=settings.AUTH_USER_MODEL, verbose_name='操作人')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operation_records', to='productApp.product', verbose_name='产品')),
            ],
            options={
                'verbose_name': '操作记录',
                'verbose_name_plural': '操作记录',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RepairRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repair_reason', models.TextField(verbose_name='维修原因')),
                ('repair_solution', models.TextField(blank=True, null=True, verbose_name='维修解决方案')),
                ('repair_date', models.DateTimeField(blank=True, null=True, verbose_name='维修日期')),
                ('status', models.IntegerField(choices=[(1, '待维修'), (2, '维修中'), (3, '已完成'), (4, '无法修复')], default=1, verbose_name='状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('customer', models.ForeignKey(limit_choices_to={'user_type': 2}, on_delete=django.db.models.deletion.CASCADE, related_name='repair_requests', to=settings.AUTH_USER_MODEL, verbose_name='客户')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repair_records', to='productApp.product', verbose_name='产品')),
                ('technician', models.ForeignKey(blank=True, limit_choices_to={'user_type': 3}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repairs_handled', to=settings.AUTH_USER_MODEL, verbose_name='技术人员')),
            ],
            options={
                'verbose_name': '维修记录',
                'verbose_name_plural': '维修记录',
                'ordering': ['-created_at'],
            },
        ),
    ]
