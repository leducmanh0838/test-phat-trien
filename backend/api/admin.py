from django.contrib import admin
from .models import ChatMessage, ChatSession, Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Cấu hình hiển thị trang Admin cho Model Document"""

    list_display = ('title', 'language', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'language', 'created_at')
    search_fields = ('title', 'error_message')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


class ChatMessageInline(admin.TabularInline):
    """Hiển thị danh sách tin nhắn ngay bên trong trang chi tiết của Phiên chat"""

    model = ChatMessage
    extra = 0
    readonly_fields = ('id', 'role', 'content', 'sources', 'created_at')
    can_delete = True


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    """Cấu hình hiển thị trang Admin cho Model ChatSession"""

    list_display = ('title', 'id', 'created_at')
    search_fields = ('title', 'id')
    readonly_fields = ('id', 'created_at')
    inlines = [ChatMessageInline]
    ordering = ('-created_at',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """Cấu hình hiển thị trang Admin riêng cho từng ChatMessage"""

    list_display = ('session', 'role', 'short_content', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('id', 'created_at')

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    short_content.short_description = "Nội dung tin nhắn"