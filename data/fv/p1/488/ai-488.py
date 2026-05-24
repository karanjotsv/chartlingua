import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_filepath = pathlib.Path(sys.argv[1])

# Check if the provided JSON file exists
if not json_filepath.is_file():
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_filepath, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', {})
water_area = chart_info.get('water_area', {})
texts = chart_info.get('texts', {})

# Initialize the figure
fig = go.Figure()

# Add the bar chart trace with individual bar colors
fig.add_trace(go.Bar(
    x=chart_data.get('x_values'),
    y=chart_data.get('y_values'),
    marker_color=chart_data.get('bar_colors'),
    showlegend=False
))

# Add the water area as a background shape
if water_area:
    fig.add_shape(
        type="rect",
        xref="x",
        yref="y",
        x0=water_area.get('x_start_index') - 0.5,
        x1=water_area.get('x_end_index') + 0.5,
        y0=0,
        y1=water_area.get('y_level'),
        fillcolor=water_area.get('color'),
        line_width=0,
        layer='below'
    )

# Configure the layout of the chart
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text = f"{title_text}<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=50, r=20, t=40, b=40),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1.5,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        range=[0, 9],
        dtick=1
    )
)

# Add source/note annotation if present
if texts.get('source'):
    fig.add_annotation(
        text=texts.get('source'),
        xref="paper", yref="paper",
        x=0, y=-0.1,
        showarrow=False,
        xanchor='left',
        yanchor='top',
        align='left',
        font=dict(size=12)
    )

# Define the output filename based on the input JSON filename
output_filename = json_filepath.stem + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")