import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Define the output image path based on the JSON filename
output_image_path = json_file_path.with_suffix(".png")

# Load data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_config.get("chart_data", [])
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])

# Prepare data for the pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    textinfo='none', # Use texttemplate for custom formatting
    texttemplate='%{label} %{value}%',
    textposition='outside',
    hole=0,
    sort=False,  # Preserve the original order from the JSON data
    direction='clockwise',
    hoverinfo='label+percent'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Prepare annotations list
annotations = []

# Add source text if available
source_text = texts.get("source")
if source_text:
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1.0, y=-0.1,
            xanchor='right', yanchor='top',
            text=source_text,
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )

# Add note text if available
note_text = texts.get("note")
if note_text:
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0.0, y=-0.1,
            xanchor='left', yanchor='top',
            text=note_text,
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )

# Update layout
fig.update_layout(
    title_text=texts.get("title"),
    showlegend=False,
    font=dict(family="Arial", size=14),
    margin=dict(l=80, r=80, t=80, b=80),
    annotations=annotations,
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)'
)

# Write the output image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to '{output_image_path}'")