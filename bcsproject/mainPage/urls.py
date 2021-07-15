from django.urls import path
from .views import BlockListView, block_detail

urlpatterns = [
    path('', BlockListView.as_view(), name='main'),
    path('blocks/<slug:height>/', block_detail, name='block-detail'),
]