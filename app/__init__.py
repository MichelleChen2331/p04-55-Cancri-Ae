from flask import Flask, render_template
from flask import session, request, redirect, url_for
import plotly.graph_objects as go
import plotly.utils #plotly helper
import json
from data import load_planets, fetch_and_store


app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home', methods=["GET", "POST"])
def home():
    chart_json = build_chart()
    pie_chart_json = pie_discov_method()
    return render_template("home.html",
                            chart_json=chart_json
                            pie_chart_json=pie_chart_json)

@app.route("/definitions", methods=["GET", "POST"])
def definitions():
    return render_template("definitions.html")

@app.route("/data1", methods=["GET", "POST"])
def data1():
    return render_template("data1.html")

@app.route("/data2", methods=["GET", "POST"])
def data2():
    return render_template("data2.html")

@app.route("/explore", methods=["GET", "POST"])
def explore():
    return render_template("Explore.html")

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
        xaxis = dict(title="Year", color="white",
                     gridcolor = "rgba(255,255,255,0.1)"),
        yaxis = dict(title="Number of Planets", color="white",
                     gridcolor = "rgba(255,255,255,0.1)"),
        paper_bgcolor = "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(20,20,30,0.8)",
        font = dict(color="white"),
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
        font = dict(color="white"),
        margin = dict(l=50, r=50, t=20, b=20),
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)



if __name__ == '__main__':
    fetch_and_store()
    app.debug = True
    app.run()
