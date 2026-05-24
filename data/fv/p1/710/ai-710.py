import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- Script Execution ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = Path(json_path_str)

# Ensure the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path_str}'")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- Data Extraction ---
labels = [item['label'] for item in chart_data['chart_data']]
values = [item['value'] for item in chart_data['chart_data']]
colors = chart_data['colors']
texts = chart_data['texts']

# --- Chart Creation ---
fig = go.Figure()

# Add Pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    textinfo='label',
    textposition='outside',
    sort=False,
    direction='clockwise',
    rotation=215  # Adjusts start position to match the original image
))

# --- Layout Configuration ---
fig.update_layout(
    title=dict(
        text=texts['title'] if texts['title'] else '',
        x=0.5,
        xanchor='center',
        font=dict(
            family="Arial",
            size=22,
            color='black'
        )
    ),
    font=dict(
        family="Arial",
        size=12,
        color='#555555'  # Set default font color for labels
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=100, b=80) # Add margin for outside labels
)

# --- Output Generation ---
output_filename = json_path.stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")