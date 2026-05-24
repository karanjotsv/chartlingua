import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly trace
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    textinfo='percent',
    textposition='outside',
    sort=False,  # This is crucial to preserve the original order
    direction='clockwise',
    hoverinfo='label+percent'
)

# Initialize the figure
fig = go.Figure(data=[pie_trace])

# Construct the title string from the JSON data
title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle')
if subtitle_text:
    title_text += f"<br><sub>{subtitle_text}</sub>"

# Construct the source/note string from the JSON data
source_text = texts.get('source')
note_text = texts.get('note')
caption_parts = []
if source_text:
    caption_parts.append(f"Source: {source_text}")
if note_text:
    caption_parts.append(f"Note: {note_text}")
caption_text = "<br>".join(caption_parts)

# Update layout for a clean and accurate presentation
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5,
        itemsizing='constant'
    ),
    margin=dict(l=40, r=40, t=100, b=80),
    paper_bgcolor='#f0e6ff',
    plot_bgcolor='#f0e6ff'
)

# Add annotations for source and notes if they exist
if caption_text:
    fig.add_annotation(
        text=caption_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.2, # Adjust position to be below the legend
        xanchor='left',
        yanchor='bottom'
    )

# Set the text font size for the percentage labels outside the pie
fig.update_traces(textfont_size=14)

# Define the output filename based on the input JSON filename
output_filename = json_file_path.stem + ".png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")