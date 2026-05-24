import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

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
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False  # Prevents text on top of bars from being clipped
))

# Update the layout
fig.update_layout(
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 60],
        tickvals=[0, 10, 20, 30, 40, 50, 60],
        gridcolor='#E5E5E5',
        linecolor='black'
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=100),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.2, # Positioned below the x-axis
            xanchor='right',
            yanchor='top',
            font=dict(size=10)
        )
    ]
)

# Define the output image filename based on the input JSON filename
output_filename = json_file_path.stem + '.png'

# Save the figure to a PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")