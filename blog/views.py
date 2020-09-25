from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import EmailPostForm

# Create your views here.

class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/post/list.html'

class PostDetailView(DetailView):
	context_object_name = 'posts'
	template_name = 'blog/post/detail.html'
	model = Post
	def get_object(self):
		slug = self.kwargs['post']
		post = get_object_or_404(Post, slug=slug)
		return self.model.objects.filter(slug=slug)
		
	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		print(context)
		return context
		# import pdb; pdb.set_trace()
		# post = get_object_or_404(Post, slug=self.kwargs.get('post'),
		# 						status='published',
		# 						publish__year=self.kwargs.get('year'),
		# 						publish__month=self.kwargs.get('month'),
		# 						publish__day=self.kwargs.get('day'))
		# return post


# def post_list(request):
# 	object_list = Post.published.all()
# 	paginator = Paginator(object_list, 3) # 3 posts in each page
# 	page = request.GET.get('page')
# 	try:
# 		posts = paginator.page(page)
# 	except PageNotAnInteger:
# 	# If page is not an integer deliver the first page
# 		posts = paginator.page(1)
# 	except EmptyPage:
# 	# If page is out of range deliver last page of results
# 		posts = paginator.page(paginator.num_pages)
# 	return render(request, 'blog/post/list.html',{'page': page, 'posts': posts})

# def post_detail(request, year, month, day, post):
# 	posts = get_object_or_404(Post, slug=post,
# 								status='published',
# 								publish__year=year,
# 								publish__month=month,
# 								publish__day=day)
# 	return render(request, 'blog/post/detail.html', {'post': posts})
	
def post_share(request, post_id):
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False
	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_uri())
			subject = f"{cd['name']} recommends to you to read {post.title}"
			message = f"Read {post.title} at {post.url}\n\n"\
					  f"{cd['name']}\'s comments: {cd['comments']}"
			send_mail(subject, message, 'admin@myblog.com'), [cd['to']]
			sent = True
	else:
		form = EmailPostForm()
	return render(request,'blog/post/share.html', {'post': post,
												   'form': form})



