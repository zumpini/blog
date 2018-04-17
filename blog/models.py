from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
import datetime

def upload_to(instance, filename):
	return 'blog/{}/images/'.format(instance.username)

class MyUser(AbstractUser):
	icon = models.ImageField(upload_to = upload_to, blank = True)

class Cathegory(models.Model):
	name = models.CharField(max_length = 50)
	
	def __str__(self):
		return self.name

STATUS = (('d','Черновик'),('p','Публикация'))

class Post(models.Model):
	title = models.CharField(max_length = 100, verbose_name = 'Название')
	content = models.TextField(verbose_name = 'Текст')
	pub_date = models.DateTimeField(default = datetime.datetime.now(), verbose_name = 'Дата публикации')
	updated_date = models.DateTimeField(auto_now = True)
	cathegory = models.ManyToManyField(Cathegory, verbose_name = 'Категория')
	user = models.ForeignKey(MyUser)
	status = models.CharField(max_length = 1, choices = STATUS, default = 'd', verbose_name = 'Статус')
	total_views = models.PositiveIntegerField(default = 0)

	def __str__(self):
		return self.title
	
	def get_absolute_action_url(self, action):
		return reverse('blog:post_handler', kwargs = {'action':action, 'pk':self.pk})
	
	class Meta:
		ordering = ['-pub_date','title']

class Comment(models.Model):
	text = models.TextField()
	post = models.ForeignKey(Post)#on_delete = CASCADE
	user = models.ForeignKey(MyUser)
	answers = models.ManyToManyField('self', symmetrical = False)
	answer = models.BooleanField(default = False)
	pub_date = models.DateTimeField(auto_now_add = True)
	updated_date = models.DateTimeField(auto_now = True)
	deleted = models.BooleanField(default = False)
	
	def get_absolute_action_url(self, action):
		return reverse('blog:comment_handler', kwargs = {'action':action, 'pk':self.pk})

	def __str__(self):
		return self.text

	class Meta:
		ordering = ['-pub_date']
		
class Statistics(models.Model):
	post = models.ForeignKey(Post)
	user = models.ForeignKey(MyUser, null = True)
	total_views = models.PositiveIntegerField(default = 0)
	date = models.DateTimeField(auto_now = True)
	
