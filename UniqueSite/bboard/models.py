from django.db import models
from django.contrib.auth.models import User
from django.core import validators

class AdvUser(models.Model):
	is_activated = models.BooleanField(default = True)
	user = models.OneToOneField(User, on_delete = models.CASCADE)

class Spare(models.Model):
	name = models.CharField(max_length = 30)

class Machine(models.Model):
	name = models.CharField(max_length = 30)
	spares = models.ManyToManyField(Spare)

class Bb(models.Model):
	title = models.CharField(max_length = 50, verbose_name = 'Товар',
		validators = [validators.RegexValidator(regex = '^.{4,}$')],
		error_messages = {'invalid': 'Неправильное название товара'})
	content = models.TextField(null = True, blank = True, verbose_name = 'Описание')
	price = models. FloatField(null = True, blank = True, verbose_name = 'Цена')
	published = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name = 'Опубликованно')
	rubric = models.ForeignKey('Rubric', null = True, on_delete = models.PROTECT, verbose_name = 'Рубрика')
	def title_and_prices(self):
		if self.price:
			return '%s (%.2f)' % (self.title, self.price)
		else:
			return self.title
	title_and_prices.short_description = 'Название и цена'

	class Meta:
		verbose_name_plural = 'Объявления'
		verbose_name = 'Объявление'
		ordering = ['-published']

class Rubric(models.Model):
	name = models.CharField(max_length = 20, db_index = True, verbose_name = 'Название')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Рубрики'
		verbose_name = 'Рубрика'
		ordering = ['name']