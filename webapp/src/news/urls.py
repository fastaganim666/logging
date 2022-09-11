from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, PostsSearch, PostSubscribe, CView
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', cache_page(60*10)(PostDetail.as_view()), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostsSearch.as_view(), name='post_search'),
   path('subscribe/', PostSubscribe.as_view(), name='post_subscribe'),
   path('celery/', CView.as_view()),
]