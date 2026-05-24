import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read chart data and configuration from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{json_file_path}'.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly by extracting labels and values while preserving order
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1.5)
    ),
    textinfo='label',
    textposition='outside',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    rotation=-15  # Adjusts the start angle to match the source image
))

# Configure the layout of the chart
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"
    
# Create a caption by combining source and note
caption_parts = []
if texts.get('source'):
    caption_parts.append(texts['source'])
if texts.get('note'):
    caption_parts.append(texts['note'])
caption_text = "<br>".join(caption_parts)

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font_size=18,
    showlegend=False,
    font=dict(
        family="Arial",
        size=12
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=100, r=100, t=100, b=100),  # Generous margins for outside labels
    annotations=[
        dict(
            showarrow=False,
            text=caption_text,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ] if caption_text else []
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")