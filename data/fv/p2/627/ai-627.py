import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read and load the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    texttemplate='%{label}<br>%{value}%',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    rotation=79 # Position the 'Other' slice near the top for visual consistency
))

# Configure the layout
# Combine title and subtitle using HTML tags for rich text formatting
title_text = ''
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Prepare the source/note text
source_text = texts.get('source', '')

fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5, # Center the title
    font=dict(family="Arial", size=12),
    showlegend=False,
    # Adjust margins to prevent labels from being clipped
    margin=dict(l=120, r=100, t=60, b=60),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            x=0,
            y=-0.1,
            xref="paper",
            yref="paper",
            xanchor="left",
            yanchor="top",
            align="left"
        )
    ] if source_text else []
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Write the image file with a higher scale for better resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")