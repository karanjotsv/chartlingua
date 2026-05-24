import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_file_path} is not a valid JSON file.")
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
    text=values,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"{texts.get('title', '')}<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    yaxis=dict(
        range=[0, 50],
        tickmode='linear',
        dtick=10,
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        zeroline=False
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#f5f5f5',
        gridwidth=1
    ),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=60, b=100),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('source'),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#666666')
        )
    ]
)

base_filename = os.path.splitext(json_file_path)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")