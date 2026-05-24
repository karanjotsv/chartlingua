import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

formatted_text = []
for v in values:
    if v == int(v):
        formatted_text.append(f'{int(v):,}'.replace(',', ' '))
    else:
        formatted_text.append(f'{v:,.1f}'.replace(',', ' '))

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=formatted_text,
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='black'),
    cliponaxis=False,
    hoverinfo='none'
))

y_axis_range = [0, 70000]
y_axis_tickvals = list(range(0, 70001, 10000))
y_axis_ticktext = [f'{val:,}'.replace(',', ' ') for val in y_axis_tickvals]

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12)
        )
    )

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=y_axis_range,
        tickvals=y_axis_tickvals,
        ticktext=y_axis_ticktext,
        gridcolor='#E5E5E5',
        zerolinecolor='#444444',
        zerolinewidth=1,
        tickfont=dict(size=12)
    ),
    margin=dict(l=100, r=40, t=40, b=120),
    annotations=annotations
)

output_filename = json_file_path.with_suffix(".png")
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")