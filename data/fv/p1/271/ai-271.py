import sys
import json
import plotly.graph_objects as go
import os

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Derive the output filename base from the JSON path
output_filename_base = os.path.splitext(os.path.basename(json_path))[0]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data for the chart
data = chart_info['chart_data']
labels = [item['label'] for item in data]
values = [item['value'] for item in data]
colors = chart_info['colors']

# Create labels for the legend that mimic the original chart's format
# The original displays labels and percentages next to the chart, not on the slices.
# A formatted legend is the most robust way to replicate this in Plotly.
legend_labels = [f"{item['label']}<br>{item['value']}%" for item in data]

# Create the pie chart trace
# Note: Plotly does not support 3D pie charts.
# An exploded 2D donut chart is used as the closest representation.
pie_trace = go.Pie(
    labels=legend_labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    pull=[0.05] * len(values),  # Explode all slices slightly
    hole=0.2,                   # Create a hole to mimic the 3D visual gap
    sort=False,                 # Preserve the original data order
    direction='clockwise',
    textinfo='none',            # Hide text on the pie slices themselves
    hoverinfo='label+percent',
    showlegend=True
)

fig = go.Figure(data=[pie_trace])

# Update layout for a clean and accurate presentation
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=40, r=220, t=40, b=40), # Add right margin for legend
    paper_bgcolor='white',
    plot_bgcolor='white',
    legend=dict(
        x=1.05,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        traceorder='normal',
        bgcolor='rgba(0,0,0,0)', # Transparent background for the legend box
        bordercolor='rgba(0,0,0,0)'
    )
)

# Save the figure as a high-resolution PNG file
output_image_path = f"{output_filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")