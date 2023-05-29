from django.urls import path

from main.views import MainIndexView, MainList, MainPostView, MainSearchView, FileDownloadView

app_name = "main"

urlpatterns = [
    path("", MainIndexView.as_view(), name='index'),
    path("<str:slug>-<int:id>/", MainList.as_view(), name='list'),
    path("posts/", MainList.as_view(), name='posts'),
    path('download/<int:pk>/', FileDownloadView.as_view(), name='file_download'),
    path("<str:slug>-b<int:pk>/", MainPostView.as_view(), name='post'),
    path("search/", MainSearchView.as_view(), name='search'),
]
