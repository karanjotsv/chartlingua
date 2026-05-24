import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the JSON structure
data = chart_data.get("chart_data", [])
texts = chart_data.get("texts", {})
colors = chart_data.get("colors", [])

labels = [item.get("label") for item in data]
values = [item.get("value") for item in data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=120,
    textinfo='none',
    domain={'x': [0.0, 0.75]}
))

# Update layout
fig.update_layout(
    showlegend=True,
    legend=dict(
        x=0.77,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bordercolor='black',
        borderwidth=1
    ),
    paper_bgcolor='#d3d3d3',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=20, r=20, t=20, b=150)
)

# Add source note as an annotation
source_note = texts.get('source_note')
if source_note:
    fig.add_annotation(
        text=source_note,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.02,
        y=0,
        yanchor='top',
        yshift=-10
    )

# Define output filename and save the image
output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")