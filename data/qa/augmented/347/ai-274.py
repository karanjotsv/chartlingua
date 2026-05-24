import sys
import json
import plotly.graph_objects as go
import pathlib

# Check if the JSON file path is provided as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
base_filename = pathlib.Path(json_path).stem

# Read and parse the JSON configuration file.
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object.
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize a Plotly Figure.
fig = go.Figure()

# Add a bar trace for each data series specified in the JSON.
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Combine title and subtitle using HTML for rich formatting.
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

# Combine source and note texts.
source_text = texts.get('source')
note_text = texts.get('note')
source_note_text = ""
if source_text:
    source_note_text += source_text
if note_text:
    source_note_text += f"<br>{note_text}"

# Configure the chart layout, axes, fonts, and annotations.
fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 18],
        tickmode='array',
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5],
        gridcolor='#E0E0E0',
        gridwidth=1,
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickangle=0 # Keep labels horizontal as they fit well
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            text=source_note_text,
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.25,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10, color="#555555")
        )
    ]
)

# Apply specific styling to the axes lines.
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=False)
fig.update_yaxes(showline=False)

# Generate and save the chart as a PNG image.
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as {output_filename}")