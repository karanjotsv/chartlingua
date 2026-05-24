import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if a command-line argument is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the JSON object
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in data_series]
values = [item['value'] for item in data_series]

# Assign colors to non-zero bars, otherwise use a transparent color
marker_colors = []
color_iterator = iter(colors)
for value in values:
    if value > 0:
        try:
            marker_colors.append(next(color_iterator))
        except StopIteration:
            # Fallback color if not enough colors are provided
            marker_colors.append('#CCCCCC')
    else:
        marker_colors.append('rgba(0,0,0,0)')

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=marker_colors,
    hoverinfo='none'
))

# Create annotations for the bar values
annotations = []
for i, item in enumerate(data_series):
    if item.get('annotation'):
        annotations.append(
            go.layout.Annotation(
                x=categories[i],
                y=item['value'],
                text=item['annotation'],
                showarrow=False,
                xanchor='center',
                yanchor='bottom',
                yshift=5,
                font=dict(family="Arial", size=11, color="#555555"),
                bgcolor='rgba(240, 240, 240, 0.8)',
                borderpad=2
            )
        )

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=16)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 5],
        tickvals=[0, 1, 2, 3, 4, 5],
        showgrid=True,
        gridcolor='#E0E0E0',
        showline=True,
        linecolor='black'
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=50, r=20, t=100, b=120),
    annotations=annotations
)

# Add a horizontal line below the title
fig.add_shape(
    type="line",
    xref="paper", yref="paper",
    x0=0, y0=0.91, x1=1, y1=0.91,
    line=dict(color="black", width=1)
)

# Generate the output image file path
output_filename = json_file_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")