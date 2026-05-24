import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    text=y_values,
    textposition='outside',
    cliponaxis=False # Ensures text labels are not clipped by the plot area
))

# Combine title and subtitle
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if title_text and subtitle_text:
    full_title = f"{title_text}<br><sub>{subtitle_text}</sub>"
elif title_text:
    full_title = title_text
else:
    full_title = None

# Combine source and note for annotation
source_text = texts.get('source') or ''
note_text = texts.get('note') or ''
if source_text and note_text:
    full_source = f"{source_text}<br>{note_text}"
else:
    full_source = source_text or note_text

# Update layout
fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showgrid=False,
        showline=True,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 180],
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=full_source,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='grey')
        )
    ]
)

fig.update_traces(textfont_size=12)

# Define output filename and save the image
base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)