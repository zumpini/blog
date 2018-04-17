from pytz import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
#import bleach

moscow_time = timezone('Europe/Moscow')
#fmt = '%Y-%m-%d %H:%M:%S %Z'
fmt = '%Y-%m-%d %H:%M'

def comments_tree(request, comments):
	page = comments.number
	tree = ''
	i = 0
	qs = []
	if not comments:
		return '<p>Нет комментариев</p>'
	else:
		while True:
			while i < len(comments):
				comment = comments[i]
				if comment.deleted:
					comment_text = '<span class="deleted">Комментарий был удален</span>'
				else:
					comment_text = comment.text
				if comment.user.icon.name:
					image_href = comment.user.icon.url
				else:
					image_href = settings.MEDIA_URL + 'shared/icon.png'
				pub_date = comment.pub_date
				pub_date = pub_date.astimezone(moscow_time).strftime(fmt)
				tree += '<div class="comment" id="{}">\n'.format(comment.id)
				tree += '<img src = "{}" class="icon" title = "Картинка профиля" width = "50" alt="Картинка профиля">\n'.format(image_href)
				tree += '<div class="content">{}</div>\n'.format(comment_text)
				tree += '<div class="container">\n'
				tree += '<a href="{}" class="author">{}</a>'.format(reverse('blog:author', kwargs = {'author':comment.user.username}), comment.user.username)
				tree += '<span class="date">{}</span>\n'.format(pub_date)
				tree += '<br>'
				if request.user.is_authenticated() and request.user == comment.user:
					if comment.deleted:
						tree += '<a href="{}?page={}" class="restore">Восстановить</a>\n'.format(comment.get_absolute_action_url('restore'), page)
					else:
						tree += '<a href="{}?page={}" class="update">Обновить</a>\n'.format(comment.get_absolute_action_url('update'), page)
						tree += '<a href="{}?page={}" class="delete">Удалить</a>\n'.format(comment.get_absolute_action_url('delete'), page)
						tree += '<a href="{}?page={}" class="answer">Ответить</a>\n'.format(comment.get_absolute_action_url('answer'), page)
				else:
					if not comment.deleted:
						tree += '<a href="{}?page={}" class="answer">Ответить</a>\n'.format(comment.get_absolute_action_url('answer'), page)
				tree += '</div>\n'
				if comment.answers.all():
					qs.append([i+1, comments])
					comments = comment.answers.all()
					i = 0
				else:
					tree += '</div>\n'
					i += 1
			if qs:
				i, comments = qs.pop()
				tree += '</div>\n'
			else:
				break
	return tree
