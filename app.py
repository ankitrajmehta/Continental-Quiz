from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL


from helper import login_required
from questions import qn_options_asia, qn_options_africa, qn_options_europe, qn_options_oceania, qn_options_s_america,qn_options_n_america

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure the database
db = SQL("sqlite:///user.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        if "how" in request.form:
            return redirect("/how")
        else:
            return redirect("/map")
    else:
        return render_template("home.html")

@app.route("/login", methods=["GET" , "POST"])
def login():
    session.clear()
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must enter a username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must enter a password")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Invalid Username and/or Password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]
    
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout", methods=["POST" , "GET"])
def logout():
    # Forget any user_id
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "Post"])
def register():
    if request.method == "POST":

        if not request.form.get("username"):
            flash("Must enter a username.")
            return redirect("/register")
        elif not request.form.get("password") or not request.form.get("confirm_password"):
            flash("Must enter password as well as confirmation.")
            return redirect("/register")

        elif not request.form.get("password") == request.form.get("confirm_password"):
            flash("Password and confirm password does not match.")
            return redirect("/register")

        #check length of username
        if len(request.form.get("username")) > 10:
            flash("Max username length is 10")
            return redirect("/register")

        #check if username is available
        same_user = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))
        if len(same_user) > 0:
            flash("username not available")
            return redirect("/register")
        
        hashed = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", request.form.get("username"), hashed)
        # log in registered user
        current_user_data = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = current_user_data[0]["user_id"]

        create_database_entry(session["user_id"])
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/map")
@login_required
def map():
    return render_template("map.html")

@app.route("/how")
@login_required
def how():
    username= db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])
    return render_template("how.html", user=username[0]["username"])



@app.route("/asia", methods=["GET", "POST"])
@login_required
def asia():
    global qn_options_asia
    values = db.execute("SELECT * FROM asia WHERE user_id = ?", session["user_id"])

    current_qn = values[0]["current_qn"]
    score = values[0]["score"]
    user_ans = "none"
     
    test=current_qn
    if request.method=="POST":
        test = request.form.get("test")
        if int(test) <= int(current_qn -1):
            return redirect("/asia")
        user_ans = request.form.get("user_ans")
        current_qn += 1
        ans_of = current_qn - 1
        db.execute("UPDATE asia SET current_qn = ? WHERE user_id = ?", current_qn, session["user_id"])
        if qn_options_asia[ans_of][5] == user_ans:
            score+= 1
            db.execute("UPDATE asia SET score = ? WHERE user_id = ?", score, session["user_id"])
    if current_qn < len(qn_options_asia):
        return render_template("quiz.html",quiz="Asia", action="asia", qn_options=qn_options_asia, qn_n=current_qn)
    else:
        return render_template("thanku.html",quiz="Asia",score=score )



@app.route("/africa", methods=["GET", "POST"])
@login_required
def africa():
    global qn_options_africa
    values = db.execute("SELECT * FROM africa WHERE user_id = ?", session["user_id"])

    current_qn = values[0]["current_qn"]
    score = values[0]["score"]
    user_ans = "none"
     
    if request.method=="POST":
        test = request.form.get("test")
        if int(test) <= int(current_qn -1):
            return redirect("/africa")
        user_ans = request.form.get("user_ans")
        current_qn += 1
        ans_of = current_qn - 1
        db.execute("UPDATE africa SET current_qn = ? WHERE user_id = ?", current_qn, session["user_id"])
        if qn_options_africa[ans_of][5] == user_ans:
            score+= 1
            db.execute("UPDATE africa SET score = ? WHERE user_id = ?", score, session["user_id"])
    if current_qn < len(qn_options_africa):
        return render_template("quiz.html",quiz="Africa", action="africa" , qn_options=qn_options_africa, qn_n=current_qn)
    else:
        return render_template("thanku.html",quiz="Africa",score=score )


@app.route("/europe", methods=["GET", "POST"])
@login_required
def europe():
    global qn_options_europe
    values = db.execute("SELECT * FROM europe WHERE user_id = ?", session["user_id"])

    current_qn = values[0]["current_qn"]
    score = values[0]["score"]
    user_ans = "none"
     
    if request.method=="POST":
        test = request.form.get("test")
        if int(test) <= int(current_qn -1):
            return redirect("/europe")
        user_ans = request.form.get("user_ans")
        current_qn += 1
        ans_of = current_qn - 1
        db.execute("UPDATE europe SET current_qn = ? WHERE user_id = ?", current_qn, session["user_id"])
        if qn_options_europe[ans_of][5] == user_ans:
            score+= 1
            db.execute("UPDATE europe SET score = ? WHERE user_id = ?", score, session["user_id"])
    if current_qn < len(qn_options_europe):
        return render_template("quiz.html",quiz="Europe", action="europe", qn_options=qn_options_europe, qn_n=current_qn)
    else:
        return render_template("thanku.html",quiz="Europe",score=score )


@app.route("/oceania", methods=["GET", "POST"])
@login_required
def oceania():
    global qn_options_oceania
    values = db.execute("SELECT * FROM oceania WHERE user_id = ?", session["user_id"])

    current_qn = values[0]["current_qn"]
    score = values[0]["score"]
    user_ans = "none"
    
    
    test=current_qn
    if request.method=="POST":
        test = request.form.get("test")
        if int(test) <= int(current_qn -1):
            return redirect("/oceania")
        user_ans = request.form.get("user_ans")
        current_qn += 1
        ans_of = current_qn - 1
        db.execute("UPDATE oceania SET current_qn = ? WHERE user_id = ?", current_qn, session["user_id"])
        if qn_options_oceania[ans_of][5] == user_ans:
            score+= 1
            db.execute("UPDATE oceania SET score = ? WHERE user_id = ?", score, session["user_id"])
    if current_qn < len(qn_options_oceania):
        return render_template("quiz.html",quiz="Oceania", action="oceania", qn_options=qn_options_oceania, qn_n=current_qn)
    else:
        return render_template("thanku.html",quiz="Oceania",score=score )

