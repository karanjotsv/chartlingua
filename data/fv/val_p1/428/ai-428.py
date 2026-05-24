import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load the JSON data
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# --- 2. Create the Plotly Figure ---
# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series, maintaining order
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i % len(colors)]  # Cycle through colors if not enough are provided
    ))

# --- 3. Configure Layout and Styling ---
# Combine title and subtitle using HTML for rich text formatting
title_parts = []
if texts.get('title'):
    title_parts.append(f"<span style='font-size: 18px;'><b>{texts['title']}</b></span>")
if texts.get('subtitle'):
    title_parts.append(f"<span style='font-size: 14px; color: #555;'>{texts['subtitle']}</span>")
combined_title = "<br>".join(title_parts)

# Update the layout of the figure
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    title=dict(
        text=combined_title,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1.5,
        linecolor='black',
        showgrid=False,
        automargin=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 45],
        dtick=5,
        showline=False,
        showgrid=True,
        gridcolor='#D3D3D3',
        zeroline=False
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="right",
        x=0.98,
        bgcolor='rgba(255,255,255,0.5)'
    ),
    margin=dict(l=50, r=50, t=60, b=150) # Increased bottom margin for long labels
)

# --- 4. Add Source/Note Annotation ---
# Combine source and note for a single annotation block
annotation_parts = []
if texts.get('source'):
    annotation_parts.append(texts['source'])
if texts.get('note'):
    annotation_parts.append(texts['note'])
combined_annotation = "<br>".join(annotation_parts)

if combined_annotation:
    fig.add_annotation(
        text=combined_annotation,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.0,
        y=-0.25, # Position below the x-axis, adjust if necessary
        xanchor='left',
        yanchor='top',
        font=dict(size=10, color="#666666")
    )


# --- 5. Output the Image ---
# Derive the output filename from the input JSON filename
output_filename = json_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")