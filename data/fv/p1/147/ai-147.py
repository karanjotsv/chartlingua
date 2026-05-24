import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the file exists before proceeding
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data for plotting
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
num_series = len(texts['series_names'])
data_series = [[item['values'][i] for item in chart_data] for i in range(num_series)]

# Create the figure
fig = go.Figure()

# Add a bar trace for each series
for i in range(num_series):
    fig.add_trace(go.Bar(
        name=texts['series_names'][i],
        y=categories,
        x=data_series[i],
        orientation='h',
        marker_color=colors[i]
    ))

# Update layout
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_font_family="Arial",
    barmode='group',
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=True,
        gridcolor='lightgrey',
        range=[0, 120],
        dtick=20
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        autorange='reversed',  # To display categories from top to bottom
        showgrid=False
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.15,
        xanchor='center',
        x=0.5
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    # Adjust margin to prevent y-axis labels from being cut off
    margin=dict(l=350, r=30, t=100, b=80),
    autosize=False,
    width=800,
    height=600
)

# Determine output filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")