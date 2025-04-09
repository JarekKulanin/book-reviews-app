from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_list, name='books_list'),
    path('book/<int:pk>', views.book_detail, name='book_detail'),
    path('book/<int:pk>/add-review/', views.add_review_ajax, name='add_review_ajax'),
    path('add-book/', views.add_book, name='add_book'),
    path('api/books/add/', views.AddBookAPIView.as_view(), name='add_book_api'),
    path('api/categories/', views.CategoryListAPIView.as_view(), name='category_list_api'),
]