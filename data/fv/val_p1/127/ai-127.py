import sys
import json
import plotly.graph_objects as go
import pathlib

# This script must be run from the command line with the JSON file path as an argument.
# Example: python your_script_name.py your_json_file.json

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the output filename from the input JSON filename
output_filename_base = pathlib.Path(json_path).stem
output_image_path = f"{output_filename_base}.png"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=1)
    ),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    domain=dict(x=[0, 0.6]) # Allocate left 60% of the area for the pie
))

# Update layout for a professional look, matching the original
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=18, weight="bold")
    ),
    legend=dict(
        x=0.62,  # Position legend in the space created by the domain
        y=0.9,
        xanchor='left',
        yanchor='top',
        traceorder='normal',
        font=dict(family="Arial", size=12),
        bgcolor='rgba(0,0,0,0)' # Transparent background
    ),
    font=dict(family="Arial", size=12),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=80, b=20)
)

# Write the image to a file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")