import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
background_color = chart_info.get('background_color', '#FFFFFF')

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    textinfo='percent',
    texttemplate='%{value:.1f}%',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=125,
    textfont=dict(size=14)
))

fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_y=0.95,
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    margin=dict(t=100, b=100, l=40, r=40),
    showlegend=True
)

base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")