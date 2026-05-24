import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure
fig = go.Figure()

# Add bar traces from the data
for i, series in enumerate(data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('series_name', ''),
        marker=dict(
            color=colors['series_colors'][i],
            line=dict(
                color=colors['border'],
                width=1
            )
        ),
        showlegend=False
    ))

# Update the layout to match the original chart's style
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor='white',
    bargap=0.1,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        type='category',
        tickangle=0,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 4.1],
        tickmode='linear',
        tick0=0,
        dtick=1,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='lightgrey'
    ),
    margin=dict(l=80, r=40, t=50, b=80),
    width=800,
    height=600
)

# Generate output filename from the input JSON path
base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)