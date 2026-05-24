import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
background_color = chart_info.get('background_color', '#FFFFFF')

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=0.5)),
    hoverinfo='label+percent',
    textinfo='percent',
    textposition='outside',
    textfont=dict(size=14, family="Arial"),
    sort=False,  # This is crucial to preserve the original order from the JSON
    direction='clockwise',
    rotation=90 # Start the first slice at the top
)])

# Update the layout of the chart
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family="Arial, serif", # Use Arial as primary, but serif as fallback
            size=20
        )
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(
            family="Arial",
            size=12
        )
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    margin=dict(t=100, b=100, l=40, r=40),
    showlegend=True
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")