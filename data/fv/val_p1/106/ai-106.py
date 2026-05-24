import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data ---
# The script expects the path to the JSON file as the single command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly Pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
display_texts = [item['display_text'] for item in chart_data]

# --- 2. Create Figure ---
fig = go.Figure()

# Add the Pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=display_texts,
    textinfo='text',
    textposition='outside',
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    sort=False,
    direction='clockwise',
    rotation=45,  # Adjusts start position to match original
    hoverinfo='label+percent'
))

# --- 3. Configure Layout ---
# Combine title and subtitle if available
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for an annotation
source_text = ""
if texts.get('source'):
    source_text += texts['source']
if texts.get('note'):
    source_text += f"<br>{texts['note']}"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font=dict(
        family="Arial",
        size=24
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100, b=80, l=60, r=60),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,
            xanchor="left",
            yanchor="top",
            font=dict(family="Arial", size=12)
        )
    ]
)

# Set the text font for the pie slice labels
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    ),
    outsidetextfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
)

# --- 4. Output Image ---
# Derive the output filename from the input JSON filename
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)