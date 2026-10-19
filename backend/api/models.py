import uuid
from django.db import models


class Document(models.Model):
    """Model lưu trữ thông tin các tài liệu kỹ thuật được tải lên"""

    STATUS_CHOICES = [
        ('PENDING', 'Chờ xử lý'),
        ('PROCESSING', 'Đang xử lý/Indexing'),
        ('COMPLETED', 'Hoàn tất'),
        ('FAILED', 'Lỗi xử lý'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Tên tài liệu")
    file = models.FileField(upload_to='documents/', verbose_name="File đính kèm")
    language = models.CharField(
        max_length=10, default='en', verbose_name="Ngôn ngữ chính"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name="Trạng thái",
    )
    error_message = models.TextField(
        blank=True, null=True, verbose_name="Chi tiết lỗi nếu có"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Ngày tải lên"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Cập nhật lần cuối"
    )

    class Meta:
        verbose_name = "Tài liệu"
        verbose_name_plural = "Danh sách tài liệu"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"


class ChatSession(models.Model):
    """Model quản lý các phiên hội thoại (Cần thiết để nhóm các tin nhắn)"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=255, default="Cuộc trò chuyện mới", verbose_name="Tiêu đề"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Ngày tạo"
    )

    class Meta:
        verbose_name = "Phiên trò chuyện"
        verbose_name_plural = "Danh sách phiên trò chuyện"

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    """Model lưu trữ từng tin nhắn trong cuộc trò chuyện"""

    ROLE_CHOICES = [
        ('user', 'Người dùng'),
        ('assistant', 'Trợ lý AI'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="Phiên chat",
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, verbose_name="Vai trò"
    )
    content = models.TextField(verbose_name="Nội dung tin nhắn")

    # Lưu danh sách nguồn tài liệu trích dẫn (Citations/Sources) dạng JSON
    sources = models.JSONField(
        blank=True, null=True, verbose_name="Nguồn trích dẫn"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Thời gian tạo"
    )

    class Meta:
        verbose_name = "Tin nhắn"
        verbose_name_plural = "Danh sách tin nhắn"
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.get_role_display()}] {self.content[:30]}..."