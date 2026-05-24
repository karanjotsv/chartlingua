import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script.py> <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

fig = go.Figure()

x_values = [d['x'] for d in data]
y_values = [d['y'] for d in data]

fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines',
    line=dict(color=colors[0], width=2),
    showlegend=False
))

title_parts = []
if texts.get('title'):
    title_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_parts.append(f"<span style='font-size:0.8em;'>{texts['subtitle']}</span>")
full_title = "<br>".join(title_parts)

fig.update_layout(
    title=dict(
        text=full_title,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickvals=[1968, 1973, 1978, 1983, 1988, 1993, 1998, 2003, 2008],
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 900],
        tickvals=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900],
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=60, r=40, t=80, b=80),
    autosize=False,
    width=600,
    height=500
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")