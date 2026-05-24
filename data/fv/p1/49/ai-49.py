import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
x_category = [chart_data['x_category']] # Plotly expects a list for axes

# Create a new figure
fig = go.Figure()

# Add a bar trace for each series in the data
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=x_category,
        y=[series['y_value']],
        name=series['name'],
        marker_color=colors[i]
    ))

# Update the layout of the chart
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    font_family="Arial",
    xaxis_title_text=texts['x_axis_title'],
    yaxis_title_text=texts['y_axis_title'],
    plot_bgcolor='white',
    barmode='group',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        tickvals=x_category # Ensures the category label is displayed
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgrey',
        range=[0, 50],
        dtick=5,
        showline=False
    ),
    margin=dict(t=80, b=100, l=40, r=40)
)

# Define the output image file name based on the JSON file name
output_filename = json_file_path.with_suffix(".png")

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")