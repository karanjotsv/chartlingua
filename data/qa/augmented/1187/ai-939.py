import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# Extract data and text from the JSON structure
chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

# Prepare data for plotting
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
bar_color = colors[0] if colors else '#1976D2'

# Format text for display on bars (with space as thousand separator)
bar_texts = [f'{v:,}'.replace(',', ' ') for v in values]

# --- 2. Create the Chart ---
# Initialize the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=bar_texts,
    textposition='outside',
    marker_color=bar_color,
    cliponaxis=False  # Allow text to be drawn outside the plot area
))

# --- 3. Configure Layout and Styling ---
# Combine title and subtitle using HTML for flexible styling
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

# Update layout properties
fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    title_y=0.95,
    title_xanchor='left',
    title_yanchor='top',
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=60, b=80),
    yaxis=dict(
        range=[0, 800000],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False,
        ticks='outside',
        ticklen=5
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        ticks='outside',
        ticklen=5
    )
)

# Add source annotation at the bottom right
fig.add_annotation(
    text=texts.get('source'),
    align='right',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=1,
    y=0,
    xanchor='right',
    yanchor='top',
    yshift=-35,
    font=dict(size=10)
)

# --- 4. Output the Image ---
# Derive the output filename from the input JSON filename
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as '{output_filename}'")