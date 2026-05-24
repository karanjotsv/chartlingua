import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data series from JSON
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(
        color=colors[0],
        line=dict(color='black', width=1.5)
    ),
    showlegend=False
))

# Build combined title string
title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><i>{texts['subtitle']}</i>"

# Update layout for a professional look and feel
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=18)
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='white',
        gridwidth=1,
        zeroline=False,
        range=[0, 25]
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        autorange='reversed',  # To display categories from top to bottom as in the image
        showgrid=False
    ),
    plot_bgcolor='#F0F0F0',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=80, r=40, t=80, b=80),  # Adjust margins to prevent clipping
    showlegend=False
)

# Derive output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")