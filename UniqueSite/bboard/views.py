from django.shortcuts import render
from django.template import loader, context, Template
from django.views.generic import CreateView, ArchiveIndexView, TemplateView, DetailView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from .models import Bb, Rubric
from .forms import BbForm

def index(request):
	bbs = Bb.objects.all()
	rubrics = Rubric.objects.all()
	context = {'bbs': bbs, 'rubrics': rubrics}
	return render(request, 'bboard/index.html', context)

def by_rubric(request, rubric_id):
	bbs = Bb.objects.filter(rubric = rubric_id)
	rubrics = Bb.objects.all()
	current_rubric = Rubric.objects.get(pk = rubric_id)
	context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
	return render(request, 'bboard/by_rubric.html', context)

class BbCreateView(CreateView):
	template_name = 'bboard/create.html'
	form_class = BbForm
	success_url = reverse_lazy('index')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context

class BbIndexView(TemplateView):
	template_name = 'bboard/index.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['bbs'] = Bb.objects.all()
		context['rubrics'] = Rubric.objects.all()
		return context

class BbDetailView(DetailView):
	model = Bb

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context

class BbByRubricView(ListView):
	template_name = 'bboard/by_rubric.html'
	context_object_name = 'bbs'

	def get_queryset(self):
		return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
		return context

class BbUpdateView(UpdateView):
	model = Bb
	form_class = BbForm
	success_url = '/'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context

class BbDeleteView(DeleteView):
	model = Bb
	success_url = '/'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context

class BbIndexView(ArchiveIndexView):
	model = Bb
	date_field = 'published'
	template_name = 'bboard/index.html'
	context_object_name = 'bbs'
	allow_empty = True

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context