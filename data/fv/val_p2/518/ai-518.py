import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for the chart
labels = [item['label'] for item in chart_data['chart_data']]
values = [item['value'] for item in chart_data['chart_data']]
colors = chart_data['colors']
texts = chart_data['texts']

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # Preserve the original order
    direction='clockwise'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Combine title and source for the bottom caption
# Handle potential null values gracefully
title_text = texts.get('title') or ""
source_text = texts.get('source') or ""
# Add a line break only if both title and source exist
separator = "<br>" if title_text and source_text else ""
full_caption = f"{title_text}{separator}{source_text}"


# Update layout to match the original image
fig.update_layout(
    showlegend=True,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    paper_bgcolor='#D3D3D3',  # Light grey background like the original
    plot_bgcolor='white',
    margin=dict(t=30, b=200, l=50, r=50),  # Ample bottom margin for the caption
    legend=dict(
        x=1,
        y=1,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.7)' # Semi-transparent white background for legend
    ),
    annotations=[
        dict(
            text=full_caption,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=0,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ]
)

# Define the output image file name from the input JSON file name
output_filename = f"{json_file_path.stem}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved to '{output_filename}'")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)