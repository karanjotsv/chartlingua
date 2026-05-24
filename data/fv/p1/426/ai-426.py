import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data from the specified file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Prepare data for Plotly trace
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace with data labels
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='inside',
    textangle=-90,
    textfont=dict(color='white', size=11),
    insidetextanchor='middle'
))

# Construct the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout for a clean and accurate presentation
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=20)
    ),
    xaxis=dict(
        type='category',
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        visible=False  # Hide y-axis, labels, and gridlines
    ),
    plot_bgcolor='#E9E9E9',
    paper_bgcolor='#E9E9E9',
    font=dict(
        family="Arial",
        color="#000000"
    ),
    showlegend=False,
    margin=dict(t=80, b=50, l=40, r=40)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")