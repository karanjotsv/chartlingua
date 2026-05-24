import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data ---
# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load the chart data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly Pie chart
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# --- 2. Create Chart ---
# Initialize a Figure object
fig = go.Figure()

# Add the Pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    texttemplate=[f"<b>{l}</b><br>{v}%" for l, v in zip(labels, values)],
    textposition='inside',
    insidetextfont=dict(color='white', family='Arial', size=16),
    hoverinfo='label+percent',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise'
))

# --- 3. Configure Layout ---
# Construct the title string, combining title and subtitle if available
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout properties
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=18, family='Arial', color='black')
    ),
    showlegend=False,
    font=dict(family='Arial'),
    margin=dict(t=80, b=40, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# --- 4. Save Output ---
# Define the output filename based on the input JSON filename
output_path = json_path.with_suffix('.png')

# Save the figure as a PNG image with a high resolution
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")