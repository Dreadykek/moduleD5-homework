from django.shortcuts import render, redirect
from .models import Book, Publishing_house, Author, Friend
from .forms import AuthorForm, BookForm
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader
from django.forms import formset_factory
from django.http.response import HttpResponseRedirect

# Create your views here.
def books_list(request):
    template = loader.get_template('title.html')
    return HttpResponse(template.render())

def index(request):
    template = loader.get_template('index.html')
    books = Book.objects.all()
    numbers = []
    for i in range(1, 100):
        numbers.append(i)
    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
        "numbers": numbers,
    }
    return HttpResponse(template.render(biblio_data, request))

def borrow(request):
    template = loader.get_template('borrow.html')
    friends = Friend.objects.all()
    biblio_data = {
        "title":  "У кого какие книги",
        "friends": friends,
    }
    return HttpResponse(template.render(biblio_data, request))

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

def publishing_house(request):
    template = loader.get_template('publishing_house.html')
    books = Book.objects.all()
    houses = Publishing_house.objects.all()

    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
        "houses": houses,
    }
    return HttpResponse(template.render(biblio_data, request))


class AuthorEdit(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_library:author_list')
    template_name = 'author_edit.html'


class AuthorList(ListView):
    model = Author
    template_name = 'authors_list.html'

def author_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)

    if request.method=="POST":
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix="authors")

        if author_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            return HttpResponseRedirect(reverse_lazy('p_labrary:author_list'))
    else:
        author_formset = AuthorFormSet(prefix="authors")
    return render(request, 'manage_authors.html', {'author_formset':author_formset})

def books_authors_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if author_formset.is_valid() and book_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            for book_form in book_formset:
                book_form.save()
            return HttpResponseRedirect(reverse_lazy('p_library:author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render(
	    request,
		'manage_books_authors.html',
		{
	        'author_formset': author_formset,
			'book_formset': book_formset,
		}
	)