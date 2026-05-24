import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

base_filename = json_file_path.stem

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    texttemplate='%{text:,}',
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False
))

title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle', '')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

source_text = texts.get('source', '')

fig.update_layout(
    title={
        'text': full_title,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'showgrid': False,
        'linecolor': '#BCC0C4',
        'ticks': 'outside'
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'range': [0, 15000],
        'dtick': 2500,
        'showgrid': True,
        'gridcolor': '#EAEAEA',
        'separatethousands': True
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    font={'family': 'Arial', 'size': 12, 'color': '#333333'},
    showlegend=False,
    margin={'t': 60, 'b': 100, 'l': 80, 'r': 40},
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ]
)

output_file = f"{base_filename}.png"
fig.write_image(output_file, scale=2)
print(f"Chart saved to {output_file}")