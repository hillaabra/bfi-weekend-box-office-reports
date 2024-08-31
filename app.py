from dash import Dash, dash_table, dcc, html, Input, Output
from utils import Top15


app = Dash()

excel_report_pathway = "bfi-weekend-box-office-report-2024-08-16-18.xls" # decide how to handle this when automating
top15 = Top15(excel_report_pathway)
top15_df = top15.read_table_to_df()
top15_reformatted_df = top15.restore_original_formatting(top15_df)
UK_films_in_top15_df = top15.filter_for_UK_films(top15_reformatted_df)
new_releases_in_top15_df = top15.filter_for_new_releases(top15_reformatted_df)

app.layout = html.Div(children=[
    html.H1(children=top15.report_heading),

    dcc.Dropdown(
        id="div-selector",
        options=[
            {"label": "Top 15 Highest Grossing Films", "value": "top-15"},
            {"label": "UK Films in the Top 15", "value": "uk-in-top-15"},
            {"label": "New Releases in the Top 15", "value": "new-releases-in-top-15"}
        ],
        value="top-15",
        clearable=False
    ),

    html.Div(id="top-15", children=[
        html.H2("""
            Top 15 Highest-Grossing Films
        """),
        dash_table.DataTable(data=top15_reformatted_df.to_dict("records"), page_size=15)
    ], style={"display": "block"}),

    html.Div(id="uk-in-top-15", children=[
        html.H2("""
            UK Films in the Top 15
        """),
        dash_table.DataTable(data=UK_films_in_top15_df.to_dict("records"), page_size=15)
    ], style={"display": "none"}
    ),

    html.Div(id="new-releases-in-top-15", children=[
        html.H2("""
            New Releases in the Top 15
        """),
        dash_table.DataTable(data=new_releases_in_top15_df.to_dict('records'), page_size=15)
    ], style={"display": "none"}
    )
])

@app.callback(
    [Output("top-15", "style"),
     Output("uk-in-top-15", "style"),
     Output("new-releases-in-top-15", "style")],
     [Input("div-selector", "value")]
)
def toggle_dataset_visibility(selected_div) -> tuple:
    top15_style = {"display": "none"}
    ukintop15_style = {"display": "none"}
    newreleasesintop15_style = {"display": "none"}

    if selected_div == "top-15":
        top15_style = {"display": "block"}
    elif selected_div == "uk-in-top-15":
        ukintop15_style = {"display": "block"}
    elif selected_div == "new-releases-in-top-15":
        newreleasesintop15_style = {"display": "block"}

    return top15_style, ukintop15_style, newreleasesintop15_style

if __name__ == "__main__":
    app.run(debug=True)