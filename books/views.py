from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from .models import Book, Message

def book_list(request):
    return render(request, 'books/book_list.html')

def about_us(request):
    return render(request, 'books/about.html')

@login_required
def chat_view(request):
    messages = Message.objects.all().order_by('-timestamp')
    return render(request, 'books/chat.html', {'messages': messages})

def home(request):
    books = Book.objects.all()
    return render(request, 'books/home.html', {'books': books})

def post_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        published_date = request.POST.get('published_date')
        Book.objects.create(title=title, author=author, description=description, published_date=published_date)
        return HttpResponse(f"Book '{title}' by {author} posted successfully!")
    return redirect('home') 

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

def download_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Assuming the book file is stored in the 'media' directory
    file_path = f'media/books/{book.title}.pdf'
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{book.title}.pdf')
    return response

# Login Logic
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'books/login.html')

# Sign-Up Logic
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    
    return render(request, 'books/signup.html')

# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Custom 404 Error Redirect
def error_404(request, exception):
    return redirect('signup')

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content)
    return redirect('chat')

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            message.content = content
            message.save()
    return redirect('chat')

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, user=request.user)
    if request.method == 'POST':
        message.delete()
    return redirect('chat')