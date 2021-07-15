from django.db import models
from django.urls import reverse


class Block(models.Model):
	height = models.IntegerField(null=False, blank=False, unique=True)
	hash = models.CharField(max_length=512, null=False, blank=False)
	timestamp = models.IntegerField(null=False, blank=True)
	interval = models.IntegerField(null=False, blank=True)
	size = models.IntegerField(null=False, blank=True)
	transactionCount = models.IntegerField(null=False, blank=True)
	miner = models.CharField(max_length=512, null=False, blank=False)
	reward = models.CharField(max_length=512, null=False, blank=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	iso_timestamp = models.DateTimeField(null=False)

	class Meta:
		db_table = 'blocks'

	def get_absolute_url(self):
		return reverse('block-detail', kwargs={'slug': self.height})