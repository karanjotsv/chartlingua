import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

# Extract data from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)])
    ))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=80),
    xaxis=dict(
        range=[0, 8],
        tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        zeroline=False
    ),
    yaxis=dict(
        range=[0, 2.5],
        tickvals=[0, 0.5, 1, 1.5, 2, 2.5],
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        zeroline=False
    )
)

# Derive output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)