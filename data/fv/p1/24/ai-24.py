import sys
import json
import plotly.graph_objects as go
import os

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']
categories = chart_data['categories']
series = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Add the first series (solid bars with different colors)
trace1_style = colors[0]
fig.add_trace(go.Bar(
    x=categories,
    y=series[0]['data'],
    name=series[0]['name'],
    marker_color=trace1_style['bar_colors'],
    marker_line_color=trace1_style['outline_color'],
    marker_line_width=1
))

# Add the second series (light grey bars with dotted outline)
trace2_style = colors[1]
fig.add_trace(go.Bar(
    x=categories,
    y=series[1]['data'],
    name=series[1]['name'],
    marker_color=trace2_style['fill_color'],
    marker_line_color=trace2_style['outline_color'],
    marker_line_width=2,
    marker_line_dash='dot'
))

# Update the layout to match the original chart's appearance
fig.update_layout(
    barmode='group',
    title_text=texts['title'],
    title_x=0.5,
    title_font_size=16,
    xaxis_title_text=texts['x_axis_title'],
    yaxis_title_text=texts['y_axis_title'],
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='LightGray',
        range=[0, 70],
        tickvals=[0, 10, 20, 30, 40, 50, 60, 70],
        zeroline=False,
        linecolor='black'
    ),
    bargap=0.2,
    bargroupgap=0.1,
    margin=dict(t=80, b=80, l=50, r=30)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")