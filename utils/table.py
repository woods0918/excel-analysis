import dash_table

def plot(data, id_name):
    cols = data.columns.tolist()
    style_cell_conditional = []
    for col in cols:
        style_cell_conditional.append(
            {
                "if": {"column_id": col},
                "width": "5%"
            }
        )

    return [
        dash_table.DataTable(
            id=id_name,
            columns=[
                {"name": i, "id": i, "deletable": False} for i in cols
            ],
            data=data.to_dict('records'),
            editable=True,
            sort_action="native",
            sort_mode = "multi",
            row_selectable="single",
            row_deletable=False,
            selected_rows=[],
            style_header={"font-size":"16px","background-color":"#4CAF50","color":"#FFFFFF"},
            style_as_list_view=True,
            style_table={'overflowX': 'scroll'},
            style_cell={
                'minWidth': '0px', 
                'maxWidth': '100px',
                'whiteSpace': 'normal',
                'textAlign': 'left',
                'padding': '5px',
                'font-size' : '14px'
            },
            # style_cell_conditional=style_cell_conditional,
            css=[{
                'selector': '.dash-cell div.dash-cell-value',
                'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit; font-size: 14px;'
            }],
            page_action="native",
            page_current= 0,
            page_size= 10
        )
    ]