import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the file path from command line arguments
json_file_path = Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Create the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(data_series):
    color = colors[i % len(colors)] if colors else None
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines+markers',
        line=dict(color=color, width=1.5),
        marker=dict(
            color=color,
            size=7,
            line=dict(
                color='black',
                width=1
            )
        )
    ))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(size=16)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, 51],
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='#CCCCCC',
        gridwidth=1,
        griddash='dot'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[-5, 115],
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='#CCCCCC',
        gridwidth=1,
        griddash='dot'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        x=1,
        y=1,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='black',
        borderwidth=1,
        font=dict(size=10)
    ),
    margin=dict(l=90, r=50, t=80, b=80)
)

# Generate output filename from the input JSON filename
output_filename = json_file_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")