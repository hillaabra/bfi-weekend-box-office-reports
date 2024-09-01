from dash import Dash, dash_table, dcc, html, Input, Output
from utils import DataPreparation
from excel_parser import ExcelParser


app = Dash()

excel_report_pathway = "bfi-weekend-box-office-report-2024-08-16-18.xls" # decide how to handle this when automating
excel_parser = ExcelParser(excel_report_pathway)
data_preparer = DataPreparation()
top15_df = excel_parser.top_15_df
top15_reformatted_df = data_preparer.restore_original_formatting(top15_df)
UK_films_in_top15_df = excel_parser.filter_for_UK_films(top15_reformatted_df)
new_releases_in_top15_df = excel_parser.filter_for_new_releases(top15_reformatted_df)
other_uk_films_df = excel_parser.other_uk_films_df
other_uk_films_reformatted_df = data_preparer.restore_original_formatting(other_uk_films_df)
other_new_releases_df = excel_parser.other_new_releases_df
other_new_releases_reformatted_df = data_preparer.restore_original_formatting(other_new_releases_df)

app.layout = html.Div(children=[
    html.H1(children=excel_parser.report_heading),

    dcc.Dropdown(
        id="div-selector",
        options=[
            {"label": "Top 15 Highest Grossing Films", "value": "top-15"},
            {"label": "UK Films in the Top 15", "value": "uk-in-top-15"},
            {"label": "New Releases in the Top 15", "value": "new-releases-in-top-15"},
            {"label": "Other UK Films", "value": "other-uk-films"},
            {"label": "Other New Releases", "value": "other-new-releases"}
        ],
        value="top-15",
        clearable=False
    ),

    html.Div(id="top-15", children=[
        html.H2("""
            Top 15 Highest-Grossing Films
        """),
        dash_table.DataTable(data=top15_reformatted_df.to_dict("records"), page_size=15),

				html.Div(id="comments", children=[
						html.H3("""
								Comments
						"""),

						html.P("""
							'Weekend gross' figures include Previews. Comments below for more detail.
						""")
		])
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
    ),

		html.Div(id="other-uk-films", children=[
        html.H2("""
            Other UK Films
        """),
        dash_table.DataTable(data=other_uk_films_reformatted_df.to_dict('records'))
    ], style={"display": "none"}
    ),

		html.Div(id="other-new-releases", children=[
        html.H2("""
            Other New Releases
        """),
        dash_table.DataTable(data=other_new_releases_reformatted_df.to_dict('records'))
    ], style={"display": "none"}
    )
])

@app.callback(
    [Output("top-15", "style"),
     Output("uk-in-top-15", "style"),
     Output("new-releases-in-top-15", "style"),
     Output("other-uk-films", "style"),
			Output("other-new-releases", "style")],
     [Input("div-selector", "value")]
)
def toggle_dataset_visibility(selected_div) -> tuple:
	top15_style = {"display": "none"}
	ukintop15_style = {"display": "none"}
	newreleasesintop15_style = {"display": "none"}
	otherukfilms_style = {"display": "none"}
	othernewreleases_style = {"display": "none"}

	if selected_div == "top-15":
			top15_style = {"display": "block"}
	elif selected_div == "uk-in-top-15":
			ukintop15_style = {"display": "block"}
	elif selected_div == "new-releases-in-top-15":
			newreleasesintop15_style = {"display": "block"}
	elif selected_div == "other-uk-films":
			otherukfilms_style = {"display": "block"}
	elif selected_div == "other-new-releases":
			othernewreleases_style = {"display": "block"}

	return top15_style, ukintop15_style, newreleasesintop15_style, otherukfilms_style, othernewreleases_style

if __name__ == "__main__":
    app.run(debug=True)