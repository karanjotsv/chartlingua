import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
base_filename = Path(json_file_path).stem

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

fig = go.Figure()

categories = chart_data['chart_data']['categories']
series_data = chart_data['chart_data']['series']
colors = chart_data['colors']
texts = chart_data['texts']

for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=series['data'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            color='white',
            size=12
        ),
        hoverinfo='skip'
    ))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickfont=dict(size=12),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 301],
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=80, r=40, t=50, b=150),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.35,
            xanchor='right',
            yanchor='top',
            text=texts.get('source'),
            showarrow=False,
            font=dict(
                family="Arial",
                size=12,
                color="grey"
            )
        )
    ]
)

output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")