from vanilla import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from .models import Post, PostCategory
from .filters import PostFilter
from django.http import HttpResponse

class AllPostsView(ListView):
    template_name = 'posts.html'
    model = Post
    paginate_by = 10

    def get_queryset(self):
    	post_filter = PostFilter(self.request.GET, Post.objects.all().order_by('-created'))
    	return post_filter

    def get_context_data(self, **kwargs):
        context = super(AllPostsView, self).get_context_data(**kwargs)
        context['categories'] = PostCategory.objects.all()
        context['selected_categories'] = map(int, self.request.GET.getlist('category')) if 'category' in self.request.GET else []
        context['specified_name'] = self.request.GET['name'] if 'name' in self.request.GET else ''
        return context

class PostDetail(DetailView):
	template_name = 'post_detail.html'
	model = Post

class CreatePost(CreateView):
    template_name='new_post.html'
    model=Post 
    fields=('name', 'content', 'category')
    success_url='/blog'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePost, self).form_valid(form)

@login_required
def like_post(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']

    if post_id:
        post = Post.objects.get(id = int(post_id))
        post.liked_by.add(request.user)
        likes = post.liked_by.count()
        post.save()

        return HttpResponse(likes)

    return HttpResponse()