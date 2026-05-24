import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the config
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', {})
layout_elements = config.get('layout_elements', {})

# Initialize the figure
fig = go.Figure()

# Add procedural shapes (e.g., lines inside the globe)
if 'procedural_shapes' in layout_elements:
    if 'globe_lines' in layout_elements['procedural_shapes']:
        line_config = layout_elements['procedural_shapes']['globe_lines']
        y_positions = [line_config['y_start'] + i * (line_config['y_end'] - line_config['y_start']) / (line_config['count'] - 1) for i in range(line_config['count'])]
        for y_pos in y_positions:
            fig.add_shape(
                type="line",
                x0=line_config['x0'], y0=y_pos,
                x1=line_config['x1'], y1=y_pos,
                line=dict(
                    color=colors.get(line_config['color_key']),
                    width=line_config.get('width', 2)
                ),
                layer=line_config.get('layer', 'below')
            )

# Add shapes from the layout configuration
for shape_config in layout_elements.get('shapes', []):
    shape_copy = shape_config.copy()
    if 'fillcolor_key' in shape_copy:
        shape_copy['fillcolor'] = colors.get(shape_copy.pop('fillcolor_key'))
    fig.add_shape(shape_copy)

# Add data traces (bars)
for series in chart_data:
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        width=series.get('width'),
        marker_color=colors.get('bars'),
        name=series.get('name', ''),
        hoverinfo='none'
    ))

# Add annotations (text elements)
for anno_config in layout_elements.get('annotations', []):
    anno_copy = anno_config.copy()
    text_key = anno_copy.pop('text_key', None)
    if text_key:
        anno_copy['text'] = texts.get(text_key, '')
        
    anno_copy['font'] = dict(
        family="Arial",
        size=anno_copy.pop('font_size', 12),
        color=colors.get('text')
    )
    fig.add_annotation(anno_copy)

# Configure the layout
fig.update_layout(
    paper_bgcolor=colors.get('background'),
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False,
    xaxis=dict(
        visible=False,
        range=layout_elements.get('xaxis_range')
    ),
    yaxis=dict(
        visible=False,
        range=layout_elements.get('yaxis_range')
    ),
    margin=dict(t=20, b=20, l=20, r=20),
    width=layout_elements.get('figure_size', {}).get('width', 650),
    height=layout_elements.get('figure_size', {}).get('height', 500)
)

# Determine the output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")