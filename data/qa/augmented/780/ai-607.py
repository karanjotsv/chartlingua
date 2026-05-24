import sys
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data from the file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and text from the JSON structure
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [item['x'] for item in data]
y_values = [item['y'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    text=[f'{val:,}'.replace(',', ' ') for val in y_values],
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False
))

# Combine title and subtitle
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if title_text and subtitle_text:
    full_title = f"{title_text}<br><sub>{subtitle_text}</sub>"
else:
    full_title = title_text or subtitle_text

# Update layout
fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    yaxis=dict(
        showgrid=True,
        gridcolor='#E5E5E5',
        range=[0, 450000],
        dtick=50000,
        separatethousands=True,
        ticksuffix=" " # Adds a small space to prevent label clipping
    ),
    xaxis=dict(showgrid=False),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Generate the output filename from the input JSON path
output_filename = json_path.rsplit('.', 1)[0] + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")