from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, SubscribersCategory, Author, Category, PostCategory
from .filters import PostFilter
from .forms import PostForm, SubscribeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render

from django.http import HttpResponse
from .tasks import hello, printer


class PostsList(ListView):
    model = Post
    ordering = '-time_add'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class PostsSearch(ListView):
    model = Post
    ordering = '-time_add'
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'post_edit.html', {})

    def post(self, request, *args, **kwargs):
        author = Author.objects.get(user_id=request.user.id)
        post = Post(
            type=request.POST['type'],
            name=request.POST['name'],
            text=request.POST['text'],
            author_id=author.id,
        )
        post.save()
        print(post.id)

        category = PostCategory(
            category_id=request.POST['select'],
            post_id=post.id,
        )
        category.save()
        return redirect('/posts/')

    permission_required = ('news.add_post',)


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    permission_required = ('news.change_post',)



class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PostSubscribe(LoginRequiredMixin, CreateView):
    form_class = SubscribeForm
    model = SubscribersCategory
    template_name = 'post_subscribe.html'

    def post(self, request, *args, **kwargs):
        subscribe = SubscribersCategory(
            category_id=request.POST['category'],
            user_id=request.user.id,
        )
        subscribe.save()

        return redirect('/posts/')


class CView(View):
    def get(self, request):
        printer.delay(3)
        hello.delay()
        return HttpResponse('Hello!')