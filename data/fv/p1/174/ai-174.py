import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    rotation=74 # Start the first slice (Others) to align its end at 12 o'clock
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title', ''),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        x=0.85,
        y=0.65,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=40, r=40, t=80, b=40),
    showlegend=True,
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON path
filename_base = Path(json_file_path).stem
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")