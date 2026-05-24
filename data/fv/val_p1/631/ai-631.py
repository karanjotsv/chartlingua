import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit("Usage: python <script_name>.py <json_file_path>")

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

values = [d['value'] for d in chart_data]
categories = [d['category'] for d in chart_data]
data_labels = texts['data_labels']

fig = go.Figure(data=[go.Pie(
    labels=categories,
    values=values,
    text=data_labels,
    textinfo='text',
    hoverinfo='none',
    marker=dict(
        colors=colors,
        line=dict(color='black', width=3)
    ),
    sort=False,
    direction='clockwise',
    rotation=90,
    textposition=['inside', 'outside', 'outside', 'outside', 'outside', 'inside'],
    insidetextfont=dict(family="Arial", size=16, color='white'),
    outsidetextfont=dict(family="Arial", size=14, color='black')
)])

fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_font=dict(family="Arial", size=28),
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(t=120, b=40, l=40, r=40),
    paper_bgcolor='white'
)

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_file = f"{base_name}.png"

fig.write_image(output_file, scale=2)