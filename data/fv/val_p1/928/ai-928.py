import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# --- 2. Prepare Data for Plotly ---
# Extract labels and values, preserving the order from the JSON file
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    textinfo='none', # No text on slices
    hoverinfo='label+percent',
    showlegend=True,
    rotation=-15 # Slightly rotate to match the original image
))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle using HTML for rich text formatting
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br>{texts['subtitle']}"

# Combine source and note for the annotation
# Note: In this case, both are null so nothing will be displayed.
source_text = []
if texts.get("source"):
    source_text.append(f"Source: {texts['source']}")
if texts.get("note"):
    source_text.append(f"Note: {texts['note']}")
source_note_text = "<br>".join(source_text)

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
        'size': 14
    },
    legend={
        'orientation': 'v',
        'x': 0.9,
        'y': 0.5,
        'xanchor': 'left',
        'yanchor': 'middle'
    },
    # Add margins to prevent clipping of title, legend, or annotations
    margin=dict(l=50, r=250, t=100, b=50),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Add annotation for source/note if it exists
if source_note_text:
    fig.add_annotation(
        text=source_note_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.1,
        xanchor='left',
        yanchor='top'
    )

# --- 5. Output the Image ---
# Derive the output filename from the input JSON filename
output_filename = json_path.with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")