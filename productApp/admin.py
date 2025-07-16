from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, WechatProfile, ProductType, Product, OperationRecord, RepairRecord

# 修改django管理的名字
admin.site.site_header = '产品管理系统'
admin.site.site_title = '产品管理系统'
admin.site.index_title = '产品管理系统'
admin.site.empty_value_display = '未设置'


class WechatProfileInline(admin.StackedInline):
    model = WechatProfile
    can_delete = False
    verbose_name = '微信资料'
    verbose_name_plural = '微信资料'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('额外信息', {'fields': ('phone', 'user_type', 'country', 'city')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('额外信息', {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'user_type', 'country', 'city'),
        }),
    )
    
    inlines = [WechatProfileInline]


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_number', 'warranty_period', 'created_at')
    list_filter = ('warranty_period', 'created_at')
    search_fields = ('name', 'model_number', 'specifications')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('qrcode_id', 'product_type', 'agent', 'name', 'status', 'shipping_date', 'activation_date',
                    'is_under_warranty')
    list_filter = ('status', 'product_type', 'shipping_date', 'activation_date')
    search_fields = ('qrcode_id', 'product_type__name', 'agent__username', 'name', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at', 'warranty_start_date', 'warranty_end_date')
    ordering = ('-created_at',)
    change_list_template = 'admin/productApp/product/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-create/', self.admin_site.admin_view(self.bulk_create_view), name='product_bulk_create'),
        ]
        return custom_urls + urls

    def bulk_create_view(self, request):
        if request.method == 'POST':
            qrcode_ids = request.POST.get('qrcode_ids', '').strip().split('\n')
            product_type_id = request.POST.get('product_type')
            factory_remark = request.POST.get('factory_remark', '').strip()

            if not qrcode_ids or not product_type_id:
                messages.error(request, '请提供二维码ID列表和产品类型')
                return redirect('.')

            try:
                product_type = ProductType.objects.get(id=product_type_id)
                created_count = 0
                skipped_count = 0
                error_qrcodes = []

                for qrcode_id in qrcode_ids:
                    qrcode_id = qrcode_id.strip()
                    if not qrcode_id:
                        continue

                    # 检查是否已存在相同的qrcode_id
                    if Product.objects.filter(qrcode_id=qrcode_id).exists():
                        skipped_count += 1
                        error_qrcodes.append(f"{qrcode_id} (已存在)")
                        continue

                    try:
                        Product.objects.create(
                            qrcode_id=qrcode_id,
                            product_type=product_type,
                            factory_remark=factory_remark
                        )
                        created_count += 1
                    except Exception as e:
                        error_qrcodes.append(f"{qrcode_id} ({str(e)})")

                if created_count > 0:
                    messages.success(request, f'成功创建 {created_count} 个产品')
                if skipped_count > 0:
                    messages.warning(request, f'跳过 {skipped_count} 个已存在的产品')
                if error_qrcodes:
                    messages.error(request, f'以下ID创建失败：{", ".join(error_qrcodes)}')

            except ProductType.DoesNotExist:
                messages.error(request, '无效的产品类型')
            except Exception as e:
                messages.error(request, f'创建产品时发生错误：{str(e)}')

            return redirect('admin:productApp_product_changelist')

        # GET请求显示表单
        context = {
            'title': '批量创建产品',
            'product_types': ProductType.objects.all(),
            **self.admin_site.each_context(request),
        }
        return render(request, 'admin/productApp/product/bulk_create.html', context)
    
    fieldsets = (
        ('基本信息', {
            'fields': ('qrcode_id', 'product_type', 'factory_remark', 'status')
        }),
        ('代理商信息', {
            'fields': ('agent', 'shipping_date')
        }),
        ('客户信息', {
            'fields': ('name', 'phone', 'email', 'city', 'country', 'installer')
        }),
        ('激活和保修信息', {
            'fields': ('activation_date', 'warranty_start_date', 'warranty_end_date')
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def is_under_warranty(self, obj):
        return obj.is_under_warranty()
    is_under_warranty.short_description = '在保修期内'
    is_under_warranty.boolean = True


@admin.register(OperationRecord)
class OperationRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'operator', 'operation_type', 'created_at')
    list_filter = ('operation_type', 'created_at')
    search_fields = ('product__qrcode_id', 'operator__username', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def has_change_permission(self, request, obj=None):
        return False  # 操作记录不允许修改
    
    def has_delete_permission(self, request, obj=None):
        return False  # 操作记录不允许删除


@admin.register(RepairRecord)
class RepairRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'technician', 'status', 'repair_date', 'created_at')
    list_filter = ('status', 'repair_date', 'created_at')
    search_fields = ('product__qrcode_id', 'customer__username', 'technician__username', 
                    'repair_reason', 'repair_solution')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # 编辑现有记录
            return self.readonly_fields + ('product', 'customer')  # 产品和客户信息不允许修改
        return self.readonly_fields
