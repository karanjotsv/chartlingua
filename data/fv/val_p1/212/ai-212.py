import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get file paths
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data for plotting
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['category'] for item in data]
values = [item['value'] for item in data]
text_labels = [item['text_label'] for item in data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=text_labels,
    textinfo='text',
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=4)
    ),
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    hoverinfo='label+percent+value',
    textposition='auto',
    insidetextfont=dict(family="Arial", color='white', size=14),
    outsidetextfont=dict(family="Arial", color='black', size=12),
    pull=[0.015] * len(values) # Slight separation between slices
))

# Update layout
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top',
        font=dict(
            family="Arial",
            size=24,
            color='black'
        )
    ),
    font=dict(
        family="Arial",
        color='black'
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=120, b=40, l=40, r=40)
)

# Save the figure as a PNG image
try:
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)