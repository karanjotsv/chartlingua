import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get file path from command-line argument
json_file_path = Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# --- Prepare data for Plotly ---
chart_data = data.get('chart_data', [])
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
texts_data = data.get('texts', {})
colors = data.get('colors', [])

# Prepare text labels for inside the pie chart slices
# This format matches the original: bold label, line break, value with '%'
text_labels = [f"<b>{d['label']}</b><br>{d['value']}%" for d in chart_data]

# Set text color based on background for readability, mimicking the original
insidetextfont_colors = ['white', 'black', 'black']

# --- Create the Plotly figure ---
fig = go.Figure()

# Add the Pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    text=text_labels,
    textinfo='text',
    insidetextfont=dict(
        family="Arial",
        size=18,
        color=insidetextfont_colors
    ),
    hoverinfo='none',
    sort=False,
    direction='clockwise',
    rotation=135 # Position the start of the first slice to match the visual
))

# --- Update layout and styling ---
fig.update_layout(
    title_text=texts_data.get('title', ''),
    title_font=dict(
        family="Arial",
        size=26,
        color='#333333'
    ),
    title_x=0.01,
    title_y=0.98,
    title_xanchor='left',
    title_yanchor='top',
    
    font_family="Arial",
    showlegend=False,
    
    margin=dict(t=150, b=60, l=20, r=20),
    
    paper_bgcolor='white',
    plot_bgcolor='white',
    
    annotations=[
        dict(
            text=texts_data.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0.01,
            xanchor='left',
            yanchor='bottom',
            font=dict(
                family="Arial",
                size=12,
                color='grey'
            )
        )
    ]
)

# --- Output the image ---
# Derive output filename from the input JSON filename
output_filename = json_file_path.stem + ".png"

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")