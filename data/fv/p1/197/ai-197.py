import sys
import json
import plotly.graph_objects as go
import os

# Check for the required command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", {})

# Prepare data for Plotly, preserving the order from the JSON
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
marker_colors = colors.get("marker_colors", [])
background_color = colors.get("background_color", "#FFFFFF")

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=marker_colors),
    hoverinfo='label+percent',
    textinfo='percent',
    textfont=dict(size=14, family="Arial"),
    textposition='outside',
    sort=False  # This is crucial to preserve the original data order
))

# Combine title and subtitle if available
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Combine source and note if available
source_text = []
if texts.get('source'):
    source_text.append(texts['source'])
if texts.get('note'):
    source_text.append(texts['note'])
caption_text = "<br>".join(source_text)

# Update layout for a professional look, handling potential overlaps
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    margin=dict(t=100, b=100, l=40, r=40),
    annotations=[
        dict(
            text=caption_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.2, # Adjust position to be below the legend
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ] if caption_text else []
)

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have the 'kaleido' package installed (`pip install kaleido`)")
    sys.exit(1)