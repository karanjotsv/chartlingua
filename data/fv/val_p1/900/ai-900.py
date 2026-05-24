import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# --- 2. Load and Parse JSON Data ---
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])
style = config.get('style', {})

# Extract data for the pie chart, maintaining the original order
labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    textinfo='percent',
    textposition='outside',
    sort=False,  # This is crucial to preserve the order from the JSON file
    hoverinfo='label+percent',
    direction='clockwise'
))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle using HTML for multi-line support
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    if title_text:
        title_text += "<br>"
    title_text += texts['subtitle']

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    font={
        'family': "Arial",
        'size': 12,
        'color': "black"
    },
    legend={
        'orientation': "h",
        'yanchor': "top",
        'y': -0.1,  # Position legend below the chart area
        'xanchor': "center",
        'x': 0.5
    },
    plot_bgcolor=style.get('plot_bgcolor', 'white'),
    paper_bgcolor=style.get('paper_bgcolor', 'white'),
    margin=dict(t=120, b=120, l=40, r=40) # Add margins to prevent clipping
)

# --- 5. Generate and Save Output Image ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have the 'kaleido' package installed (`pip install kaleido`)")
    sys.exit(1)