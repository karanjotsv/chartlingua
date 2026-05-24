import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Use pathlib to handle the input path
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly trace
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0] if colors else '#337ab7'),
    text=[f"{v}%" for v in values],
    textposition='outside',
    cliponaxis=False,
    hoverinfo='none',
    textfont=dict(family="Arial", size=12, color='black')
))

# Construct the title using HTML for potential subtitles
title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle', '')
if title_text and subtitle_text:
    full_title = f"<b>{title_text}</b><br><span style='font-size:0.8em;'>{subtitle_text}</span>"
elif title_text:
    full_title = f"<b>{title_text}</b>"
else:
    full_title = None

# Update the layout of the chart for a clean, professional look
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, 38],  # Extend range to prevent text clipping
        tickvals=[0, 5, 10, 15, 20, 25, 30, 35],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange="reversed",  # This ensures the order from the JSON is displayed top-to-bottom
        showgrid=False,
        showline=False
    ),
    margin=dict(l=110, r=50, t=40, b=80),  # Adjust margins to fit labels and source
)

# Add source annotation if it exists
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=1, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=10, color="grey")
    )

# Determine the output filename and save the chart as a PNG image
output_filename = json_path.stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as {output_filename}")