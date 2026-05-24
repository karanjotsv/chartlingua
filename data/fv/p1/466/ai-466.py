import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit("Usage: python <script_name>.py <json_file_path>")

json_path = sys.argv[1]
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
colors = config['colors']

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
display_texts = [item['display_text'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=display_texts,
    marker_colors=colors,
    textinfo='text',
    sort=False,
    direction='clockwise',
    rotation=160,
    textfont=dict(
        family="Arial",
        size=16,
        color='white'
    ),
    hoverinfo='none',
    insidetextorientation='radial'
))

fig.update_layout(
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial"),
    margin=dict(l=20, r=20, t=20, b=20),
    width=800,
    height=481
)

fig.write_image(output_filename, scale=2)