@app.route("/s_america", methods=["GET", "POST"])
@login_required
def s_america():
    global qn_options_s_america
    values = db.execute("SELECT * FROM s_america WHERE user_id = ?", session["user_id"])

    current_qn = values[0]["current_qn"]
    score = values[0]["score"]
    user_ans = "none"


    test=current_qn
    if request.method=="POST":
        test = request.form.get("test")
        if int(test) <= int(current_qn -1):
            return redirect("/s_america")
        user_ans = request.form.get("user_ans")
        current_qn += 1

        ans_of = current_qn - 1
        db.execute("UPDATE s_america SET current_qn = ? WHERE user_id = ?", current_qn, session["user_id"])
        if qn_options_s_america[ans_of][5] == user_ans:
            score+= 1
            db.execute("UPDATE s_america SET score = ? WHERE user_id = ?", score, session["user_id"])
    if current_qn < len(qn_options_s_america):
        return render_template("quiz.html",quiz="South America", action="s_america", qn_options=qn_options_s_america, qn_n=current_qn )
    else:
        return render_template("thanku.html",quiz="South America",score=score )


@app.route("/n_america", methods=["GET", "POST"])
@login_required
def n_america():
    global qn_options_n_america
    values = db.execute("SELECT * FROM n_america WHERE user_id = ?", session["user_id"])

    current_qn = values[0]["current_qn"]
    score = values[0]["score"]
    user_ans = "none"

    test = current_qn
    if request.method=="POST":
        test = request.form.get("test")
        if int(test) <= (current_qn -1):
            return redirect("/n_america")
        user_ans = request.form.get("user_ans")
        current_qn += 1
        ans_of = current_qn - 1
        db.execute("UPDATE n_america SET current_qn = ? WHERE user_id = ?", current_qn, session["user_id"])
        if qn_options_n_america[ans_of][5] == user_ans:
            score+= 1
            db.execute("UPDATE n_america SET score = ? WHERE user_id = ?", score, session["user_id"])
    if current_qn < len(qn_options_n_america):
        return render_template("quiz.html",quiz="North America", action="n_america", qn_options=qn_options_n_america, qn_n=current_qn)
    else:
        return render_template("thanku.html",quiz="North America",score=score )




@app.route("/leaderboard")
def leaderboard():
    asia = db.execute ("SELECT users.username, asia.score FROM users INNER JOIN asia ON users.user_id = asia.user_id  ORDER BY asia.score DESC LIMIT 5")
    africa = db.execute ("SELECT users.username, africa.score FROM users INNER JOIN africa ON users.user_id = africa.user_id  ORDER BY africa.score DESC LIMIT 5")
    europe =db.execute ("SELECT users.username, europe.score FROM users INNER JOIN europe ON users.user_id = europe.user_id  ORDER BY europe.score DESC LIMIT 5")
    n_america = db.execute ("SELECT users.username, n_america.score FROM users INNER JOIN n_america ON users.user_id = n_america.user_id  ORDER BY n_america.score DESC LIMIT 5")
    s_america = db.execute ("SELECT users.username, s_america.score FROM users INNER JOIN s_america ON users.user_id = s_america.user_id  ORDER BY s_america.score DESC LIMIT 5")
    oceania = db.execute ("SELECT users.username, oceania.score FROM users INNER JOIN oceania ON users.user_id = oceania.user_id  ORDER BY oceania.score DESC LIMIT 5")

    return render_template("top.html",asia=asia,africa=africa,europe=europe,n_america=n_america,s_america=s_america,oceania=oceania)

@app.route("/scores")
@login_required
def scores():
    asia_s = db.execute("SELECT score FROM asia WHERE user_id = ?",session["user_id"])
    africa_s = db.execute("SELECT score FROM africa WHERE user_id = ?",session["user_id"])
    europe_s = db.execute("SELECT score FROM europe WHERE user_id = ?",session["user_id"])
    oceania_s = db.execute("SELECT score FROM oceania WHERE user_id = ?",session["user_id"])
    n_america_s = db.execute("SELECT score FROM n_america WHERE user_id = ?",session["user_id"])
    s_america_s = db.execute("SELECT score FROM s_america WHERE user_id = ?",session["user_id"])

    return render_template("scores.html",asia=asia_s[0]["score"],africa=africa_s[0]["score"],europe=europe_s[0]["score"],oceania=oceania_s[0]["score"],n_america=n_america_s[0]["score"],s_america=s_america_s[0]["score"])

def create_database_entry(user_id):
    db.execute("INSERT INTO asia (user_id, current_qn, score) VALUES (?, ?, ?)", user_id, 0 , 0)
    db.execute("INSERT INTO africa (user_id, current_qn, score) VALUES (?, ?, ?)", user_id, 0 , 0)
    db.execute("INSERT INTO europe (user_id, current_qn, score) VALUES (?, ?, ?)", user_id, 0 , 0)
    db.execute("INSERT INTO oceania (user_id, current_qn, score) VALUES (?, ?, ?)", user_id, 0 , 0)
    db.execute("INSERT INTO n_america (user_id, current_qn, score) VALUES (?, ?, ?)", user_id, 0 , 0)
    db.execute("INSERT INTO s_america (user_id, current_qn, score) VALUES (?, ?, ?)", user_id, 0 , 0)
    
