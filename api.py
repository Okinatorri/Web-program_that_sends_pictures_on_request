from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.secret_key = 'secret_key'
UNSPLASH_ACCESS_KEY = '9wTGZX8KvvSouSWHrxNjvrJp0KwClzHiQsCHlGxYSxo'

# Добавим переменные, которые будут хранить текущее изображение и последний поисковой запрос
current_image = None
last_search_query = None


@app.route('/', methods=['GET', 'POST'])
def index():
    global current_image, last_search_query  # Объявим, что мы используем глобальные переменные

    if request.method == 'POST':
        search_query = request.form.get('search_query')
        if search_query and search_query != "random":
            response = requests.get(f'https://api.unsplash.com/photos/random',
                                    params={'query': search_query, 'client_id': UNSPLASH_ACCESS_KEY})

            if response.status_code == 200:
                current_image = response.json()['urls']['regular']
                last_search_query = search_query

        if search_query == "random" and last_search_query:
            response = requests.get(f'https://api.unsplash.com/photos/random',
                                    params={'query': last_search_query, 'client_id': UNSPLASH_ACCESS_KEY})

            if response.status_code == 200:
                current_image = response.json()['urls']['regular']

    return render_template('index.html', image_url=current_image, search_query=last_search_query)


if __name__ == '__main__':
    app.run(debug=True)
