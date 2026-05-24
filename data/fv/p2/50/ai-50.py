import sys
import json
import os
import plotly.graph_objects as go

# Load data from the JSON file provided as a command-line argument
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and styles from the JSON object
chart_data = config['chart_data']
colors = config['colors']

# Prepare data specifically for the Plotly pie chart
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"{item['category']}<br>{item['value']}%" for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=text_labels,
    textinfo='text',
    textposition='inside',
    textfont=dict(family="Arial", size=16, color='black'),
    marker=dict(colors=colors, line=dict(color='white', width=2)),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=135
))

# Update the layout of the chart
fig.update_layout(
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output image filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(sys.argv[1]))[0]
output_image_path = f"{base_filename}.png"

# Write the figure to a PNG image file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")