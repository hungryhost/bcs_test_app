import django_filters
from .models import Block
from django import forms


class RequestFilter(django_filters.FilterSet):
	iso_timestamp = django_filters.DateTimeFilter('iso_timestamp__date')

	class Meta:
		model = Block
		fields = [
			'iso_timestamp'
		]
