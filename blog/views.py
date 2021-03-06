from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Blog, BlogType, ReadNum
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from datetime import datetime

# each_page_blogs_number = 5


# Create your views here.

def get_blog_list_common_date(request, blogs_all_list):
    context = {}
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)  # 获取url页码参数 Get请求
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 获取前后各两页的页码
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    # 加上省略页码
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首尾页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取每个分类的文章数量 (方法1)
    # blog_types = BlogType.objects.all()
    # blog_types_list = []
    # for blog_type in blog_types:
    #     blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
    #     blog_types_list.append(blog_type)

    # 方法2
    # BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))

    # 获取每个日期归档的文章数量 (方法1)
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_list = []
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_list.append(blog_date)
        blog_dates_dict[blog_date] = blog_count

    context['page_range'] = page_range
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    # context['blog_types'] = blog_types_list  使用方法2
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_date(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        # 判断文章是否被访问过
        if ReadNum.objects.filter(blog=blog).count():
            readnum = ReadNum.objects.get(blog=blog)
        else:
            readnum = ReadNum(blog=blog)
        readnum.read_num += 1  # 每次打开文章 访问认识 +1
        readnum.save()

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog

    # 设置访问数量,防止每次刷新页面访问数量都会+1
    response = render(request, 'blog/blog_detail.html', context)
    # set_cookie(key, value, 有效时间)
    response.set_cookie('blog_%s_readed' % blog_pk, 'true', max_age=60, expires=datetime)
    return response


def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)

    context = get_blog_list_common_date(request, blogs_all_list)
    context['blog_type'] = blog_type

    return render(request, 'blog/blog_with_type.html', context)


def blog_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)

    context = get_blog_list_common_date(request, blogs_all_list)
    context['blogs_with_dates'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blog_with_date.html', context)
