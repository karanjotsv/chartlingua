import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# This script is designed to be self-contained and free of external dependencies
# beyond the standard ones required for this task (sys, json, plotly).
# It avoids creating functions or classes to keep the execution flow linear and simple.

# --- 1. Argument and File Handling ---
# The script requires a single command-line argument: the path to the JSON file.
# This approach makes the script flexible and reusable for different data sets.
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# The output PNG filename is derived directly from the input JSON filename.
output_filename = json_file_path.with_suffix('.png')

# Load the chart data and configuration from the specified JSON file.
# This is the sole source of data and text for the chart.
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# --- 2. Data Extraction ---
# All data, text, and styling information are extracted from the loaded JSON object.
# This ensures that the script is entirely data-driven.
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
chart_title = texts.get('title', '')

# Prepare data for Plotly's pie chart trace.
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Chart Recreation ---
# A 2D pie chart is used as Plotly does not natively support 3D pie charts.
# This provides a clear and accurate representation of the data proportions.
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.0,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)  # Emulates separation between slices
    ),
    # Sort is disabled to preserve the order from the JSON file.
    sort=False,
    # Direction is set to match the visual flow of many standard charts.
    direction='clockwise',
    # Text with both label and percentage is placed outside the slices.
    # While the original has callout lines, this is a robust Plotly-native alternative.
    textinfo='percent+label',
    textposition='outside',
    hoverinfo='label+percent',
    # The 'pull' parameter slightly separates slices for emphasis, mimicking the original.
    pull=[0, 0.05, 0.05, 0]
))

# --- 4. Layout and Styling ---
# The layout is carefully configured to match the original's aesthetics and
# ensure readability, using "Arial" as the universal font family.
fig.update_layout(
    title=dict(
        text=chart_title,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=20)
    ),
    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="black"
    ),
    # The legend is included as in the original, placed horizontally at the bottom.
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    # Margins are set to prevent the title, labels, or legend from being cut off.
    margin=dict(t=100, b=100, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# --- 5. Image Export ---
# The final chart is exported to a high-resolution PNG file.
# The 'scale' parameter increases the resolution for better quality.
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")