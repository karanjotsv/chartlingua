import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x', []),
        y=series.get('y', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Update layout
fig.update_layout(
    title_text=texts.get('title', ''),
    xaxis_title=texts.get('x_axis_title', ''),
    yaxis_title=texts.get('y_axis_title', ''),
    barmode='group',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),
    margin=dict(l=80, r=40, t=100, b=100)
)

# Add source annotation at the bottom right
fig.add_annotation(
    text=texts.get('source', ''),
    align='right',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.95,
    y=-0.15,
    xanchor='right',
    yanchor='bottom'
)

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`) for image export.")
    sys.exit(1)