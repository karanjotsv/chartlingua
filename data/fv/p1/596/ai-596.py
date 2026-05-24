import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a command-line argument is provided for the JSON file path
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(sys.argv[0]).name} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Verify that the specified JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load all chart data and text from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data structures from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data series for Plotly from the JSON 'chart_data' list
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
data_labels = [d['label'] for d in chart_data]

# Initialize a Plotly graph objects Figure
fig = go.Figure()

# Add the bar trace using data extracted from the JSON
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=data_labels,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,  # Prevent text labels from being clipped by the plot area
    textfont=dict(
        family="Arial",
        size=10
    )
))

# Construct the title string using HTML for multi-line formatting and styling
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 14px;'>{texts['subtitle']}</span>"

# Update the figure's layout, styling, and annotations
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='lightgrey',
        zeroline=False
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='lightgray',
        range=[0, max(values) * 1.15],  # Add 15% padding to the top for data labels
        tickformat=".0s"  # Format y-axis ticks as 5M, 10M, etc.
    ),
    margin=dict(t=100, r=40, b=80, l=80),
    showlegend=False
)

# Define the output PNG filename based on the input JSON filename stem
output_filename = json_path.with_suffix('.png')

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")