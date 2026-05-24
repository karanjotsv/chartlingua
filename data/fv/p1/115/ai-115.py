import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 2. Create the Chart ---
# Initialize the figure
fig = go.Figure()

# Add the pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='value',
    texttemplate='%{value}%',
    textfont=dict(family="Arial", size=14, color='black'),
    sort=False,  # Preserve the original data order
    direction='clockwise'
))

# --- 3. Configure Layout and Styling ---
# Combine title and subtitle if available
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><span style='font-size: 14px;'>{texts.get('subtitle')}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.98,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=20)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.88,
        xanchor="center",
        x=0.5,
        font=dict(family="Arial")
    ),
    font=dict(family="Arial", size=12),
    margin=dict(l=40, r=40, t=120, b=40),
    paper_bgcolor='rgba(255,255,255,1)',
    plot_bgcolor='rgba(255,255,255,1)'
)

# --- 4. Output the Image ---
# Derive the output filename from the input JSON filename
filename_base, _ = os.path.splitext(os.path.basename(json_file_path))
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")