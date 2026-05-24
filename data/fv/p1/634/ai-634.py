import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the structured data from the JSON file.
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts for plotting.
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
title_text = texts.get('title', '')

# --- 2. Create the Plotly Figure ---
# Initialize a Figure object.
fig = go.Figure()

# Add the pie chart trace.
# The data is processed in the order it appears in the JSON file.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=2)
    ),
    hoverinfo='label+percent',
    textinfo='percent',
    textfont=dict(family='Arial', size=14, color='#FFFFFF'),
    sort=False,  # This is crucial to preserve the order from the JSON file.
    direction='clockwise',
    rotation=120 # Adjusts the start angle to match the source image.
))

# --- 3. Configure Layout and Styling ---
# Update layout properties for a clean and accurate representation.
fig.update_layout(
    title=dict(
        text=f"<b>{title_text}</b>",
        y=0.95,
        x=0.05,
        xanchor='left',
        yanchor='top',
        font=dict(family='Arial', size=18)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        x=0.8,
        y=0.95,
        xanchor='left',
        yanchor='top',
        traceorder='normal',
        bgcolor='rgba(255,255,255,0)' # Transparent background
    ),
    margin=dict(t=100, b=30, l=30, r=30),
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)',
    showlegend=True
)

# By default, Plotly might hide text on very small slices. This ensures it's always visible.
fig.update_traces(textposition='inside')

# --- 4. Output the Figure ---
# Derive the output filename from the input JSON file path.
output_filename = f"{Path(json_path).stem}.png"

# Save the figure to a high-resolution PNG file.
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")