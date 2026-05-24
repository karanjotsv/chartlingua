import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

fig = go.Figure()

data = chart_info['chart_data']
colors = chart_info['colors']
texts = chart_info['texts']
categories = data[0]['y']

for i, series in enumerate(data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(color='rgba(0,0,0,0.5)', width=1)
        )
    ))

title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

fig.update_layout(
    barmode='relative',
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title=dict(
            text=texts['x_axis_title'],
            standoff=10
        ),
        range=[-7, 28],
        tickvals=[-5, 0, 5, 10, 15, 20, 25],
        showgrid=True,
        gridcolor='darkgrey',
        gridwidth=0.5,
        griddash='dash',
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        categoryorder='array',
        categoryarray=categories
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    font=dict(family="Arial"),
    plot_bgcolor='#f2efe4',
    paper_bgcolor='white',
    margin=dict(l=150, r=30, t=80, b=80)
)

output_filename = json_path.with_suffix(".png").name
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")