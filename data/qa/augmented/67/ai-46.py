import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=[f'{v}%' for v in values],
    textposition='outside',
    textfont=dict(size=12, family="Arial"),
    hoverinfo='none',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 50],
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=80),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2, # Position below x-axis
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Determine output filename from JSON path
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")