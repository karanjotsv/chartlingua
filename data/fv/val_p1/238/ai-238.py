import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.6,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=3)
    ),
    textinfo='percent',
    textfont=dict(color='white', size=16, family="Arial"),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=85
))

fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_y=0.95,
    title_font=dict(family="Arial", size=16),
    font=dict(family="Arial", size=12),
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.15,
        xanchor='center',
        x=0.5
    ),
    margin=dict(t=140, b=100, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    shapes=[
        dict(
            type="rect",
            xref="paper",
            yref="paper",
            x0=0.01,
            y0=0.01,
            x1=0.99,
            y1=0.99,
            line=dict(
                color="grey",
                width=1
            )
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")