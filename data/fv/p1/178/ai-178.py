import sys
import json
import plotly.graph_objects as go
import os

# Ensure a command-line argument is provided for the JSON file path
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the base filename for the output PNG from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Load chart data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Prepare data for the plot from the JSON configuration
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Create combined labels for the legend as seen in the original chart
labels_for_legend = [f"{item['label']} {item['value']}%" for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels_for_legend,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='darkgrey', width=1)  # Thin line around slices
    ),
    sort=False,  # Preserve the original data order
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent'
))

# Configure the layout of the chart to match the original image
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        y=0.95,
        font=dict(family="Arial", size=24, weight='bold', color='black')
    ),
    font=dict(family="Arial", size=14, color='black'),
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.7,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)'  # Transparent legend background
    ),
    margin=dict(l=30, r=30, t=100, b=30),
    paper_bgcolor='white'
)

# Add a grey border around the entire plot area to replicate the source image
fig.add_shape(
    type="rect",
    xref="paper", yref="paper",
    x0=0, y0=0, x1=1, y1=1,
    line=dict(color="darkgrey", width=2)
)

# Write the generated chart to a high-resolution PNG file
fig.write_image(output_filename, scale=2)