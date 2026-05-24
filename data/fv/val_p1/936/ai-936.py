import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

# Extract data for plotting
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])
text_colors = chart_data.get('text_colors', [])

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart trace
# Using textposition='auto' lets Plotly decide whether to place text inside or outside
# Using textfont_color allows specifying individual colors for labels
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,
    direction='clockwise',
    textinfo='label',
    textposition='auto',
    textfont=dict(
        family="Arial",
        size=16,
        color=text_colors
    ),
    insidetextorientation='horizontal',
    hoverinfo='label+percent'
)])

# Update layout
fig.update_layout(
    showlegend=False,
    margin=dict(l=40, r=40, t=40, b=60),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial")
)

# Add source annotation if it exists
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=0,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=12)
    )

# Determine output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")