import sys
import json
import os
import plotly.graph_objects as go

# This script requires a single command-line argument: the path to the JSON file.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data and configuration from the specified JSON file.
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON.
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', {})
series_colors = colors.get('series', [])
background_color = colors.get('background', 'white')

labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

# Initialize a Plotly figure.
fig = go.Figure()

# Add the pie chart trace.
# The `sort=False` argument is crucial to maintain the original data order from the JSON file.
# `domain` is used to position the pie chart on the left side of the layout.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=series_colors, line=dict(color=background_color, width=2)),
    hole=0,
    sort=False,
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent',
    domain={'x': [0.0, 0.7], 'y': [0.05, 0.95]}
))

# Update the layout of the figure.
# This section sets the title, legend, fonts, colors, and margins.
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.05,
        xanchor='left',
        yanchor='top'
    ),
    title_font=dict(
        family="Arial",
        size=40,
        color='white'
    ),
    font=dict(
        family="Arial",
        size=18,
        color='white'
    ),
    showlegend=True,
    legend=dict(
        title=texts.get('legend_title'),
        x=0.65,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(0,0,0,0)', # Transparent background for the legend
        bordercolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial",
            size=18,
            color='white'
        ),
        title_font=dict(
            family="Arial",
            size=18,
            color='white'
        )
    ),
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    margin=dict(l=20, r=20, t=120, b=20)
)

# Determine the output filename from the input JSON path.
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure to a PNG file with a high resolution.
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")