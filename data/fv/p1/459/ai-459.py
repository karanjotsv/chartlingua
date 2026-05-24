import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    marker_line_color='black',
    marker_line_width=1.5
))

# Update layout to match the original image
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(
            family="Arial",
            size=24,
            color="black",
            weight="bold"
        )
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    plot_bgcolor='#C0C0C0',
    paper_bgcolor='white',
    showlegend=False,
    bargap=0.25,
    margin=dict(l=80, r=40, t=100, b=80),
    yaxis=dict(
        range=[0, 5],
        tickmode='linear',
        dtick=1,
        gridcolor='#808080',
        gridwidth=1,
        zeroline=False,
        showline=True,
        linewidth=2,
        linecolor='black',
        ticks='outside',
        tickwidth=2,
        tickcolor='black'
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=2,
        linecolor='black',
        ticks='outside',
        tickwidth=2,
        tickcolor='black'
    )
)

# Determine the output filename from the input JSON path
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Write the image to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")