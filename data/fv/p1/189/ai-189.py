import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from JSON ---
# The script requires the JSON file path as a command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract Data and Texts ---
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# --- 3. Create the Chart ---
fig = go.Figure()

# Add the pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # Preserve the original order from the JSON file
    direction='clockwise'
))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    legend=dict(
        x=1,
        y=0.8,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='black',
        borderwidth=1
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    margin=dict(l=50, r=250, t=100, b=50), # Increased right margin for legend
    paper_bgcolor='#D3D3D3',
    plot_bgcolor='white', # The chart area itself is white
    showlegend=True
)

# --- 5. Save the Output ---
# Derive the output filename from the input JSON filename
output_filename = json_path.with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")