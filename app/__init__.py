from flask import Flask, render_template
from flask import session, request, redirect
import plotly.graph_objects as go
import plotly.utils #plotly helper
import json
from .data import load_planets, fetch_and_store


app = Flask(__name__)


@app.route('/home', methods=["GET", "POST"])
def home():
    chart_json = build_chart()
    return render_template("home.html",
                            chart_json=chart_json)

@app.route("/definitions", methods=["GET", "POST"])
def definitions():
    return render_template("defintions.html")

@app.route("/data1", methods=["GET", "POST"])
def data1():
    return render_template("data1.html")

@app.route("/data2", methods=["GET", "POST"])
def data2():
    return render_template("data2.html")

def build_chart():
    fetch_and_store()
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


if __name__ == '__main__':
    app.debug = True
    app.run()
