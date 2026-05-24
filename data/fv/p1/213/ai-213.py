import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first command-line argument.
if len(sys.argv) < 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and settings from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    sort=False,  # Preserve the order from the JSON data
    direction='counterclockwise',
    hoverinfo='label+percent',
    textinfo='none'
))

# --- 3. Configure Layout and Styling ---
title_text = texts.get('title', '')

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(size=18)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        x=0.85,
        y=0.7,
        traceorder="normal",
        font=dict(
            family="Arial",
            size=11
        ),
        bgcolor='white',
        bordercolor='black',
        borderwidth=0
    ),
    margin=dict(l=40, r=40, t=80, b=40),
    plot_bgcolor='white',
    paper_bgcolor='white',
    width=500,
    height=375
)

# --- 4. Output the Image ---
# Derive the output filename from the input JSON filename
base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file with a higher resolution
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved to '{output_filename}'")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)