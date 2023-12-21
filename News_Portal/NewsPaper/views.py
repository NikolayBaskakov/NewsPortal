from typing import Any
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from.filters import PostFilter
from .models import Post, Category, Subscriber
from .forms import *
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
# Create your views here.
class NewsList(ListView):
    model = Post
    ordering = 'date'
    template_name = 'News.html'
    context_object_name ='News'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.filter(type='NW')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    
class ArticleList(NewsList):
    template_name = 'Articles.html'
    def get_queryset(self):
        queryset = Post.objects.filter(type='AR')
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
        
    
    
class NewsDetail(DetailView):
    model = Post
    template_name = 'NewsOne.html'
    context_object_name = 'NewsOne'
    
def post_search(request):
    queryset = Post.objects.all()
    filterset = PostFilter(request.GET, queryset)
    context = {'filterset':filterset, 'path':request.path}
    return render(request, 'search.html', context )

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPaper.add_post')
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    
class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPaper.add_post')
    form_class = ArticlesForm
    model = Post
    template_name = 'post_edit.html'
    
class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPaper.change_post')
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    
class ArticlesEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPaper.change_post')
    form_class = ArticlesForm
    model = Post
    template_name = 'post_edit.html'
    
class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPaper.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    
class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPaper.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    
@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
    
