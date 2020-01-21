from django.shortcuts import render, redirect
from django.template import loader, context, Template
from django.views.generic import CreateView, ArchiveIndexView, TemplateView, DetailView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME

from .models import Bb, Rubric
from .forms import BbForm

def index(request):
	bbs = Bb.objects.all()
	rubrics = Rubric.objects.all()
	context = {'bbs': bbs, 'rubrics': rubrics}
	return render(request, 'bboard/index.html', context)

def rubrics(request):
	RubricFormSet = modelformset_factory(Rubric, fields=('name',), can_order=True, can_delete=True)
	if request.method == 'POST':
		formset = RubricFormSet(request.POST)
		if formset.is_valid():
			for form in formset:
				if form.cleaned_data:
					rubric = form.save(commit=False)
					rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
					rubric.save()
			return redirect('bboard:index')
	else:
		formset = RubricFormSet()
	context = {'formset': formset}
	return render(request, 'bboard/rubrics.html', context)

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

def index(request):
	rubrics = Rubric.objects.all()
	bbs = Bb.objects.all()
	paginator = Paginator(bbs, 2)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	context = {'rubrics': rubrics, 'page': page, 'bbs': page.object_list}
	return render(request, 'bboard/index.html', context)
