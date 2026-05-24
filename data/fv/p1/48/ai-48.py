import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    sort=False,  # Preserve original data order
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent',
    domain=dict(x=[0.0, 0.55], y=[0.1, 1.0]) # Position pie on the left
))

# Update layout
fig.update_layout(
    font=dict(
        family="Arial",
        size=12
    ),
    paper_bgcolor='#D3D3D3',
    plot_bgcolor='#D3D3D3',
    showlegend=True,
    legend=dict(
        x=0.57,
        y=1.0,
        xanchor='left',
        yanchor='top'
    ),
    width=1200,
    height=800,
    margin=dict(l=40, r=40, t=50, b=200),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=0.01,
            y=0.01,
            xanchor='left',
            yanchor='bottom',
            align='left'
        )
    ]
)

# Define output filename and save the image
output_filename = json_file_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")