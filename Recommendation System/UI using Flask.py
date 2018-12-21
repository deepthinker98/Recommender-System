import mongo as mongo
from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'sdlDB'
app.config['MONGO_URI'] = "mongodb://localhost:27017/sdlDB"

mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        return redirect(url_for('login'))
    else:
        #return "WELCOME TO MOVIE RECOMMENDATION"
        return render_template('h.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('email')
        paswrd = request.form.get('password')

        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})

        if login_user:
            if request.form['password'] == login_user['password']:
                return redirect(url_for('movie_name'))
            else:
                return 'Invalid username/password combination'
        else:
            return 'Invalid username/password combination'
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        number = request.form.get('number')
        email = request.form.get('email')
        paswrd = request.form.get('password')

        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            users.insert({'username': username, 'number': number, 'email': email,'password': paswrd})
            return redirect(url_for('login'))

        return 'That username already exists!'
    else:
        return render_template('register.html')


@app.route('/movie_name', methods=['GET', 'POST'])
def movie_name():
    if request.method == 'GET':
        return render_template('movie_name.html')
    else:
        inp = request.form.get('movie_rec')
        print(inp)
        return redirect(url_for('recommended_movie'))


@app.route('/recommended_movie', methods=['GET', 'POST'])
def recommended_movie():
    if request.method == 'GET':
        url= ['http://image.tmdb.org/t/p/w185//rhIRbceoE9lR4veEXuwCC2wARtG.jpg',
              'https://auto.ndtvimg.com/car-images/medium/jeep/compass/jeep-compass.jpg?v=2',
              'https://auto.ndtvimg.com/car-images/medium/jeep/compass/jeep-compass.jpg?v=2',
              'https://auto.ndtvimg.com/car-images/medium/jeep/compass/jeep-compass.jpg?v=2',
              'https://auto.ndtvimg.com/car-images/medium/jeep/compass/jeep-compass.jpg?v=2',
              'https://auto.ndtvimg.com/car-images/medium/jeep/compass/jeep-compass.jpg?v=2']
        return render_template('recommended_movie.html',url=url)
    else:
        return render_template('recommended_movie.html')


app.run(debug=True)