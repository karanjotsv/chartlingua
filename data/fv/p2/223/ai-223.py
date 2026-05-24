import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_path = json_path.with_suffix('.png')

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
series_names = config['series_names']

fig = go.Figure()

categories = [item['category'] for item in chart_data]
num_series = len(series_names)

for i in range(num_series):
    values = [item['values'][i] for item in chart_data]
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        name=series_names[i],
        marker_color=colors[i]
    ))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        tickformat='.0%',
        showgrid=True,
        gridcolor='#dddddd',
        zeroline=False,
        showline=False,
        range=[0, 0.255],
        dtick=0.05
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=50, r=50, t=80, b=100)
)

fig.write_image(output_path, scale=2, width=800, height=500)

print(f"Chart saved to {output_path}")