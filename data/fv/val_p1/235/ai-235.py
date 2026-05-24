import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        mode='lines',
        line=dict(color=colors[i % len(colors)], width=3),
        showlegend=False
    ))

# Add annotations for series labels
for ann in texts.get("annotations", []):
    fig.add_annotation(
        x=ann.get("x"),
        y=ann.get("y"),
        text=ann.get("text"),
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        xshift=10,
        font=dict(family="Arial", size=12),
        align='left'
    )

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get("title"),
        x=0.5,
        font=dict(size=22)
    ),
    xaxis=dict(
        title=texts.get("x_axis_title"),
        tickvals=[3, 6, 9, 12],
        range=[-0.5, 15],  # Extend range to fit annotations
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title=texts.get("y_axis_title"),
        tickvals=[-4, -3, -2, -1, 0, 1, 2, 3],
        range=[-4.2, 3.2],
        showgrid=True,
        gridwidth=1,
        gridcolor='LightGray',
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='black',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=150, t=100, b=80)
)

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)