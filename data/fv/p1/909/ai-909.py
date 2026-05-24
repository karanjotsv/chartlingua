import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_info['chart_data']
values = [item['value'] for item in chart_data]
display_labels = [item['display_label'] for item in chart_data]
colors = chart_info['colors']

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    values=values,
    labels=display_labels,
    marker_colors=colors,
    textinfo='none',
    hoverinfo='label',
    sort=False,
    direction='clockwise',
    rotation=110  # Start the first slice near the top (12 o'clock)
)])

# Update layout for a clean appearance and to match the original
fig.update_layout(
    showlegend=False,
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=100, r=100, t=50, b=50),
    plot_bgcolor='white',
    paper_bgcolor='white',
    # Add a border around the entire plot area
    shapes=[
        dict(
            type='rect',
            xref='paper', yref='paper',
            x0=0, y0=0, x1=1, y1=1,
            line=dict(color='black', width=1)
        )
    ]
)

# Determine output filename from JSON path
output_path = pathlib.Path(json_path)
output_filename = output_path.with_suffix('.png')

# Save the figure as a PNG image
try:
    fig.write_image(str(output_filename), scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)