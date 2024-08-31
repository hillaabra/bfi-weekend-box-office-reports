from dash import Dash, dash_table, html
from utils import Top15


app = Dash()

excel_report_pathway = "bfi-weekend-box-office-report-2024-08-16-18.xls" # decide how to handle this when automating
top15 = Top15(excel_report_pathway)
top15_df = top15.read_table_to_df()
top15_reformatted_df = top15.restore_original_formatting(top15_df)

app.layout = html.Div(children=[
	html.H1(children=top15.report_heading),

	html.Div(id="top15", children=[
        	html.H2("""
            		Top 15 Highest-Grossing Films
        	"""),
        	dash_table.DataTable(data=top15_reformatted_df.to_dict('records'), page_size=15)
    	])
])

if __name__ == "__main__":
  app.run_server(debug=True)