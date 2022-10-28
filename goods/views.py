from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from .models import GoodsModel

class GoodsView(TemplateView):
    template_name = 'goods/good_info.html'
    def get_context_data(self, **kwargs):

        context=super().get_context_data(**kwargs)
        pk=kwargs.get('pk')

        good=GoodsModel.objects.get(pk=pk)
        context['good']=good
        return context