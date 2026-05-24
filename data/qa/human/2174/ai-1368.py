import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Derive the base filename for the output image from the JSON filename
output_filename_base = json_file_path.stem

# Load chart configuration from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series specified in the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i],
        text=series['y'],
        texttemplate='<b>%{y}%</b>',
        textposition='outside'
    ))

# Construct the title and subtitle using HTML for rich text formatting
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

# Update the layout of the chart
fig.update_layout(
    barmode='group',
    title_text=full_title,
    title_x=0.5,
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=60, b=100),
    yaxis=dict(
        range=[0, 105],
        showgrid=True,
        gridcolor='#dddddd',
        griddash='dot',
        tickvals=[0, 20, 40, 60, 80, 100],
        ticktext=[f"{v}%" for v in [0, 20, 40, 60, 80, 100]],
        zeroline=False,
        showline=True,
        linecolor='black'
    ),
    xaxis=dict(
        showline=True,
        linecolor='black',
        ticks='outside'
    )
)

# Update trace properties for better text visibility
fig.update_traces(
    textfont_size=12,
    cliponaxis=False
)

# Add source text as an annotation if it exists
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0, y=-0.3,
        showarrow=False,
        align="left",
        xanchor="left",
        font=dict(size=10)
    )

# Save the figure as a high-resolution PNG image
output_file_path = f"{output_filename_base}.png"
fig.write_image(output_file_path, scale=2)

print(f"Chart successfully generated and saved to {output_file_path}")