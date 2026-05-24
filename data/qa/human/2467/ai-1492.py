import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = Path(json_path_str)

if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
categories = chart_info['categories']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(color='white', width=1)
        ),
        text=[f'{v}%' for v in series['values']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=14,
            color=series['text_color']
        )
    ))

fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=270, r=40, t=50, b=120),
    xaxis=dict(
        title=texts['x_axis_title'],
        title_font=dict(size=14),
        range=[0, 120],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=13)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        traceorder="normal"
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    ]
)

output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2, width=1000, height=600)

print(f"Chart saved to {output_path}")