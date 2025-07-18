from django.test import TestCase
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient
from rest_framework import status
from productApp.models import User, Product, ProductType, RepairRecord, Attachment
import json
from datetime import datetime, timedelta


class AttachmentTests(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            role=1  # 管理员角色
        )

        # 创建产品类型
        self.product_type = ProductType.objects.create(
            name='测试产品类型',
            warranty_period=12,
            description='测试产品类型描述'
        )

        # 创建产品
        self.product = Product.objects.create(
            qrcode_id='TEST123456',
            name='测试产品',
            product_type=self.product_type,
            status=1,  # 已生产
            production_date=datetime.now().date()
        )

        # 创建维修记录
        self.repair_record = RepairRecord.objects.create(
            product=self.product,
            customer=self.user,
            repair_reason='测试维修原因',
            status=2  # 维修中
        )

        # 设置API客户端
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # 获取RepairRecord的ContentType
        self.repair_record_content_type = ContentType.objects.get_for_model(RepairRecord)

    def test_create_attachment(self):
        """测试创建附件"""
        url = reverse('productApp:attachment-list')
        data = {
            'name': '测试附件',
            'file_url': 'https://example.com/test.pdf',
            'file_type': 1,  # PDF
            'description': '测试附件描述',
            'content_type_id': self.repair_record_content_type.id,
            'object_id': self.repair_record.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attachment.objects.count(), 1)

        attachment = Attachment.objects.first()
        self.assertEqual(attachment.name, '测试附件')
        self.assertEqual(attachment.file_url, 'https://example.com/test.pdf')
        self.assertEqual(attachment.file_type, 1)
        self.assertEqual(attachment.description, '测试附件描述')
        self.assertEqual(attachment.content_type, self.repair_record_content_type)
        self.assertEqual(attachment.object_id, self.repair_record.id)

    def test_get_repair_record_attachments(self):
        """测试获取维修记录的附件"""
        # 创建附件
        attachment = Attachment.objects.create(
            name='测试附件',
            file_url='https://example.com/test.pdf',
            file_type=1,  # PDF
            description='测试附件描述',
            content_type=self.repair_record_content_type,
            object_id=self.repair_record.id
        )

        url = reverse('productApp:repairrecord-attachments', args=[self.repair_record.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(len(response_data['data']), 1)
        self.assertEqual(response_data['data'][0]['name'], '测试附件')
        self.assertEqual(response_data['data'][0]['file_url'], 'https://example.com/test.pdf')

    def test_add_attachment_to_repair_record(self):
        """测试为维修记录添加附件"""
        url = reverse('productApp:repairrecord-add-attachment', args=[self.repair_record.id])
        data = {
            'name': '新测试附件',
            'file_url': 'https://example.com/new_test.pdf',
            'file_type': 1,  # PDF
            'description': '新测试附件描述'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], '附件添加成功')

        # 验证附件是否正确关联到维修记录
        attachments = self.repair_record.attachments
        self.assertEqual(attachments.count(), 1)
        self.assertEqual(attachments.first().name, '新测试附件')
        self.assertEqual(attachments.first().file_url, 'https://example.com/new_test.pdf')
