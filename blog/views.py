from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Post
from users.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# function_based view
# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


# class_based view :
class PostListView(ListView):
    model = Post
    template_name = "blog/home.html" # <app>/<model>_<viewtype>.html     exmp: blog/post_List.html
    context_object_name = "posts"
    ordering = ['-date_posted']
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curr_page = context['page_obj'].number
        end = context['page_obj'].paginator.num_pages
        my_range = range(max(curr_page - 2, 1), min(curr_page + 2 + 1, end + 1))
        context['my_range'] = my_range
        return context

# class_based view :
class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html" # <app>/<model>_<viewtype>.html     exmp: blog/post_List.html
    context_object_name = "posts"
    ordering = ['-date_posted']
    paginate_by = 3
    
    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return super().get_queryset().filter(author=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curr_page = context['page_obj'].number
        end = context['page_obj'].paginator.num_pages
        my_range = range(max(curr_page - 2, 1), min(curr_page + 2 + 1, end + 1))
        context['my_range'] = my_range
        return context
    
    

class PostDetailView(DetailView):
    model = Post


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
        return post.author == self.request.user

class PostDeleteVeiw(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
def about(request):
    return render(request, 'blog/about.html', {"title": 'xxx'})