import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

fig.add_trace(go.Bar(
    x=[d['category'] for d in data],
    y=[d['value'] for d in data],
    text=[d['label'] for d in data],
    textposition='outside',
    marker_color=colors[0],
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color='#444444'),
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 80],
        ticksuffix='%',
        gridcolor='#EAEAEA',
        showline=False
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    showlegend=False,
    annotations=[
        dict(
            text=texts['source_left'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.18,
            xanchor='left',
            yanchor='bottom',
            font=dict(family="Arial", size=11, color='#0073B0')
        ),
        dict(
            text=texts['source_right'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.18,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=11, color='#555555')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")