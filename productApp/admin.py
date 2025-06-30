from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, WechatProfile, ProductType, Product, OperationRecord, RepairRecord


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('qrcode_id', 'product_type', 'agent', 'name', 'phone', 'email', 'status', 
                   'shipping_date', 'activation_date', 'is_under_warranty')
    list_filter = ('status', 'product_type', 'shipping_date', 'activation_date')
    search_fields = ('qrcode_id', 'product_type__name', 'agent__username', 'name', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at', 'warranty_start_date', 'warranty_end_date')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {
            'fields': ('qrcode_id', 'product_type', 'factory_remark', 'status')
        }),
        ('代理商信息', {
            'fields': ('agent', 'shipping_date')
        }),
        ('客户信息', {
            'fields': ('name', 'phone', 'email', 'city', 'country')
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
