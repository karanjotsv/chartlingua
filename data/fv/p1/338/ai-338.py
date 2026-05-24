import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}", file=sys.stderr)
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Prepare data for the pie chart trace
labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1.5)),
    textposition='inside',
    textinfo='label',
    insidetextfont=dict(family='Arial', size=14, color='black'),
    hoverinfo='label+percent',
    sort=False  # This is crucial to preserve the original data order
)

# Create the figure object
fig = go.Figure(data=[pie_trace])

# Apply layout settings from the JSON
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_y=0.05,
    title_font=dict(family='Arial', size=16, color='black', weight='bold'),
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    annotations=texts.get('annotations'),
    margin=dict(l=20, r=20, t=30, b=80)
)

# Generate the output filename and save the image
output_filename_base = Path(json_file_path).stem
output_png_path = f"{output_filename_base}.png"

try:
    fig.write_image(output_png_path, scale=2)
except Exception as e:
    print(f"Error writing image file: {e}", file=sys.stderr)
    sys.exit(1)