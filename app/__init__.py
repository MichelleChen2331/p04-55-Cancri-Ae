from flask import Flask, render_template
from flask import session, request, redirect, url_for
import plotly.graph_objects as go
import plotly.utils #plotly helper
import json
from .data import load_planets
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "676767676helpaaaaaamogusrahhhh"

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home', methods=["GET", "POST"])
def home():
    logged_in = "You aren't logged in but"
    logged_in_bool = False
    if "user" in session:
        logged_in = session["user"]
        logged_in_bool = True
    return render_template("home.html",logged_in=logged_in)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()

        if result and check_password_hash(result[0], password):
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", invalid="Invalid username or password")

    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", invalid="Username already exists")

        conn.close()

        session["user"] = username
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/definitions", methods=["GET", "POST"])
def definitions():
    return render_template("definitions.html")

@app.route("/data1", methods=["GET", "POST"])
def data1():
    chart_json = build_chart()
    return render_template("data1.html", chart_json=chart_json)

@app.route("/data2", methods=["GET", "POST"])
def data2():
    pie_chart_json = pie_discov_method()
    return render_template("data2.html",
                            pie_chart_json=pie_chart_json)

@app.route("/data3", methods=['GET', 'POST'])
def data3():
    radii_chart_json = build_density_chart()
    return render_template("data3.html", density_chart_json = radii_chart_json)

@app.route("/explore", methods=["GET", "POST"])
def explore():
    df = load_planets()
    return render_template("Explore.html", data=df.to_json(orient="records"))

@app.route("/planets", methods=["GET", "POST"])
def planets():
    df = load_planets()
    return render_template("Planets.html", data=df.to_json(orient="records"))

def build_density_chart():
    df = load_planets()
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=df["pl_rade"],
        nbinsx=30,
        marker_color="rgba(100,150,200,0.7)",
        hovertemplate = (
            "<b>Radius: %{x} Earth Radii</b><br>"
            "Count: %{y}<br>"
            "<extra></extra>"
        )
    ))

    fig.update_layout(
        title = "Distribution of Exoplanet Radii",
        xaxis = dict(title="Radius (Earth Radii)", color="black",
                     gridcolor = "rgba(255,255,255,0.1)"),
        yaxis = dict(title="Count", color="black",
                     gridcolor = "rgba(255,255,255,0.1)"),
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(20,20,30,0.8)",
        font = dict(color="black"),
        margin = dict(l=60, r=40, t=60, b=60),
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

#Bar Chart of discovery year
def build_chart():
    df = load_planets()

    yearly = df.groupby("disc_year").size().reset_index(name="count")
    fig = go.Figure()


    fig.add_trace(go.Bar(
        x = yearly["disc_year"],
        y = yearly["count"],
        marker=dict(
            color = yearly["count"],
            colorscale = "Viridis",
            showscale = True,
            colorbar = dict(title="# Planets")
        ),
        hovertemplate = (
            "<b>Year: %{x}</b><br>"
            "Planets discovered: %{y}<br>"
            "<extra></extra>"
        )
    ))

    fig.update_layout(
        title = "Exoplanet Discoveries Per Year",
        xaxis = dict(title="Year", color="black",
                     gridcolor = "rgba(255,255,255,0.1)"),
        yaxis = dict(title="Number of Planets", color="black",
                     gridcolor = "rgba(255,255,255,0.1)"),
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(20,20,30,0.8)",
        font = dict(color="black"),
        margin = dict(l=60, r=40, t=60, b=60),
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

#Pie Chart of Discovery
def pie_discov_method():
    df = load_planets()
    methods = df.groupby("discoverymethod").size().reset_index(name="count")

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=methods["discoverymethod"],
        values=methods["count"],
        textinfo="label+percent",
        hovertemplate = (
        "<b>%{label}</b><br>"
        "Planets: %{value}<br>"
    )))

    fig.update_layout(
        title = "Exoplanets Sorted By Discovery Method",
        paper_bgcolor= "rgba(0,0,0,0)",
        font = dict(color="black"),
        margin = dict(l=50, r=50, t=20, b=20),
        legend=dict(
            font=dict(color="white", size=12),
            bgcolor="rgba(30,30,40,0.8)",
            bordercolor= "black",
            borderwidth=1
        )
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)



if __name__ == '__main__':
    app.debug = False
    app.run()
