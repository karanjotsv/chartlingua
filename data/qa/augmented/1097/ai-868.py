import sys
import os
import json
import plotly.graph_objects as go

if len(sys.argv) < 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data['series']):
    fig.add_trace(go.Bar(
        x=data['categories'],
        y=series['data'],
        name=texts['legend_labels'][i],
        marker_color=colors[i],
        text=series['data'],
        texttemplate='%{text}',
        textposition='inside',
        textfont=dict(color='white', family='Arial', size=12),
        insidetextanchor='middle'
    ))

fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        title=texts['x_axis_title'],
        type='category',
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 40],
        gridcolor='#e0e0e0',
        zeroline=False,
        linecolor='black'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.3,
            xanchor='left', yanchor='bottom',
            text=f"ⓘ {texts['additional_info']}",
            showarrow=False,
            font=dict(family="Arial", color="#267fca")
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.3,
            xanchor='right', yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", color="#8c8c8c")
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")