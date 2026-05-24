import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i % len(colors)]
    ))

title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><i>{texts['subtitle']}</i>"

source_text_parts = []
if texts.get('source'):
    source_text_parts.append(texts['source'])
if texts.get('note'):
    source_text_parts.append(texts['note'])
source_text = "<br>".join(source_text_parts)

annotations = []
if source_text:
    annotations.append(
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.2,
            xanchor='center',
            yanchor='top',
            align='center'
        )
    )

fig.update_layout(
    title={
        'text': title_text,
        'x': 0.05,
        'xanchor': 'left',
        'y': 0.95,
        'yanchor': 'top'
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'showgrid': False,
        'showline': False,
        'ticks': '',
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'range': [0, 4.1],
        'tickvals': [0, 1, 2, 3, 4],
        'showgrid': True,
        'gridcolor': '#e0e0e0',
        'zeroline': False,
        'showline': False,
    },
    legend={
        'traceorder': 'normal',
        'x': 0.99,
        'y': 0.99,
        'xanchor': 'right',
        'yanchor': 'top',
    },
    font={'family': "Arial", 'size': 12},
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin={'l': 50, 'r': 50, 't': 80, 'b': 80},
    annotations=annotations
)

base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")