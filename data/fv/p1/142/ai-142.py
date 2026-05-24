import sys
import json
import os
import plotly.graph_objects as go

# Load data from the JSON file provided as a command-line argument
json_file_path = sys.argv[1]
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
labels = [item['label'] for item in chart_data['chart_data']]
values = [item['value'] for item in chart_data['chart_data']]
colors = chart_data['colors']
texts = chart_data['texts']

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    sort=False,
    direction='clockwise',
    textposition='outside',
    textinfo='label',
    outsidetextfont=dict(family="Arial", size=14, color='black'),
    showlegend=False
)])

# Build the title string from JSON data
title_text = ""
if texts.get("title"):
    title_text += f'<span style="font-size: 20px;"><b>{texts["title"]}</b></span>'
if texts.get("subtitle"):
    title_text += f'<br><span style="font-size: 16px;">{texts["subtitle"]}</span>'

# Update the figure layout
fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    font_family="Arial",
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=100, r=100, t=60, b=60),
    width=800,
    height=600
)

# Determine the output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)