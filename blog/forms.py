from django import forms
from .models import Post, Cathegory, Comment, MyUser
from django.contrib.auth import forms as auth_forms
from django.core.validators import RegexValidator
from django.core.files.uploadedfile import UploadedFile

class LoginForm(auth_forms.AuthenticationForm):
	username = forms.CharField(label = 'Логин',
								error_messages = {'required':'Поле "Логин" является обязательным.'},
								help_text = 'Поле "Логин" является регистрозависимым.',
								widget = forms.TextInput(attrs = {'required':True, 'autofocus':True, 'pattern':'[A-Za-z_]{1}[A-Za-z0-9_]{4,19}'}))
	password = forms.CharField(label = 'Пароль',
								error_messages = {'required':'Поле "Пароль" является обязательным.'},
								help_text = 'Поле "Пароль" является регистрозависимым.',
								widget=forms.PasswordInput(attrs = {'required': True, 'pattern': '[A-Za-z0-9_]{5,20}'}))
	
	error_messages = {'invalid_login':'Неправильный логин/пароль.', 'inactive':'Данный аккаунт деактивирован.'}
	
class PasswordChangeForm(auth_forms.PasswordChangeForm):
	error_messages = {'password_incorrect':'Ваш текущий пароль указан неправильно.',
						'password_mismatch':'Поля "Новый пароль" и "Подтвердите пароль" должны совпадать.'}
	new_password1 = forms.CharField(label = 'Новый пароль', min_length = 5, max_length = 20,
									error_messages = {'required':'Поле "Новый пароль" является обязательным.',
														'min_length':'Длина поля "Новый пароль" не должна быть меньше 5 символов.',
														'max_length':'Длина поля "Новый пароль" не должна быть больше 20 символов.',
														},
									widget=forms.PasswordInput(attrs = {'required': True, 'pattern': '[A-Za-z0-9_]{5,20}'}),
									help_text = 'Пароль может состоять из прописных и строчных букв латинского алфавита, цифр и символа подчеркивания. '\
												'Длина пароля может варьироваться от 5 до 20 символов включительно.',
									validators = [RegexValidator('^[A-Za-z0-9_]{5,20}$', message = 'Пароль может состоять из прописных и строчных букв латинского алфавита, цифр и символа подчеркивания.')])
	new_password2 = forms.CharField(label = 'Подтвердите пароль', min_length = 5, max_length = 20,
									error_messages = {'required':'Поле "Подтвердите пароль" является обязательным.',
														'min_length':'Длина поля "Подтвердите пароль" не должна быть меньше 5 символов.',
														'max_length':'Длина поля "Подтвердите пароль" не должна быть больше 20 символов.',},
									widget=forms.PasswordInput(attrs = {'required': True, 'pattern': '[A-Za-z0-9_]{5,20}'}))
	old_password = forms.CharField(label = 'Старый пароль', min_length = 5, max_length = 20,
									error_messages = {'required':'Поле "Старый пароль" является обязательным.',
														'min_length':'Длина поля "Старый пароль" не должна быть меньше 5 символов.',
														'max_length':'Длина поля "Старый пароль" не должна быть больше 20 символов.',},
									widget=forms.PasswordInput(attrs = {'required': True, 'pattern': '[A-Za-z0-9_]{5,20}'}))
	

