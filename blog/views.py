from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from .forms import RegForm, PostForm, CommentForm, LoginForm, PasswordChangeForm, UpdateForm
from django.forms import Form
from .models import Post, Comment, Cathegory, Statistics, MyUser
from .utils import comments_tree
from django.views.generic import View
from django.contrib.auth import views as auth_views
from django.db.models import Sum
import html

comments_per_page = 10
posts_per_page = 10

class CommentHandler(View):
	def get(self, request, action, pk):
		if not (action in ['answer', 'delete', 'update', 'restore', 'add']):
			raise Http404
		page = request.GET.get('page', '1')
		if not request.user.is_authenticated():
			redirect_string = '{}?next={}?page={}'.format(reverse('blog:user_login'), request.path, page)
			return redirect(redirect_string)
		form = question = None
		if action == 'add':
			post = get_object_or_404(Post, pk = pk)
			form = CommentForm()
			redirect_string = '{}?page={}'.format(reverse('blog:post', kwargs = {'pk':pk}), page)
			action_message = 'Добавить'
			title = 'Добавить комментарий'
			return render(request, 'blog/handler.html', {'form':form, 'question':question, 'action_message':action_message, 'title':title, 'page':page, 'redirect_string':redirect_string})
		elif action == 'answer':
			comment = get_object_or_404(Comment, pk = pk, deleted = False)
			form = CommentForm()
			action_message = 'Добавить'
			title = 'Добавить комментарий'
		elif action == 'delete':
			comment = get_object_or_404(Comment, pk = pk, user = request.user, deleted = False)
			question = 'Вы действительно хотите удалить комментарий?'
			action_message = 'Удалить'
			title = 'Удалить комментарий'
		elif action == 'update':
			comment = get_object_or_404(Comment, pk = pk, user = request.user, deleted = False)
			comment.text = html.unescape(comment.text)
			form = CommentForm(instance = comment)
			action_message = 'Обновить'
			title = 'Обновить комментарий'
		else:
			comment = get_object_or_404(Comment, pk = pk, user = request.user, deleted = True)
			question = 'Вы действительно хотите восстановить комментарий?'
			action_message = 'Восстановить'
			title = 'Восстановить комментарий'
		redirect_string = '{}?page={}#{}'.format(reverse('blog:post', kwargs = {'pk':comment.post.pk}), page, comment.pk)
		return render(request, 'blog/handler.html', {'form':form, 'question':question, 'action_message':action_message, 'title': title, 'page':page, 'redirect_string':redirect_string})
	def post(self, request, action, pk):
		if not (action in ['answer', 'delete', 'update', 'restore', 'add']):
			raise Http404
		page = request.POST.get('page', '1')
		question = None
		if not request.user.is_authenticated():
			redirect_string = '{}?next={}?page={}'.format(reverse('blog:user_login'), request.path, page)
		if action == 'add':
			post = get_object_or_404(Post, pk = pk)
			form = CommentForm(request.POST)
			if not form.is_valid():
				redirect_string = '{}?page={}'.format(reverse('blog:post', kwargs = {'pk':pk}), page)
				action_message = 'Добавить'
				title = 'Добавить комментарий'
				return render(request, 'blog/handler.html', {'form':form, 'question':question, 'action_message':action_message, 'title':title, 'page':page, 'redirect_string':redirect_string})
			comment = form.save(commit = False)
			comment.user = request.user
			comment.post = post
			#comment.text = string_converter(comment.text)
			comment.save()
			redirect_string = '{}#{}'.format(reverse('blog:post', kwargs = {'pk':pk}), comment.pk)
			return redirect(redirect_string)
		elif action == 'answer':
			comment = get_object_or_404(Comment, pk = pk, deleted = False)
			form = CommentForm(request.POST)
			if not form.is_valid():
				redirect_string = '{}?page={}#{}'.format(reverse('blog:post', kwargs = {'pk':comment.post.id}), page, comment.pk)
				action_message = 'Добавить'
				title = 'Добавить комментарий'
				return render(request, 'blog/handler.html', {'form':form, 'question':question, 'action_message':action_message, 'title':title, 'page':page, 'redirect_string':redirect_string})
			reply = form.save(commit = False)
			reply.user = request.user
			reply.post = comment.post
			#reply.text = string_converter(reply.text)
			reply.answer = True
			reply.save()
			comment.answers.add(reply)
			comment.save()
		elif action == 'delete':
			comment = get_object_or_404(Comment, pk = pk, user = request.user, deleted = False)
			comment.deleted = True
			comment.save()
		elif action == 'update':
			comment = get_object_or_404(Comment, pk = pk, user = request.user, deleted = False)
			form = CommentForm(request.POST, instance = comment)
			if not form.is_valid():
				redirect_string = '{}?page={}'.format(reverse('blog:post', kwargs = {'pk':comment.post.id}), page)
				action_message = 'Обновить'
				title = 'Обновить комментарий'
				return render(request, 'blog/handler.html', {'form':form, 'question':question, 'action_message':action_message, 'title':title, 'page':page, 'redirect_string':redirect_string})
			comment = form.save(commit = False)
			#comment.text = string_converter(comment.text)
			comment.save()
		else:
			comment = get_object_or_404(Comment, pk = pk, user = request.user, deleted = True)
			comment.deleted = False
			comment.save()
		redirect_string = '{}?page={}#{}'.format(reverse('blog:post', kwargs = {'pk':comment.post.id}), page, comment.pk)
		return redirect(redirect_string)

