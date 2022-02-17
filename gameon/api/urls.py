from functools import reduce
from django.urls import path
from .views import (WatchListView, WatchListDetail, StreamPlatformView, StreamPlatformDetail, 
                    ReviewList, ReviewDetail,ReviewCreate,UserReview, WatchListSearch)

urlpatterns = [
    path('',WatchListView.as_view(),name='watchlist'),
    path('<int:pk>/',WatchListDetail.as_view(),name='watchlist_detail'),
    path('stream/',StreamPlatformView.as_view(),name='streamplatform'),
    path('stream/<int:pk>/',StreamPlatformDetail.as_view(),name='streamplatform_detail'),
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create'),
    path('<int:pk>/review/',ReviewList.as_view(),name='review-list'),
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review_detail'),
    # path('review/<str:username>/',UserReview.as_view(),name='user'), case 1 
    path('review/',UserReview.as_view(),name='user-review'),
    path('watchlist/',WatchListSearch.as_view(),name='watchlist_search'),

]