import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(
            color=colors[i],
            dash=series.get('line_style', 'solid'),
            width=2 if series.get('line_style') != 'dash' else 2.5
        )
    ))

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        font=dict(size=22)
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        title_font=dict(size=18),
        range=[0, 1000],
        tickmode='linear',
        dtick=100,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 140],
        tickmode='linear',
        dtick=20,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=60, r=40, t=80, b=80),
    width=800,
    height=600
)

fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")