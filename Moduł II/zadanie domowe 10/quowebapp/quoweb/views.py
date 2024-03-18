from django.shortcuts import render, redirect, get_object_or_404
from .form import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote
from django.contrib import messages
from .web_scrap import data
from datetime import datetime
from django.core.paginator import Paginator

# Create your views here.


def main(request):
    quotes = Quote.objects.order_by('id')
    paginator = Paginator(quotes, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'quoweb/index.html', {"page_obj": page_obj})


def detail_quote(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quoweb/detailQuote.html', {"quote": quote})


def detail_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quoweb/detailAuthor.html', {"author": author})


def tag(request):
    if request.user.is_authenticated == False:
        messages.error(request, 'You don\'t have permission to manage tags.')
        return redirect(to='quoweb:main')

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoweb:main')
        else:
            return render(request, 'quotesapp/tag.html', {'form': form})
    return render(request, 'quoweb/tag.html', {'form': TagForm()})


def author(request):
    if request.user.is_authenticated == False:
        messages.error(
            request, 'You don\'t have permission to manage authors.')
        return redirect(to='quotesapp:main')

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoweb:main')
        else:
            return render(request, 'quoweb/author.html', {'form': form})
    return render(request, 'quoweb/author.html', {'form': AuthorForm()})


def quote(request):
    if request.user.is_authenticated == False:
        messages.error(request, 'You don\'t have permission to manage quotes.')
        return redirect(to='quoweb:main')

    tags = Tag.objects.all()
    author = Author.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.author = Author.objects.get(
                fullname=request.POST["author"])
            new_quote.save()
            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            return redirect(to='quoweb:main')
        else:
            return render(request, 'quoweb/quote.html', {"tags": tags, "author": author, 'form': form})
    return render(request, 'quoweb/quote.html', {"tags": tags, "author": author, 'form': QuoteForm()})


def scrape_data(request):
    if request.user.is_authenticated == False:
        messages.error(request, 'You don\'t have permission to manage quotes.')
        return redirect(to='quoweb:main')

    authors, quotes = data()
    for author in authors:
        author_object = Author.objects.get_or_create(
            fullname=author["fullname"],
            born_date=datetime.strptime(
                author["born_date"], "%B %d, %Y").date(),
            born_location=author["born_location"],
            description=author["description"])
        author_object[0].save()
        for quote in quotes:
            quote_object = Quote.objects.get_or_create(
                quote=quote["quote"],
                author=author_object[0])
            for tag in quote["tags"]:
                tag_object = Tag.objects.get_or_create(name=tag)
                quote_object[0].tags.add(tag_object[0])
            quote_object[0].save()

    return redirect(to="quoweb:main")
