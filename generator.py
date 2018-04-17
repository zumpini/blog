#from django.contrib.auth.models import User
from blog.models import Post, Cathegory, Comment, MyUser
import datetime
import random

def main():
	def text_generator(seq, length):
		s=''
		for i in range(length):
			s+=random.choice(seq)+' '
		return s.rstrip()

	#Общее количество пользователей
	users_num = 10
	#Макимальное количество статей каждого пользователя
	posts_num = 10
	#Минимальная длина заголовка
	min_title = 1
	#Максимальная длина заголовка
	max_title = 20
	#Минимальная длина статьи
	min_content = 100
	#Максимальная длина статьи
	max_content = 200
	#Каждая статья может принадлежать максимум к двум категориям.
	max_number_of_cathegories = 2

	words = {'математика': ('абсцисса','аксиома',
							'аппликата','асимптота',
							'вектор','гипербола',
							'дискриминант','интеграл',
							'константа','лемма'),
			 'физика':	   ('античастицы','активная инертность',
							'антигравитация','инерция',
							'заряд','импульс',
							'магнитное поле','мюон',
							'плотность','свет'),
			 'генетика':   ('ген','локус',
							'генотип','доминантный признак',
							'аллель','плейотропия',
							'пенетрантность','модификация',
							'вакцина','кроссинговер'),
			 'информатика':('алгоpитм','ассемблер',
							'база данных','байт',
							'вентиль','дисковод',
							'драйвер','интернет',
							'компилятор','отладчик'),
			 'астрономия': ('аберрация','абиогенез',
							'барионий','барстер',
							'звезда','земля',
							'лимб','магнетар',
							'млечный путь','эпакта')}
	users = {'ж':{
			 'имя':['Наталья','Ольга','Лиана','Валентина','Екатерина','Любовь','Ирина','Мария','Светлана','Надежда'],
			 'фамилия':['Демидова','Любимая','Шутова','Ефремова','Пирогова','Долина','Ветрова','Кузнецова','Лаптева','Цыплакова']},
			 'м':{
			 'имя':['Александр','Сергей','Константин','Михаил','Эдуард','Игорь','Владимир','Артур','Денис','Георгий'],
			 'фамилия':['Давыдов','Зотов','Невзоров','Еремин','Проханов','Ефремов','Шафаревич','Михайлов','Пчелкин','Соболев']}
			}

	alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

	#Генерация логинов и паролей.
	#Минимальная длина - 5 символов
	min_length = 5
	#Максимальная длина - 20 символов
	max_length = 20

	Cathegory.objects.bulk_create([Cathegory(name = 'математика'),
							 	   Cathegory(name = 'физика'),
							       Cathegory(name = 'генетика'),
							       Cathegory(name = 'информатика'),
							       Cathegory(name = 'астрономия')])
	cathegories_list = Cathegory.objects.all()
	
	origin_date = datetime.datetime(2000, 1, 1, tzinfo = datetime.timezone.utc)
	current_date = datetime.datetime.now(tz = datetime.timezone.utc)
	current_date = current_date.astimezone(datetime.timezone.utc)
	td = current_date - origin_date
	for i in range(users_num):
		sex = random.choice(('ж', 'м'))
		first_name = random.choice(users[sex]['имя'])
		last_name = random.choice(users[sex]['фамилия'])
		password_length = random.randint(min_length, max_length)
		login_length = random.randint(min_length, max_length)
		login = text_generator(alphabet, login_length).replace(' ', '')
		password = text_generator(alphabet, password_length).replace(' ', '')
		hours = random.randint(0, 23)
		minutes = random.randint(0, 59)
		seconds = random.randint(0, 59)
		reg_date = origin_date + datetime.timedelta(days = random.randint(0, td.days), 
													hours = hours, minutes = minutes, seconds = seconds)
		u = MyUser.objects.create_user(username = login, password = password, first_name = first_name, last_name = last_name)
		u.date_joined = reg_date
		u.save()
		number_of_posts = range(random.randint(0, posts_num))
		for j in number_of_posts:
			rand_length_title = random.randint(min_title, max_title)
			rand_length_content = random.randint(min_content, max_content)
			random_cathegories = random.sample(words.keys(), max_number_of_cathegories)
			rand_words = []
			for cathegory in random_cathegories:
				rand_words.extend(words[cathegory])
			title = text_generator(rand_words, rand_length_title)
			content = text_generator(rand_words, rand_length_content)
			td = current_date - reg_date
			hours = random.randint(0, 23)
			minutes = random.randint(0, 59)
			seconds = random.randint(0, 59)
			pub_date = reg_date + datetime.timedelta(days = random.randint(0, td.days),
													 hours = hours, minutes = minutes, seconds = seconds)
			current_post = Post.objects.create(title = title, content = content, user = u)
			current_post.pub_date = pub_date
			current_post.updated_date = pub_date
			current_post.status = random.choice(('d','p'))
			for c in random_cathegories:
				cathegory = Cathegory.objects.get(name = c)
				current_post.cathegory.add(cathegory)
			current_post.save()

	total_posts = Post.objects.count()
	total_users = MyUser.objects.count()
	min_comment_length = 1
	max_comment_length = 20
	#Максимально допустимое количество комментариев для каждого поста
	total_comments_per_post = 20
	if total_posts:
		random_posts_list = random.sample(range(1, total_posts + 1), random.randint(0, total_posts))
		for i in random_posts_list:
			comments_per_post = random.randint(0, total_comments_per_post)
			if comments_per_post:
				j = 0
				while j < comments_per_post:
					post = Post.objects.get(id = i)
					user = MyUser.objects.get(id = random.randint(1, total_users))
					comment = Comment.objects.create(post = post, user = user)
					td = current_date - post.pub_date
					hours = random.randint(0, 23)
					minutes = random.randint(0, 59)
					seconds = random.randint(0, 59)
					pub_date = post.pub_date + datetime.timedelta(days = random.randint(0, td.days),
													 		  	  hours = hours, minutes = minutes, seconds = seconds)
					comment.pub_date = pub_date
					comment.updated_date = pub_date
					comment.text = text_generator('01', random.randint(min_comment_length, max_comment_length))
					comment.save()
					j += 1
			
main()
