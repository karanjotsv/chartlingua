import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) < 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get file paths from argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in file {json_path}")
    sys.exit(1)

# Create figure
fig = go.Figure()

# Add traces from JSON data
for series, color in zip(chart_data['chart_data'], chart_data['colors']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=color, width=2)
    ))

# Update layout
fig.update_layout(
    title_text=chart_data['texts']['title'],
    xaxis_title=chart_data['texts']['x_axis_title'],
    yaxis_title=chart_data['texts']['y_axis_title'],
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridwidth=1,
        gridcolor='#D3D3D3',
        griddash='dot',
        tickvals=[300, 400, 500, 600, 700, 800, 900, 1000]
    ),
    yaxis=dict(
        type='log',
        exponentformat='power',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridwidth=1,
        gridcolor='#D3D3D3'
    ),
    margin=dict(l=90, r=40, t=40, b=80)
)

# Save the figure to a PNG file
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")