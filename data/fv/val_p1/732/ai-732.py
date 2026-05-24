import sys
import json
import os
import plotly.graph_objects as go

# Load data from the JSON file provided as a command-line argument
json_file_path = sys.argv[1]
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# To create the vertical split seen in the image, we rotate the pie.
# The boundary is at the top (90 degrees). The first slice (Acid2 compliant, 45.3%)
# must end at this boundary. Its angular size is 45.3 * 3.6 = 163.08 degrees.
# Therefore, it must start at 90 - 163.08 = -73.08 degrees.
rotation_angle = 90 - (values[0] * 3.6)

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,
    direction='clockwise',
    rotation=rotation_angle,
    hole=0
))

# Update trace properties
fig.update_traces(
    textposition='outside',
    textinfo='value',
    texttemplate='%{value}%',
    textfont_size=14
)

# Format the title
title_text = f"<b>{texts['title']}</b>" if texts.get('title') else ""

# Update layout for a clean and accurate presentation
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_xanchor='center',
    title_y=0.95,
    title_yanchor='top',
    title_font=dict(size=24),
    font=dict(family="Arial", size=14, color="black"),
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    width=600,
    height=400,
    margin=dict(l=50, r=160, t=80, b=50),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON path
output_filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{output_filename_base}.png"

# Save the chart as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")