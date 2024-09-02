import argparse

import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output

from utils.dash_styling import create_paragraphs_from_list_of_comments, produce_dash_table_with_common_styling
from utils.data_preparation import DataPreparation
from utils.excel_parser import ExcelParser


def parse_args():
	parser = argparse.ArgumentParser(description="Launch Dash app to display contents \
																	of existing BFI weekend box office xls report.")
	parser.add_argument("xls_file", type=str, help="Path to the XLS file to display. \
										 The XLS file must be in the format of the BFI's existing weekly weekend box office reports.")
	return parser.parse_args()


def main():
	args = parse_args()
	excel_report_pathway = args.xls_file
	excel_parser = ExcelParser(excel_report_pathway)
	data_preparer = DataPreparation()
	top15_df = data_preparer.restore_original_formatting(excel_parser.top_15_df_with_notes_column)
	uk_films_in_top15_df = excel_parser.filter_for_UK_films(top15_df)
	new_releases_in_top15_df = excel_parser.filter_for_new_releases(top15_df)
	other_uk_films_df = data_preparer.restore_original_formatting(excel_parser.other_uk_films_df)
	all_uk_films_df = pd.concat([uk_films_in_top15_df, other_uk_films_df], ignore_index=True)
	other_new_releases_df = data_preparer.restore_original_formatting(excel_parser.other_new_releases_df)
	all_new_releases_df = pd.concat([new_releases_in_top15_df, other_new_releases_df], ignore_index=True)
	openers_next_week_df = excel_parser.openers_next_week_df
	total_weekend_gross_of_top_15 = data_preparer.format_gbp_currency(excel_parser.total_top_15_weekend_gross)
	total_gross_to_date_of_top_15 = data_preparer.format_gbp_currency(excel_parser.total_top_15_gross_to_date)

	app = Dash()

	app.layout = html.Div(children=[
			html.H1(children=excel_parser.report_heading),

			dcc.Dropdown(
					id="div-selector",
					options=[
							{"label": "Top 15 Highest Grossing Films", "value": "top-15"},
							{"label": "UK Films in the Top 15", "value": "uk-in-top-15"},
							{"label": "New Releases in the Top 15", "value": "new-releases-in-top-15"},
							{"label": "All UK Films", "value": "all-uk-films"},
							{"label": "All New Releases", "value": "all-new-releases"},
							{"label": "Openers Next Week", "value": "openers-next-week"}
					],
					value="top-15",
					clearable=False
			),

			html.Div(id="top-15", children=[
					html.H2("""
							Top 15 Highest-Grossing Films
					"""),

					dcc.Markdown("""
							*Note: 'Weekend Gross' figures will include Previews where applicable. See Notes column for more details.*
						"""
						),

					produce_dash_table_with_common_styling(top15_df),

					html.Div(id="revenue-totals", children=[
							html.P(f"Top 15 Total Weekend Gross: {total_weekend_gross_of_top_15}", style={"fontWeight": "bold"}),
							html.P(f"Total 15 Total Gross To Date: {total_gross_to_date_of_top_15}", style={"fontWeight": "bold"})
					], style={"marginTop": "20px"}
					),

					html.Div(id="comments", children=[
							html.H3("""
									Comments on this week's top 15 results
							"""),

							html.Div(create_paragraphs_from_list_of_comments(excel_parser.list_of_comments_on_top_15_result)),
					]),

			], style={"display": "block"}),

			html.Div(id="uk-in-top-15", children=[
					html.H2("""
							UK Films in the Top 15
					"""),
					produce_dash_table_with_common_styling(uk_films_in_top15_df)
			], style={"display": "none"}
			),

			html.Div(id="new-releases-in-top-15", children=[
					html.H2("""
							New Releases in the Top 15
					"""),
					produce_dash_table_with_common_styling(new_releases_in_top15_df)
			], style={"display": "none"}
			),

			html.Div(id="all-uk-films", children=[
					html.H2("""
							All UK Films
					"""),
					produce_dash_table_with_common_styling(all_uk_films_df)
			], style={"display": "none"}
			),

			html.Div(id="all-new-releases", children=[
					html.H2("""
							All New Releases
					"""),
					produce_dash_table_with_common_styling(all_new_releases_df)
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
			Output("all-uk-films", "style"),
			Output("all-new-releases", "style"),
			Output("openers-next-week", "style")],
			[Input("div-selector", "value")]
	)
	def toggle_dataset_visibility(selected_div) -> tuple:
		top15_style = {"display": "none"}
		ukintop15_style = {"display": "none"}
		newreleasesintop15_style = {"display": "none"}
		allukfilms_style = {"display": "none"}
		allnewreleases_style = {"display": "none"}
		openersnextweek_style = {"display": "none"}

		if selected_div == "top-15":
				top15_style = {"display": "block"}
		elif selected_div == "uk-in-top-15":
				ukintop15_style = {"display": "block"}
		elif selected_div == "new-releases-in-top-15":
				newreleasesintop15_style = {"display": "block"}
		elif selected_div == "all-uk-films":
				allukfilms_style = {"display": "block"}
		elif selected_div == "all-new-releases":
				allnewreleases_style = {"display": "block"}
		elif selected_div == "openers-next-week":
				openersnextweek_style = {"display": "block"}

		return top15_style, ukintop15_style, newreleasesintop15_style, allukfilms_style, \
							allnewreleases_style, openersnextweek_style

	app.run_server(debug=True)


if __name__ == "__main__":
    main()