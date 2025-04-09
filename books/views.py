from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from .forms import ReviewForm, BookForm
from .models import Book, Category
from .serializers import BookSerializer


def books_list(request):
    category_id = request.GET.get('category')
    search_phrase = request.GET.get('q', '')
    page_number = request.GET.get('page')

    books = Book.objects.all()
    if category_id:
        books = Book.objects.filter(category_id=category_id)

    if search_phrase:
        books = books.filter(
            Q(name__icontains=search_phrase) | Q(author__icontains=search_phrase)
        )
    
    paginator = Paginator(books, 8)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'books': page_obj.object_list,
        'categories': categories,
        'chosen_cat': int(category_id) if category_id and category_id.isdigit() else None,
        'search_phrase': search_phrase,
    }

    return render(request, 'books/books_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all().order_by('-id')

    paginator = Paginator(reviews, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_review = None
    review_form = None

    if request.user.is_authenticated:
        user_review = reviews.filter(author=request.user).first()
        if not user_review:
            review_form = ReviewForm()

    context = {
        'book': book,
        'reviews': page_obj.object_list,
        'page_obj': page_obj,
        'review_form': review_form,
        'user_review': user_review,
    }
    return render(request, 'books/book_detail.html', context)


def add_review_ajax(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Musisz być zalogowany'}, status=403)

    book = get_object_or_404(Book, pk=pk)

    if book.reviews.filter(author=request.user).exists():
        return JsonResponse({'error': 'Już dodałeś recenzję'}, status=400)

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.book = book
        review.author = request.user
        review.save()

        return JsonResponse({
            'review_html': render_to_string('books/review_item.html', {'review': review}, request=request),
            'avg_rating': book.avg_rate
        })

    return JsonResponse({'errors': form.errors}, status=400)


@staff_member_required
def add_book(request):

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('books_list')
    else:
        form = BookForm()

    return render(request, 'books/add_book.html', {'form': form})


class AddBookAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all().values('id', 'name')
        return Response(list(categories))