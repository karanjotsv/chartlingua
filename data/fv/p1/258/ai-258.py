import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data for the chart
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    rotation=150  # Start position of the first slice
))

# Update the layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center',
        font=dict(
            family="Arial",
            size=20,
            color="#A52A2A"
        )
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        font=dict(
            family="Arial",
            size=10
        )
    ),
    font=dict(
        family="Arial"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=40, r=40, t=80, b=150) # Increased bottom margin for legend
)

# Define the output filename from the input JSON filename
output_filename = json_file_path.stem + '.png'

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")