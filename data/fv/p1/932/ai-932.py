import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and settings from the JSON object
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']
shapes_data = chart_data['shapes']
annotations_data = chart_data['annotations']

# Initialize figure
fig = go.Figure()

# Add the main reaction curve
fig.add_trace(go.Scatter(
    x=data_series['x'],
    y=data_series['y'],
    mode='lines',
    line=dict(
        color=colors['curve'],
        width=3,
        shape='spline',
        smoothing=1.3
    ),
    hoverinfo='none'
))

# Prepare shapes (dashed lines)
shapes = []
for s in shapes_data:
    shapes.append(go.layout.Shape(
        type='line',
        x0=s['x0'], y0=s['y0'], x1=s['x1'], y1=s['y1'],
        line=dict(
            color=colors['lines'],
            width=s['line']['width'],
            dash=s['line']['dash']
        )
    ))

# Prepare annotations (text labels and arrows)
annotations = []
for anno_template in annotations_data:
    anno = anno_template.copy()
    if 'text_key' in anno:
        anno['text'] = texts[anno.pop('text_key')]
    if 'font_color_key' in anno:
        anno['font'] = dict(color=colors[anno.pop('font_color_key')], size=14)
    if 'arrowcolor_key' in anno:
        anno['arrowcolor'] = colors[anno.pop('arrowcolor_key')]
    annotations.append(anno)

# Update layout with all elements and styling
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        font=dict(size=24, color=colors['black'])
    ),
    xaxis=dict(
        title=dict(text=texts['x_axis_title'], font=dict(size=16, color=colors['black'])),
        range=[0, 110],
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        linecolor=colors['black'],
        linewidth=2
    ),
    yaxis=dict(
        title=dict(text=texts['y_axis_title'], font=dict(size=16, color=colors['black'])),
        title_standoff=15,
        range=[0, 100],
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        linecolor=colors['black'],
        linewidth=2
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    shapes=shapes,
    annotations=annotations,
    margin=dict(l=90, r=40, t=90, b=80)
)

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")