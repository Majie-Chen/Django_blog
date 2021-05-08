from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.fields import exceptions

# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=15, verbose_name='文章类型')

    class Meta:
        verbose_name = '文章类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING, verbose_name='文章类型')
    # content = models.TextField(verbose_name='正文')
    # content = RichTextField(verbose_name='正文')  # 使用富文本编辑器 需要安装和在 settings 中注册 ckeditor 库
    content = RichTextUploadingField(verbose_name='正文')  # 使用富文本编辑器 并添加上传图片、文件功能
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    # readed_num = models.IntegerField(default=0, verbose_name='访问人数')  # 重新建一个新model

    class Meta:
        ordering = ['-created_time']
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist as e:
            return 0

    def __str__(self):
        return "%s" % self.title


class ReadNum(models.Model):
    read_num = models.IntegerField(default=0, verbose_name='访问人数')
    blog = models.OneToOneField(Blog, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '访问人数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.read_num
