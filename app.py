# importing libraries
import dash 
from dash import dcc # contains Dash Core components to create elements such as graphs, dropdowns, sliders
from dash import html # contains Dash HTML components to create and style HTML content
import plotly.express as px # used for creating graphs
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv("./life_expectancy.csv")

colors = {"background": "#011833", "text": "#7FDBFF"}
# to describe layout of dashboard
app.layout = html.Div(
    [
        html.H1(
            "Life Expectancy Dashboard - Manmeet Singh Chhabra", # Main Heading
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Developing Status of the Country"),
                        dcc.Dropdown(
                            id="status-dropdown",
                            options=[
                                {"label": s, "value": s} for s in df.Status.unique()  # Development Status Dropdown 
                            ],
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Label("Average schooling years grater than"), #Average schooling years grater than Dropdown
                        dcc.Dropdown(
                            id="schooling-dropdown",
                            options=[
                                {"label": y, "value": y}
                                for y in range(
                                    int(df.Schooling.min()), int(df.Schooling.max()) + 1
                                )
                            ],
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="row",
        ),
        html.Div(dcc.Graph(id="life-exp-vs-gdp"), className="chart"),
        dcc.Slider(
            "year-slider",
            min=df.Year.min(),
            max=df.Year.max(),
            step=None,
            marks={year: str(year) for year in range(df.Year.min(), df.Year.max() + 1)}, # Years Slider
            value=df.Year.min(),
        ),
    ],
    className="container",
)

# Here Callback function is automatically called by Dash whenever there is change in input component and output component is updated accordingly
@app.callback(
    Output("life-exp-vs-gdp", "figure"),
    Input("year-slider", "value"),
    Input("status-dropdown", "value"),
    Input("schooling-dropdown", "value"),
)
# Function for plotting Life expectancy vs Gdp per capita graph
def update_figure(selected_year, country_status, schooling):
    filtered_dataset = df[(df.Year == selected_year)]

    if schooling:
        filtered_dataset = filtered_dataset[filtered_dataset.Schooling <= schooling]

    if country_status:
        filtered_dataset = filtered_dataset[filtered_dataset.Status == country_status]

    fig = px.scatter(
        filtered_dataset,
        x="GDP",
        y="Life expectancy",
        size="Population",
        color="continent",
        hover_name="Country",
        log_x=True,
        size_max=60,
    )
    # Function for updating Graph text and Background colour
    fig.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )

    return fig


# Creating Server to run the dashboard
if __name__ == "__main__":
    app.run_server(debug=True)
