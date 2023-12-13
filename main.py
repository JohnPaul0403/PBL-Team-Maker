#Project Team Maker

#This project is for making teams based on their score
#The user will input the number of team members (n) it want as input

#Libraries Import 
from Database import professors_database as pd
from Database import data_classes as dtc
from Data_proccess import random_groups as rg
from Data_proccess import predict_note as pn
from chat_bot import chat_bot as cb
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sock import Sock
import json

#Main function, no variable declaration
def main():
    app = Flask(__name__)
    sock = Sock(app)
    app.secret_key = "sddddd"

    #Index page
    @app.route('/')
    def index_page():
        return render_template('index.html') 

    #-----------Login page and methods-----------#
    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route('/login/get_login', methods = ["POST", "GET"])
    def get_login():
        if request.method == 'POST':
            user_auth = [request.form['username'], request.form['password']]
            return redirect(url_for("auth_login", user = user_auth[0], password = user_auth[1]))

        flash("Internal problem. Please try again!")
        return redirect(url_for("login_page"))

    @app.route('/login/get_login/auth_login')
    def auth_login():
        #Variable declaration
        user = [request.args.get("user"), request.args.get("password")]
        profs = pd.read_professors()
        for row in profs:
            name, prof_id, students = row
            if name == user[0] and prof_id == user[1]:
                session.pop('_flashes', None)
                session['username'] = prof_id
                return redirect(url_for("dashboard_page", prof = name))

        flash("Invalid username or password. Please try again!")    
        return redirect(url_for("login_page"))

    @app.route('/login/get_logout')
    def get_logout():
        session.pop('username', None)
        return redirect(url_for("login_page"))

    #--------------------Blogs' page and blog getters--------------------#
    @app.route('/blogs/')
    def blogs_page():

        with open('blogs.json', 'r') as file:
            data = json.load(file)

        blogs = list(data["data"]["blogs"])
        blogs.reverse()

        return render_template('blogs_page.html', blogs = blogs)

    @app.route('/blogs/<blog_id>')
    def blog_page(blog_id):
        my_blog = None

        with open('blogs.json', 'r') as file:
            data = json.load(file)

        for blog in data['data']['blogs']:
            print(f'{blog["id"] ==blog_id}, {blog_id}')
            if blog['id'] == int(blog_id):
                my_blog = blog

        if my_blog is None:
            return render_template('404_page.html')

        return render_template('blog_page.html', blog = my_blog)

    #--------------------Conctact Us page--------------------#
    @app.route('/contacts/')
    def contacts_page():
        return render_template('contacts_page.html')
    
    @app.route("/chat/")
    def chat_page():
        return render_template("chat.html")
    
    @sock.route("/echo")
    def echo(sock):
        client = cb.set_client()
        while True:
            data = sock.receive()
            response = cb.send_message(client, data)
            sock.send(response)

    #--------------------Dashboard Page and functions--------------------#
    @app.route('/prof/<prof>')
    def dashboard_page(prof):

        #Variable declaration
        profs = pd.read_professors()
        prof_class = None

        #Create prof object and getting information
        if 'username' not in session:
            return redirect(url_for("login_page"))

        for row in profs:
            name, prof_id, students = row
            if prof_id == session["username"] and name == prof:
                prof_class = dtc.Professor(name, prof_id)

        if not prof_class:
            return redirect(url_for("login_page"))

        #Variable data declaration
        prof_class.get_students()
        prof_class.sort_students()

        try:
            scores = [int(i.score) for i in prof_class.students]
            average = rg.average_nums(scores)
        except Exception:
            scores = [0, 0]
            average = "No data yet"

        return render_template(
            'prof_dashboard.html', 
            name = prof_class.name, 
            students = prof_class.students, 
            average = average,
            min_score = min(scores),
            max_score = max(scores)
        )

    @app.route('/prof/teams', methods = ['POST', "GET"])
    def teams_page():

        #varible declaration
        if request.method != 'POST':
            session.pop('_flashes', None)
            return redirect(url_for("login_page"))
        
        try:
            team_input = int(request.form['team_input'])
        except Exception:
            team_input = 0

        if team_input <= 0:
            flash("Incorect value. Please try again!")
            prof_name = pd.get_name_by_id(session['username'])
            return redirect(url_for("dashboard_page", prof = prof_name))

        #Removing flash messages
        session.pop('_flashes', None)

        profs = pd.read_professors()
        prof_class = None

        #Create prof object and getting information
        if 'username' not in session:
            return redirect(url_for("login_page"))

        for row in profs:
            name, prof_id, students = row
            if prof_id == session["username"]:
                prof_class = dtc.Professor(name, prof_id)

        if not prof_class:
            return redirect(url_for("login_page"))

        #Variable data declaration
        prof_class.get_students()
        my_students = [student.to_jason() for student in prof_class.students]
        team_input = team_input if team_input <= int(len(my_students) / 2) else int(len(my_students) / 2)

        if rg.scores_same(my_students) :
            teams = rg.create_random_teams(my_students, team_input)
            return render_template("random_teams_page.html", teams = teams)
        
        teams, averages = rg.create_teams_pos(my_students, team_input)
        predicted_note = [pn.get_score(i) for i in averages]

        return render_template("teams_page.html", teams = teams, averages = averages, predicted_note = predicted_note)


    app.run(debug=True)

#Main function call
if __name__ == "__main__" :
    main()
