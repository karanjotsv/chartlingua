import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json>")
    sys.exit(1)

# Get the JSON file path from command-line arguments
json_path_str = sys.argv[1]
json_path = pathlib.Path(json_path_str)

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path_str}")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path_str}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON
data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', {})

# Prepare data for Plotly
categories = [d['category'] for d in data]
values = [d['value'] for d in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors.get('series_colors', ['#0000FF'])[0],
    marker_line=dict(color=colors.get('bar_outline_color', '#000000'), width=1.5),
    name='' # Hide trace name from hover info
))

# Update layout to match the original chart's appearance
fig.update_layout(
    font=dict(
        family="Arial",
        color=colors.get('text_color', '#000000')
    ),
    title=dict(
        text=texts.get('title') or '',
        x=0.5, # Center title
        xanchor='center'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor=colors.get('plot_bg_color', '#FFFFFF'),
    paper_bgcolor=colors.get('plot_bg_color', '#FFFFFF'),
    showlegend=False,
    margin=dict(l=50, r=20, t=30, b=50),
    xaxis=dict(
        type='category',
        showline=True,
        linewidth=1.5,
        linecolor=colors.get('axis_color', '#000000'),
        mirror=True,
        showgrid=False
    ),
    yaxis=dict(
        range=[0, 10],
        dtick=2,
        showline=True,
        linewidth=1.5,
        linecolor=colors.get('axis_color', '#000000'),
        mirror=True,
        showgrid=False,
        zeroline=False
    )
)

# Derive output filename from the input JSON path
output_filename = json_path.stem + ".png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)