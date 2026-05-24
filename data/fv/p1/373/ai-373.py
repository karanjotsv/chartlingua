import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get file path from command-line argument
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- Prepare data for Plotly ---
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# --- Create the chart ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    marker=dict(colors=colors['slices']),
    text=texts['data_labels'],
    textinfo='text',
    textfont=dict(
        family="Arial",
        size=28,
        color=colors['text']
    ),
    hoverinfo='skip',
    sort=False,
    direction='clockwise',
    rotation=125
))

# --- Update layout ---
fig.update_layout(
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    margin=dict(t=20, b=20, l=20, r=20),
    font=dict(
        family="Arial"
    )
)

# --- Output the image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")