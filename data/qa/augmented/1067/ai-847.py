import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
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

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    texttemplate='%{y}%',
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=14,
        color='black',
        weight='bold'
    ),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_title'),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_title'),
        range=[0, 41],
        tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40],
        ticksuffix='%',
        gridcolor='#e0e0e0',
        zeroline=False,
        title_standoff=10
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")