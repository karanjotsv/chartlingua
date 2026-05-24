import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors['bars'][0],
    text=[f"{v:.2f}%" for v in values],
    textposition='outside',
    cliponaxis=False,
    hoverinfo='none',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='#f5f5f5',
    showlegend=False,
    margin=dict(l=90, r=20, t=30, b=100),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showline=True,
        linecolor='lightgray',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 2.3],
        tickmode='array',
        tickvals=[0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.20,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=10, color='#666666')
        )
    ]
)

base_path = os.path.splitext(json_path)[0]
output_filename = f"{base_path}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")