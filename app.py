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
openers_next_week_df = excel_parser.openers_next_week_df

def produce_dash_table_with_common_styling(df):
	return dash_table.DataTable(
		data=df.to_dict("records"),
		columns=[{"name": col, "id": col} for col in df.columns],
		style_table={
			"height": "70vh",
			"overflowY": "auto",
			"width": "100%",
			"minWidth": "100%"},
		style_header={
			"whiteSpace": "normal",
			"textAlign": "center",
		},
		style_cell={
			"minWidth": "50px",
			"width": "auto",
			"maxWidth": "200px",
			"whiteSpace": "normal",
			"paddingLeft": "8px",
			"paddingRight": "8px"
		},
		style_cell_conditional=[
			{"if": {"column_id": "% change on last week"}, "width": "80px"},
			{"if": {"column_id": "Weeks on release"}, "width": "80px"},
			{"if": {"column_id": "Number of cinemas"}, "width": "80px"},
			{"if": {"column_id": "Film"}, "textAlign": "left"},
			{"if": {"column_id": "Distributor"}, "textAlign": "left"},
			{"if": {"column_id": "Country of Origin"}, "textAlign": "left"},
		],
		style_header_conditional=[
			{"if": {"column_id": "Film"}, "textAlign": "left"},
			{"if": {"column_id": "Distributor"}, "textAlign": "left"},
			{"if": {"column_id": "Country of Origin"}, "textAlign": "left"}
		],
		fixed_rows={"headers": True},
	)

app.layout = html.Div(children=[
    html.H1(children=excel_parser.report_heading),

    dcc.Dropdown(
        id="div-selector",
        options=[
            {"label": "Top 15 Highest Grossing Films", "value": "top-15"},
            {"label": "UK Films in the Top 15", "value": "uk-in-top-15"},
            {"label": "New Releases in the Top 15", "value": "new-releases-in-top-15"},
            {"label": "Other UK Films", "value": "other-uk-films"},
            {"label": "Other New Releases", "value": "other-new-releases"},
						{"label": "Openers Next Week", "value": "openers-next-week"}
        ],
        value="top-15",
        clearable=False
    ),

    html.Div(id="top-15", children=[
        html.H2("""
            Top 15 Highest-Grossing Films
        """),
        produce_dash_table_with_common_styling(top15_reformatted_df),

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
        produce_dash_table_with_common_styling(UK_films_in_top15_df)
    ], style={"display": "none"}
    ),

    html.Div(id="new-releases-in-top-15", children=[
        html.H2("""
            New Releases in the Top 15
        """),
        produce_dash_table_with_common_styling(new_releases_in_top15_df)
    ], style={"display": "none"}
    ),

		html.Div(id="other-uk-films", children=[
        html.H2("""
            Other UK Films
        """),
        produce_dash_table_with_common_styling(other_uk_films_reformatted_df)
    ], style={"display": "none"}
    ),

		html.Div(id="other-new-releases", children=[
        html.H2("""
            Other New Releases
        """),
        produce_dash_table_with_common_styling(other_new_releases_reformatted_df)
    ], style={"display": "none"}
    ),

		html.Div(id="openers-next-week", children=[
        html.H2("""
            Openers Next Week
        """),
        dash_table.DataTable(data=openers_next_week_df.to_dict('records'),
														 style_table={
															 "width": "auto",
															 "minWidth": "50%",
															 "maxWidth": "75%",
														},
														style_header={
															"whitespace": "nowrap",
															"textAlign": "left"
														},
														style_cell={
														"minWidth": "50px",
														"width": "auto",
														"maxWidth": "200px",
														"whiteSpace": "normal",
														"paddingLeft": "8px",
														"paddingRight": "8px"
														},
														style_data={
															"textAlign": "left"
														},
														fixed_rows={"headers": True},)
    ], style={"width": "100%", "display": "none"}
    )
])

@app.callback(
    [Output("top-15", "style"),
     Output("uk-in-top-15", "style"),
     Output("new-releases-in-top-15", "style"),
     Output("other-uk-films", "style"),
		 Output("other-new-releases", "style"),
		 Output("openers-next-week", "style")],
     [Input("div-selector", "value")]
)
def toggle_dataset_visibility(selected_div) -> tuple:
	top15_style = {"display": "none"}
	ukintop15_style = {"display": "none"}
	newreleasesintop15_style = {"display": "none"}
	otherukfilms_style = {"display": "none"}
	othernewreleases_style = {"display": "none"}
	openersnextweek_style = {"display": "none"}

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
	elif selected_div == "openers-next-week":
			openersnextweek_style = {"display": "block"}

	return top15_style, ukintop15_style, newreleasesintop15_style, otherukfilms_style, othernewreleases_style, openersnextweek_style

if __name__ == "__main__":
    app.run(debug=True)