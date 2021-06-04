from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import CommentForm
from .models import Post, Comment


def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class OldListView(ListView):
    model = Post
    template_name = 'blog/old_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['date_posted']


class FamousListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/famous_blog.html'
    paginate_by = 5
    ordering = ['likes']


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        data = super(PostDetailView, self).get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['total_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html')


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'
    ordering = ['-date_posted']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        comment = form.save(commit=False)
        form.instance.post_id = self.kwargs.get('pk')
        comment.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Post.objects.all().order_by('-date_posted')


        # form.instance.post_id = self.kwargs['pk']
        # return super().form_valid(form)


def SearchPage(request):
    if request.method == 'GET':
        srh = request.GET['query']
        context = {'posts': Post.objects.all().filter(title=srh)}

        return render(request, 'blog/search_page.html', context)

