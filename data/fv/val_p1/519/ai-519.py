import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Verify the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and text from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Create the pie chart trace
pie_trace = go.Pie(
    labels=[d['label'] for d in chart_data],
    values=[d['value'] for d in chart_data],
    text=[d['display_text'] for d in chart_data],
    textinfo='text',
    insidetextfont=dict(family="Arial", color='white', size=14),
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    sort=False,  # Preserve the original data order
    direction='clockwise'
)

# Create the figure and add the trace
fig = go.Figure(data=[pie_trace])

# Update the layout for a clean and accurate presentation
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.05,
    title_y=0.95,
    title_font=dict(family="Arial", size=24, color='#757575'),
    font=dict(family="Arial", size=12),
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=40, r=40, t=100, b=40)
)

# Define the output filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")