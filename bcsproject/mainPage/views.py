from typing import Optional
from django.db import models
import requests
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import datetime

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView

# from .forms import DateForm
from .filters import RequestFilter
from .models import Block
from helpers.fetcher import fetch_blocs


def block_detail(request, height):
	block = Block.objects.get(height=height)
	block_admin_url = reverse(
		'admin:%s_%s_change' % (block._meta.app_label, block._meta.model_name),
		args=[block.id])
	return render(
		request,
		'mainPage/block_detail.html',
		{'single_block': block, 'admin_url': block_admin_url})


class BlockListView(ListView):
	model = Block
	template_name = 'mainPage/block_list.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'blocks'
	paginate_by = 50

	def get_context_data(self, **kwargs):
		context = super(BlockListView, self).get_context_data(**kwargs)
		if not self.queryset:
			try:
				fetch_blocs(date=self.request.GET.get('iso_timestamp'))
				self.get_queryset()
			except Exception as e:
				pass
		filtered_list = RequestFilter(self.request.GET, queryset=self.queryset)
		paginator = Paginator(filtered_list.qs, self.paginate_by)

		page = self.request.GET.get('page')
		filter_param_1 = self.request.GET.get('iso_timestamp', None)
		try:
			response = paginator.page(page)
		except PageNotAnInteger:
			response = paginator.page(1)
		except EmptyPage:
			response = paginator.page(paginator.num_pages)

		if filter_param_1 is None:
			# if there is no GET param, look in the session
			filter_param_1 = self.request.session.get('iso_timestamp', None)
		else:
			# if there is a GET param, store it in the session for the next time
			self.request.session['filter_param_1'] = filter_param_1
		context['filter_param_1'] = filter_param_1
		context['filter'] = filtered_list
		context['filter_qs'] = response
		context['count'] = len(response)
		return context
