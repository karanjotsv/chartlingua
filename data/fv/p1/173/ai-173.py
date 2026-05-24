import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load all data and settings from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data for the pie chart trace
labels = [item['label'] for item in config['chart_data']]
values = [item['value'] for item in config['chart_data']]

# Create the main figure and add the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=config['colors']['slices'], line=dict(color='black', width=1)),
    sort=False,
    direction='clockwise',
    rotation=config['layout_options']['pie_rotation'],
    textinfo='label',
    textposition='inside',
    insidetextorientation='horizontal',
    textfont=dict(
        family="Arial",
        size=9,
        color=config['colors']['pie_text']
    ),
    hole=0
)])

# Build annotations from the JSON configuration
annotations = []
for ann_data in config['layout_options']['annotations']:
    annotations.append(go.layout.Annotation(
        text=config['texts'][ann_data['text_key']],
        x=ann_data['x'],
        y=ann_data['y'],
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(
            family="Arial",
            size=ann_data['font_size'],
            color=config['colors'][ann_data['color_key']]
        ),
        align=ann_data['align']
    ))

# Build shapes from the JSON configuration
shapes = []
for shape_data in config['layout_options']['shapes']:
    shapes.append(go.layout.Shape(
        type="path",
        path=shape_data['path'],
        xref="paper",
        yref="paper",
        line=dict(
            color=config['colors'][shape_data['color_key']],
            width=shape_data['width']
        )
    ))

# Apply layout settings, including annotations and shapes
fig.update_layout(
    showlegend=False,
    paper_bgcolor=config['colors']['background'],
    plot_bgcolor=config['colors']['background'],
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(family="Arial"),
    annotations=annotations,
    shapes=shapes
)

# Determine the output image filename from the input JSON filename
if '.' in json_file_path:
    base_name = json_file_path.rsplit('.', 1)[0]
else:
    base_name = json_file_path
output_image_path = f"{base_name}.png"

# Save the generated figure to a high-resolution PNG file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")