class PostPage(View):
	def get(self, request, pk):
		post = get_object_or_404(Post, pk = pk)
		page = request.GET.get('page')
		if not page:
			post.total_views += 1
			post.save()
			if request.user.is_authenticated():
				try:
					entry = get_object_or_404(Statistics, post = post, user = request.user)
					entry.total_views += 1
					entry.save()
				except:
					Statistics.objects.create(post = post, user = request.user, total_views = 1)
			else:
				try:
					entry = get_object_or_404(Statistics, post = post, user__isnull = True)
					entry.total_views += 1
					entry.save()
				except:
					Statistics.objects.create(post = post, total_views = 1)
		comments = post.comment_set.filter(answer = False)
		page = page_gen(page, comments, comments_per_page)
		comments = comments_tree(request, page)
		redirect_string = '{}?page={}'.format(request.path, page.number)
		return render(request, 'blog/post.html', {'post':post, 'comments':comments, 'page':page, 'redirect_string':redirect_string})

class PostHandler(View):
	def get(self, request, action, pk = None):
		if not (action in ['create', 'update', 'delete']):
			raise Http404
		page = request.GET.get('page', '1')
		question = form = None
		if not request.user.is_authenticated():
			redirect_string = '{}?next={}?page={}'.format(reverse('blog:user_login'), request.path, page)
			return redirect(redirect_string)
		if action == 'create':
			form = PostForm()
			action_message = 'Создать'
			title = 'Создать статью'
		elif action == 'update':
			post = get_object_or_404(Post, pk = pk, user = request.user)
			post.content = html.unescape(post.content)
			form = PostForm(instance = post)
			action_message = 'Обновить'
			title = 'Обновить статью'
		else:
			post = get_object_or_404(Post, pk = pk, user = request.user)
			action_message = 'Удалить'
			title = 'Удалить статью'
			question = 'Вы действительно хотите удалить статью?'
		redirect_string = '{}?page={}'.format(reverse('blog:profile'), page)
		return render(request, 'blog/handler.html', {'form':form, 'question':question, 'action_message':action_message, 'title':title, 'page':page, 'redirect_string':redirect_string})
	def post(self, request, action, pk = None):
		if not (action in ['create', 'update', 'delete']):
			raise Http404
		page = request.POST.get('page', '1')
		question = None
		if not request.user.is_authenticated():
			redirect_string = '{}?next={}?page={}'.format(reverse('blog:user_login'), request.path, page)
			return redirect(redirect_string)
		redirect_string = '{}?page={}'.format(reverse('blog:profile'), page)
		if action == 'create':
			form = PostForm(request.POST)
			if not form.is_valid():
				action_message = 'Создать'
				title = 'Создать статью'
				return render(request, 'blog/handler.html', {'form':form, 'question':question, 'action_message':action_message, 'title':title, 'page':page, 'redirect_string':redirect_string})
			post = form.save(commit = False)
			post.user = request.user
			#post.content = string_converter(post.content)
			post.save()
			form.save_m2m()
			redirect_string += '#{}'.format(post.pk)
		elif action == 'update':
			post = get_object_or_404(Post, pk = pk, user = request.user)
			form = PostForm(request.POST, instance = post)
			redirect_string += '#{}'.format(post.pk)
			if not form.is_valid():
				action_message = 'Обновить'
				title = 'Обновить статью'
				return render(request, 'blog/handler.html', {'form':form, 'question':question, 'action_message':action_message, 'title':title, 'page':page, 'redirect_string':redirect_string})
			form.save(commit = False)
			#post.content = string_converter(post.content)
			post.save()
			#form.save_m2m()
		else:
			post = get_object_or_404(Post, pk = pk, user = request.user)
			post.delete()
		return redirect(redirect_string)