class RegForm(forms.ModelForm):
	username = forms.CharField(label = 'Логин', min_length = 5, max_length = 20,
								error_messages = {'required':'Поле "Логин" является обязательным.',
													'min_length':'Длина поля "Логин" не должна быть меньше 5 символов.',
													'max_length':'Длина поля "Логин" не должна быть больше 20 символов.',
													'unique':'Пользователь с таким логином уже существует.'},
								help_text = 'Логин может состоять из прописных и строчных букв латинского алфавита, цифр и символа подчеркивания. '\
											'Логин может начинаться либо с буквы, либо с символа подчеркивания. '\
											'Длина логина может варьироваться от 5 до 20 символов включительно.',
								widget = forms.TextInput(attrs = {'required': True, 'autofocus': True, 'pattern': '[A-Za-z_]{1}[A-Za-z0-9_]{4,19}'}),
								validators = [RegexValidator('^[A-Za-z_]{1}[A-Za-z0-9_]{4,19}$', message = 'Логин может состоять из прописных и строчных букв латинского алфавита, цифр и символа подчеркивания. '\
																											'Логин может начинаться либо с буквы, либо с символа подчеркивания.')])

	password = forms.CharField(label = 'Пароль', min_length = 5, max_length = 20,
								error_messages = {'required':'Поле "Пароль" является обязательным.',
													'min_length':'Длина поля "Пароль" не должна быть меньше 5 символов.',
													'max_length':'Длина поля "Пароль" не должна быть больше 20 символов.'},
								help_text = 'Пароль может состоять из прописных и строчных букв латинского алфавита, цифр и символа подчеркивания. '\
											'Длина пароля может варьироваться от 5 до 20 символов включительно.',
								widget = forms.PasswordInput(attrs = {'required': True, 'pattern': '[A-Za-z0-9_]{5,20}'}),
								validators = [RegexValidator('^[A-Za-z0-9_]{5,20}$', message = 'Пароль может состоять из прописных и строчных букв латинского алфавита, цифр и символа подчеркивания.')])
	password_confirm = forms.CharField(label = 'Подтвердите пароль', min_length = 5, max_length = 20, 
								error_messages = {'required':'Поле "Подтвердите пароль" является обязательным.',
													'min_length':'Длина поля "Пароль" не должна быть меньше 5 символов.',
													'max_length':'Длина поля "Пароль" не должна быть больше 20 символов.'},
								widget = forms.PasswordInput(attrs = {'required': True, 'pattern': '[A-Za-z0-9_]{5,20}'}))
	
	class Meta:
		model = MyUser
		fields = ('username', 'password', 'password_confirm', 'email', 'first_name', 'last_name')
		labels = {'email':'Почта', 'first_name':'Имя пользователя', 'last_name':'Фамилия пользователя'}
	
	def clean_password_confirm(self):
		password = self.cleaned_data.get('password')
		password_confirm = self.cleaned_data.get('password_confirm')
		if password and password_confirm and password != password_confirm:
			raise forms.ValidationError('Поля "Пароль" и "Подтвердите пароль" должны совпадать.')
		return password_confirm

	def save(self, commit = True):
		user = super(RegForm, self).save(commit = False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

class UpdateForm(forms.ModelForm):
	username = forms.CharField(label = 'Логин', min_length = 5, max_length = 20,
								error_messages = {'required':'Поле "Логин" является обязательным.',
													'min_length':'Длина поля "Логин" не должна быть меньше 5 символов.',
													'max_length':'Длина поля "Логин" не должна быть больше 20 символов.',
													'unique':'Пользователь с таким логином уже существует.'},
								help_text = 'Логин может состоять из прописных и строчных букв латинского алфавита, цифр и символа подчеркивания. '\
											'Логин может начинаться либо с буквы, либо с символа подчеркивания. '\
											'Длина логина может варьироваться от 5 до 20 символов включительно.',
								widget = forms.TextInput(attrs = {'required': True, 'autofocus': True, 'pattern': '[A-Za-z_]{1}[A-Za-z0-9_]{4,19}'}),
								validators = [RegexValidator('^[A-Za-z_]{1}[A-Za-z0-9_]{4,19}$', message = 'Логин может состоять из прописных и строчных букв латинского алфавита, цифр и символа подчеркивания. '\
																											'Логин может начинаться либо с буквы, либо с символа подчеркивания.')])
	class Meta:
		model = MyUser
		fields = ('username', 'email', 'first_name', 'last_name', 'icon')
		labels = {'email':'Почта', 'first_name':'Имя пользователя', 'last_name':'Фамилия пользователя', 'icon':'Картинка'}
		widgets = {'icon': forms.FileInput(attrs = {'accept':'.png, .jpg, .jpeg'})}

class PostForm(forms.ModelForm):
	def clean_cathegory(self):
		if len(self.cleaned_data['cathegory']) > 2:
			raise forms.ValidationError('Статья может принадлежать максимум к двум категориям.', code = 'invalid')
		return self.cleaned_data['cathegory']

	class Meta:
		model = Post
		fields = ['title', 'content', 'pub_date', 'cathegory', 'status']
		error_messages = {
							'title':{
										'required':'Поле "Название" является обязательным.',
										'max_length':'Длина поля "Название" не должна превышать 100 символов.'
									},
							'content':{'required':'Поле "Текст" является обязательным.'},
							'pub_date':{'required':'Поле "Дата публикации" является обязательным.',
										'invalid': 'Указан неправильный формат даты и/или времени. Используйте правильный формат.'},
							'cathegory':{'required':'Поле "Категория" является обязательным.'}
							}
		widgets = {
					'title':forms.TextInput(attrs = {'required':True, 'autofocus':True}),
					'content':forms.Textarea(attrs = {'required':True}),
					'cathegory':forms.SelectMultiple(attrs = {'required':True}),
					'pub_date':forms.DateTimeInput(attrs = {'required':True})
				}
		help_texts = {
						'pub_date':'Для поля "Дата публикации" используйте допустимый формат. Например: 2006-10-25 14:30:59',
						'cathegory':'Статья может принадлежать максимум к двум категориям.'
						}
						
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('text',)
		labels = {'text':'Текст комментария'}
		error_messages = {'text':{'required':'Поле "Текст комментария" является обязательным.'}}
		widgets = {'text': forms.Textarea(attrs = {'required':True, 'autofocus':True})}
		
