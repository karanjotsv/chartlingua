import sys
import json
import plotly.graph_objects as go
import os

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the file path from the command-line argument
json_file_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Create a new figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i % len(colors)],
        text=[f"{val}%" for val in series['y']],
        textposition='outside',
        cliponaxis=False
    ))

# Update the layout of the figure
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgrey',
        range=[0, 100],
        ticksuffix='%'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=40, t=50, b=150),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left'
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Set the text font for the bar labels
fig.update_traces(textfont_size=12, textfont_color='#000000')

# Determine output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")