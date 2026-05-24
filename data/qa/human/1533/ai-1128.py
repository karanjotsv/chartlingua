import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_path = os.path.splitext(json_path)[0] + '.png'

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors, line=dict(width=0)),
    texttemplate='%{x}%',
    textposition='outside',
    cliponaxis=False,
    hoverinfo='none'
))

fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b><br><span style='font-size: 16px;'>{texts['subtitle']}</span>",
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=24)
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        ticksuffix='%',
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.1] 
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(size=14)
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.25,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=10)
        )
    ],
    font=dict(
        family="Arial",
        color="#333333"
    ),
    plot_bgcolor='#f0f0f0',
    paper_bgcolor='#f0f0f0',
    showlegend=False,
    margin=dict(l=100, r=80, t=120, b=200)
)

fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")