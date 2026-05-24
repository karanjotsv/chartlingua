import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]

# Read the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from the JSON structure
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart trace
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    sort=False,
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent'
))

# Update the layout
fig.update_layout(
    showlegend=True,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='white',
    margin=dict(l=20, r=20, t=50, b=220),
    legend=dict(
        x=1.02,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.5)'
    ),
    annotations=[
        dict(
            text=texts.get('source_note_left', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,
            xanchor='left',
            yanchor='top',
            align='left'
        ),
        dict(
            text=texts.get('source_note_right', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.6,
            y=-0.1,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ]
)

# Determine the output filename and save the image
output_path = Path(json_file_path).with_suffix('.png')
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")