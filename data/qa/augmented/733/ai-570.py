import sys
import json
import os
import plotly.graph_objects as go

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the specified file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in file {json_path}")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    name=''
))

# Combine source and note for the annotation
source_parts = []
if texts.get('source'):
    source_parts.append(texts['source'])
if texts.get('note'):
    source_parts.append(texts['note'])
source_text = "<br>".join(source_parts)

# Update layout for styling and text
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1000000],
        tickvals=[0, 200000, 400000, 600000, 800000, 1000000],
        ticktext=['0', '200 000', '400 000', '600 000', '800 000', '1 000 000'],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    showlegend=False,
    margin=dict(l=120, r=40, t=40, b=120),
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=-0.25,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)