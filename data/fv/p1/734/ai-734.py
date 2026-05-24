import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- Prepare data for Plotly ---
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# --- Create the chart ---
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1.5)
    ),
    sort=False,
    direction='clockwise',
    rotation=80,
    hoverinfo='label+percent',
    textinfo='none'
))

# --- Update layout and styling ---
fig.update_layout(
    showlegend=True,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='#D3D3D3',  # Light grey background for the plot area
    paper_bgcolor='white',
    legend=dict(
        x=1.02,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.8)'
    ),
    margin=dict(l=40, r=40, t=40, b=180), # Increased bottom margin for the source note
    autosize=False,
    width=800,
    height=600
)

# Add the combined source note as an annotation
if texts.get('source_note'):
    fig.add_annotation(
        text=texts['source_note'],
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.2, # Position below the chart
        xanchor='left',
        yanchor='top',
        align='left',
        font=dict(
            family="Arial",
            size=10,
            color="black"
        )
    )

# --- Output the chart ---
# Derive the output filename from the input JSON filename
output_filename = json_file_path.with_suffix(".png")

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")