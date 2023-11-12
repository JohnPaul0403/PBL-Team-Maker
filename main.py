#Project Team Maker

#This project is for making teams based on their score
#The user will input the number of team members (n) it want as input

#Libraries Import 
from Database import professors_database as pd
from Database import data_classes as dtc
from Data_proccess import groups_bounderies as gb
from Data_proccess import data_sorting as ds
from Data_proccess import random_groups as rg
from Data_proccess import predict_note as pn
from flask import Flask, render_template, request, redirect, url_for, flash, session

#Main function, no variable declaration
def main():
    app = Flask(__name__)
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
        return render_template('blogs_page.html')
    
    #--------------------Conctact Us page--------------------#
    @app.route('/contacts/')
    def contacts_page():
        return render_template('contacts_page.html')
    
    #--------------------Dashboard Page and functions--------------------#
    @app.route('/prof/<prof>')
    def dashboard_page(prof):
        
        #Variable declaration
        profs = pd.read_professors()
        prof_class = None

        #Create prof object and getting information
        if not 'username' in session:
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
            average = gb.average_nums(scores)
        except:
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
        if request.method == 'POST':
            team_input = int(request.form['team_input'])
        else:
            return redirect(url_for("login_page"))
        
        profs = pd.read_professors()
        prof_class = None

        #Create prof object and getting information
        if not 'username' in session:
            return redirect(url_for("login_page"))
        
        for row in profs:
            name, prof_id, students = row
            if prof_id == session["username"]:
                prof_class = dtc.Professor(name, prof_id)

        if not prof_class:
            return redirect(url_for("login_page"))

        #Variable data declaration
        prof_class.get_students()
        prof_class.sort_students()
        my_students = [student.to_jason() for student in prof_class.students]
        team_input = team_input if team_input <= int(len(my_students) / 2) else int(len(my_students) / 2)

        if rg.scores_same(my_students) :
            teams = rg.create_random_teams(my_students, team_input)
        else:
            teams, averages = ds.get_teams(my_students, team_input)
            predicted_note = [pn.get_score(i) for i in averages]

            return render_template("teams_page.html", teams = teams, averages = averages, predicted_note = predicted_note)
        
        return render_template("random_teams_page.html", teams = teams)
    
    app.run(host="0.0.0.0", port=8000, debug=True)

#Main function call
if __name__ == "__main__" :
    main()
