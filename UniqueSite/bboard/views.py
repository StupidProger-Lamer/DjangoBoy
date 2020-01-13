from django.shortcuts import render
from django.template import loader, context, Template
from django.views.generic.edit import CreateView
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

# def add_and_save(request):
# 	if request.method == 'POST':
# 		bbf = BbForm(request.POST)
# 		if bbf.is_valid():
# 			bbf.save()
# 			return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric id': bbf.cleaned_data['rubric'].pk}))
# 		else:
# 			context = {'form': bbf}
# 			return render(request, 'bboard/create.html', context)
# 	else:
# 		ЬЬf = BbForm()
# 		context = {'form': bbf}
# 		return render(request, 'bboard/create.html', context)

class BbCreateView(CreateView):
	template_name = 'bboard/create.html'
	form_class = BbForm
	success_url = reverse_lazy('index')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['rubrics'] = Rubric.objects.all()
		return context
