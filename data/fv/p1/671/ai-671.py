import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create subplots
fig = make_subplots(
    rows=2,
    cols=1,
    subplot_titles=(texts.get('subplot1_title'), texts.get('subplot2_title'))
)

# Add traces to the subplots
color_index = 0
for i, subplot_spec in enumerate(chart_data):
    row = i + 1
    for series in subplot_spec['series']:
        fig.add_trace(
            go.Scatter(
                x=subplot_spec['x_values'],
                y=series['y_values'],
                name=series['name'],
                mode='lines',
                line=dict(color=colors[color_index])
            ),
            row=row,
            col=1
        )
        color_index += 1

# Update layout and axes for a clean and accurate look
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    height=600,
    width=800,
    margin=dict(l=80, r=40, t=80, b=80),
    showlegend=True,
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.7)',
        bordercolor='black',
        borderwidth=1
    )
)

# Style subplot 1
fig.update_xaxes(
    title_text=texts.get('subplot1_xlabel'),
    row=1, col=1,
    showline=True, linewidth=1, linecolor='black', mirror=True,
    ticks='outside', showgrid=True, gridcolor='lightgray'
)
fig.update_yaxes(
    title_text=texts.get('subplot1_ylabel'),
    row=1, col=1,
    showline=True, linewidth=1, linecolor='black', mirror=True,
    ticks='outside', showgrid=True, gridcolor='lightgray'
)

# Style subplot 2
fig.update_xaxes(
    title_text=texts.get('subplot2_xlabel'),
    row=2, col=1,
    showline=True, linewidth=1, linecolor='black', mirror=True,
    ticks='outside', showgrid=True, gridcolor='lightgray'
)
fig.update_yaxes(
    title_text=texts.get('subplot2_ylabel'),
    row=2, col=1,
    showline=True, linewidth=1, linecolor='black', mirror=True,
    ticks='outside', showgrid=True, gridcolor='lightgray'
)

# In Plotly, legend items are global. Hide the legend for the first trace.
fig.data[0].showlegend = False

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart generated and saved as {output_image_path}")