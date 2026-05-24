import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])

# Ensure the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for the chart
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly
labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=2)),
    textinfo='none', # Remove default textinfo to use a custom template
    hovertemplate='%{label}: %{value}%<extra></extra>',
    texttemplate='%{label} %{value}%',
    textposition='outside',
    sort=False,
    direction='counterclockwise'
)])

# Update the layout for a clean and accurate appearance
fig.update_layout(
    showlegend=False,
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=50, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            x=0.95,
            y=-0.1,
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12, color='#666666')
        )
    ]
)

# Define the output filename based on the input JSON file's base name
output_filename = json_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")