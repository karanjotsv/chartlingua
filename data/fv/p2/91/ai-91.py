import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data ---
# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at '{json_file_path}'")
    sys.exit(1)

# Load the chart data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data components from the JSON structure
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly pie chart
labels = [d.get("label", "") for d in chart_data]
values = [d.get("value", 0) for d in chart_data]

# --- 2. Create Chart ---
# Initialize a Figure object
fig = go.Figure()

# Add the pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1.5)),
    sort=False,  # This is crucial to maintain the original order
    direction='clockwise',
    rotation=90, # Starts the first slice at 12 o'clock position
    hoverinfo='label+percent',
    textinfo='none'
))

# --- 3. Configure Layout ---
# Construct the title string from title and subtitle
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout properties for a clean and accurate appearance
fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.5,
    title_y=0.95,
    title_font=dict(family="Arial", size=18, color="black"),
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    margin=dict(l=20, r=20, t=50, b=20),
    paper_bgcolor='rgba(255,255,255,0)',
    plot_bgcolor='rgba(255,255,255,0)'
)

# Add a source annotation if it exists in the JSON
if texts.get("source"):
    fig.add_annotation(
        text=texts["source"],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.1,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=10, color="grey")
    )

# --- 4. Output Image ---
# Generate the output filename from the input JSON path
output_filename = json_file_path.with_suffix('.png')

# Write the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")