import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f'{v:,}'.replace(',', ' ') for v in values],
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
))

fig.update_traces(
    textfont_weight="bold",
    cliponaxis=False 
)

fig.update_layout(
    font=dict(family="Arial"),
    yaxis_title=texts['y_axis_title'],
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        range=[0, 120000],
        tickformat=" ",
        showgrid=True,
        gridcolor='#e5e5e5',
        zeroline=False,
        ticks="outside",
        tickcolor='lightgrey',
        title_standoff=10
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        ticks="outside",
        tickcolor='lightgrey'
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.2,
            xanchor='left', yanchor='top',
            text=f"<b>{texts['source_left']}</b>",
            showarrow=False,
            font=dict(size=12, color='#0073e5')
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts['source_right'].replace("Show source", "<span style='color:#0073e5'>Show source</span>"),
            align='right',
            showarrow=False,
            font=dict(size=12, color='#666666')
        )
    ]
)

output_path = json_file_path.with_suffix('.png')
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")