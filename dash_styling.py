from dash import dash_table


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