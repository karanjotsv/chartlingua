import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_filename_base = json_path.stem
output_filename = f"{output_filename_base}.png"

# --- 2. Load Data from JSON ---
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# --- 3. Prepare Data for Plotly ---
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the text to display on each slice, combining the label and value
text_on_slices = [f"<b>{d['label']}</b><br>{d['value']}%" for d in chart_data]

# --- 4. Create the Chart ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,  # Used for hover text
    values=values,
    text=text_on_slices,
    textinfo='text',
    textposition='inside',
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    pull=[0.05] * len(values),  # Explode all slices slightly to mimic original
    sort=False,  # IMPORTANT: This preserves the original data order from the JSON
    direction='clockwise',
    rotation=30, # Position the first slice in the top-right
    textfont=dict(
        family="Arial",
        size=16,
        color="white"
    )
))

# --- 5. Configure Layout and Styling ---
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=24)
    ),
    font=dict(
        family="Arial",
        color="black"
    ),
    showlegend=False,
    margin=dict(t=120, b=80, l=40, r=40), # Add margins to prevent clipping
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=0.02,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    ]
)

# --- 6. Output the Image ---
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")