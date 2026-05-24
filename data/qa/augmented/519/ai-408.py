import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    texttemplate='%{text}',
    marker_color=colors[0] if colors else None,
    cliponaxis=False  # Prevents data labels from being clipped
))

# Combine title and subtitle
title_text = texts.get('title', '') or ''
subtitle_text = texts.get('subtitle', '') or ''
if title_text and subtitle_text:
    full_title = f"<b>{title_text}</b><br><sub>{subtitle_text}</sub>"
elif title_text:
    full_title = f"<b>{title_text}</b>"
else:
    full_title = subtitle_text

# Update layout
fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    title_y=0.95,
    title_font_size=20,
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        linecolor='black',
        range=[0, max(y_values) * 1.15] # Add headroom for text labels
    ),
    margin=dict(l=90, r=40, t=60, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper', yref='paper',
            x=0.99, y=-0.18,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Generate output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")