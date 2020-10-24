import requests
import re
import xml.etree.ElementTree as ET
from flask import Flask
from flask import request, render_template
from decouple import config

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def results():
    if request.method == 'POST':
        query = request.form.get('query')
        res = requests.get('https://www.goodreads.com/search.xml?', params={
                                'key': config('API_KEY'),
                                'q': query
                            })
        root = ET.fromstring(res.content)

        elements = root.findall('./search/results/work/best_book/id')
        books_id = [item.text for item in elements]

        elements = root.findall('./search/results/work/best_book/title')
        titles = [item.text for item in elements]

        elements = root.findall('./search/results/work/best_book/author/id')
        authors_id = [item.text for item in elements]

        elements = root.findall('./search/results/work/best_book/author/name')
        authors = [item.text for item in elements]

        elements = root.findall('./search/results/work/best_book/image_url')
        links = [item.text for item in elements]
        images_urls = []
        for item in links:
            images_urls.append(re.sub('._SX98_', '', item))
        
        content = zip(books_id, titles, authors_id, authors, images_urls)
        
    return render_template('results.html', content=content)


@app.route('/<int:id>/about_book', methods=['GET'])
def about_book(id):
    res = requests.get(
        'https://www.goodreads.com/book/show/?', params={
            'id': id,
            'format': 'xml',
            'key': config('API_KEY')
        })
    root = ET.fromstring(res.content)

    book_isbn = root.find('./book/isbn').text
    book_title = root.find('book/title').text
    book_description = root.find('./book/description').text

    book_img = root.find('./book/image_url').text
    book_large_img = re.sub('._SX98_', '', book_img)
    book_publication_year = root.find('./book/publication_year').text
    book_publisher = root.find('./book/publisher').text

    elements = root.findall('./book/authors/author/id')
    authors_id = [item.text for item in elements]

    elements = root.findall('./book/authors/author/name')
    authors_names = [item.text for item in elements]

    authors = list(zip(authors_id, authors_names))
     
    content = {
        'book_isbn': book_isbn,
        'book_title': book_title,
        'book_description': book_description,
        'book_img': book_large_img,
        'book_publication_year': book_publication_year,
        'book_publisher': book_publisher,
        'authors': authors
        
    }
    return render_template('about_book.html', content=content)


@app.route('/<int:id>/about_author', methods=['GET'])
def about_author(id):
    res = requests.get(
        'https://www.goodreads.com/author/show/?', params={
            'id': id,
            'format': 'xml',
            'key': config('API_KEY')
        })
    root = ET.fromstring(res.content)

    author_name = root.find('./author/name').text
    author_image = root.find('./author/large_image_url').text
    author_about = root.find('./author/about').text

    elements = root.findall('./author/books/book/id')
    author_books_id = [item.text for item in elements]

    elements = root.findall('./author/books/book/title')
    author_books_title = [item.text for item in elements]

    author_books = list(zip(author_books_id, author_books_title))

    content = {
        'author_name': author_name,
        'author_image': author_image,
        'author_about': author_about,
        'author_books': author_books
    }

    return render_template('about_author.html', content=content)


