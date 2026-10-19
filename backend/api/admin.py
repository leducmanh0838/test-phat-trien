from django.contrib import admin
from django.utils.html import format_html

from .models import ChatMessage, ChatSession, Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Cấu hình hiển thị trang Admin cho Model Document"""

    list_display = ('title', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'error_message')

    # Chỉ hiển thị title và file khi chỉnh sửa/tạo mới trong form Admin
    fields = ('title', 'file', 'status', 'error_message', 'file_preview', 'id', 'created_at', 'updated_at')

    # Đưa status, error_message, file_preview và các trường hệ thống vào readonly_fields
    # để người dùng không chỉnh sửa thủ công khi tạo/sửa
    readonly_fields = (
        'id',
        'status',
        'error_message',
        'file_preview',
        'created_at',
        'updated_at',
    )

    ordering = ('-created_at',)

    def file_preview(self, obj):
        """Hiển thị khung xem trước (preview) nếu là ảnh hoặc link tải file"""
        if obj.file:
            url = obj.file.url
            if url.lower().endswith(
                ('png', 'jpg', 'jpeg', 'gif', 'webp', 'svg')
            ):
                return format_html(
                    '<img src="{}" style="max-height: 250px; max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);" />',
                    url,
                )
            return format_html(
                '<a href="{}" target="_blank" style="padding: 6px 12px; background: #007bff; color: white; border-radius: 4px; text-decoration: none;">📄 Xem / Tải file</a>',
                url,
            )
        return "Chưa có file"

    file_preview.short_description = "Xem trước tài liệu"

    def get_fields(self, request, obj=None):
        """
        Tùy chỉnh linh hoạt:
        - Khi Tạo mới (obj is None): Chỉ hiện 2 trường 'title' và 'file'.
        - Khi Xem/Sửa (obj đã tồn tại): Hiện thêm status, error_message và preview.
        """
        if obj is None:
            return ('title', 'file')
        return (
            'title',
            'file',
            'file_preview',
            'status',
            'error_message',
            'id',
            'created_at',
            'updated_at',
        )