def page_gen(page, elements, elements_per_page):
	p = Paginator(elements, elements_per_page)
	try:
		page = p.page(page)
	except:
		page = p.page(1)
	return page

def index(request):
	posts = Post.objects.filter(status = 'p')
	cathegories = Cathegory.objects.all()
	page = request.GET.get('page', '1')
	page = page_gen(page, posts, posts_per_page)
	redirect_string = '{}?page={}'.format(request.path, page.number)
	return render(request, 'blog/index.html', {'page':page, 'cathegories': cathegories, 'redirect_string':redirect_string})

def cathegory(request, cathegory):
	posts = Post.objects.filter(cathegory__name = cathegory.lower(), status = 'p')
	cathegories = Cathegory.objects.all()
	page = request.GET.get('page', '1')
	page = page_gen(page, posts, posts_per_page)
	redirect_string = '{}?page={}'.format(request.path, page.number)
	return render(request, 'blog/cathegory.html', {'page':page, 'cathegory':cathegory, 'cathegories': cathegories, 'redirect_string':redirect_string})

def author(request, author):
	posts = Post.objects.filter(user__username = author, status = 'p')
	cathegories = Cathegory.objects.all()
	page = request.GET.get('page', '1')
	page = page_gen(page, posts, posts_per_page)
	redirect_string = '{}?page={}'.format(request.path, page.number)
	return render(request, 'blog/author.html', {'page':page, 'author':author, 'cathegories': cathegories, 'redirect_string':redirect_string})

def user_logout(request):
	logout(request)
	redirect_string = request.GET.get('next', reverse('blog:index'))
	return redirect(redirect_string)
	
class UserRegister(View):
	def get(self, request):
		form = RegForm()
		action_message = 'Зарегистрировать'
		return render(request, 'blog/handler.html', {'form':form, 'action_message':action_message, 'title':'Регистрация'})
	def post(self, request):
		form = RegForm(request.POST, request.FILES)
		action_message = 'Зарегистрировать'
		if form.is_valid():
			form.save()
			return redirect('blog:index')
		return render(request, 'blog/handler.html', {'form':form, 'action_message':action_message,  'title':'Регистрация'})

class UserUpdate(View):
	def get(self, request):
		if not request.user.is_authenticated():
			redirect_string = '{}?next={}'.format(reverse('blog:user_login'), request.path)
			return redirect(redirect_string)
		
		form = UpdateForm(instance = request.user)
		action_message = 'Обновить'
		return render(request, 'blog/handler.html', {'form':form, 'action_message':action_message, 'title':'Обновить профиль'})
	def post(self, request):
		if not request.user.is_authenticated():
			redirect_string = '{}?next={}'.format(reverse('blog:user_login'), request.path)
			return redirect(redirect_string)
		if request.FILES:
			request.user.icon.delete()
		form = UpdateForm(request.POST, request.FILES, instance = request.user)
		action_message = 'Обновить'
		if form.is_valid():
			form.save()
			return redirect('blog:profile')
		return render(request, 'blog/handler.html', {'form':form, 'action_message':action_message,  'title':'Обновить профиль'})
		
@login_required
def profile(request):
	posts = Post.objects.filter(user = request.user)
	page = page_gen(request, posts, posts_per_page)
	return render(request, 'blog/profile.html', {'page':page})
	
def is_auth(request):
	if not request.user.is_authenticated():
		return HttpResponse(status = 401)
	else:
		return HttpResponse()
		
def statistics(request, pk):
	if not request.user.is_authenticated():
		redirect_string = '{}?next={}'.format(reverse('blog:user_login'), request.path)
		return redirect(redirect_string)
	post = get_object_or_404(Post, pk = pk, user = request.user)
	statistics = Statistics.objects.filter(post = post).order_by('user__username')
	return render(request, 'blog/statistics.html', {'statistics':statistics, 'total_views':post.total_views})
	
def user_login(request):
	return auth_views.login(request,
							template_name = 'blog/handler.html',
							authentication_form = LoginForm,
							extra_context = {'title':'Авторизация', 'action_message':'Войти'})
							
def password_change(request):
	post_change_redirect = '{}?next={}'.format(reverse('blog:user_logout'), reverse('blog:user_login'))
	return auth_views.password_change(request,
							template_name = 'blog/handler.html',
							password_change_form = PasswordChangeForm,
							post_change_redirect = post_change_redirect,
							extra_context = {'title':'Изменить пароль', 'action_message':'Изменить'})