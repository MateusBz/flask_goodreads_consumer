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

if __name__ == '__main__':
    app.run()

