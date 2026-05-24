import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
custom_text = [f"<b>{item['label']}</b><br>{item['value']}%" for item in chart_data]

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    text=custom_text,
    textinfo='text',
    hoverinfo='label+percent',
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    sort=False,
    direction='clockwise',
    textposition='auto',
    insidetextfont=dict(family="Arial", size=14, color='white'),
    outsidetextfont=dict(family="Arial", size=14, color='black'),
    rotation=80 # Adjust starting angle to match the image
)])

# Update the layout of the figure
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_y=0.95,
    title_font=dict(family="Arial", size=18, color='black'),
    font=dict(family="Arial"),
    showlegend=False,
    margin=dict(l=40, r=40, t=100, b=40),
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# Determine the output filename and save the chart
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")