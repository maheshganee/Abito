from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from Task.models import Post, Comment

# Create your views here.

class DisplayPosts(View):
	def get(self, request, *args, **kwargs):

		posts = Post.objects.all()
		paginator = Paginator(posts, 2)
		try: page = int(request.GET.get("page", '1'))
		except ValueError: page = 1
		try:
			posts = paginator.page(page)
		except (InvalidPage, EmptyPage):
			posts = paginator.page(paginator.num_pages)

		data = {post: [comment.bodytext for comment in Comment.objects.filter(
			post__title=post.title)] for post in posts}
		
		return render(request, 'show_comments.html',
			{'posts_data': data,
			'posts': posts})


class CommentView(View):
	def get(self, request, title):
		users = User.objects.all()
		return render(request, 'add_comment.html',
			{'title': title, 'users': users})


class PostComment(View):
	def post(self, request, *args, **kwargs):

		data = request.POST
		
		try:
			comment_obj = Comment(post=Post.objects.get(title=data.get('title_name')),
				bodytext=data.get('bodytext'),
				user=User.objects.get(username=data.get('user')))
			comment_obj.save()
			data = {post: [comment.post.bodytext for comment in Comment.objects.filter(
				post__title=post.title)] for post in Post.objects.all()}
			return HttpResponseRedirect('/posts/')
		except:
			return HttpResponseRedirect('/posts/')

	def get(self, request, *args, **kwargs):
		return HttpResponseRedirect('/posts/')