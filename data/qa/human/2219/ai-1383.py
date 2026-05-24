import sys
import json
import pathlib
import plotly.graph_objects as go

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

# The path to the JSON file is taken from the command-line argument.
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load all chart data and configuration from the specified JSON file.
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded configuration.
categories = config['categories']
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize a new figure.
fig = go.Figure()

# Iterate through the data series in the JSON to create a bar trace for each.
# The order of series is preserved from the JSON file.
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        texttemplate='%{y}%',
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False
    ))

# Configure the layout of the chart meticulously.
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    title_text=texts['title'],
    xaxis=dict(
        categoryorder='array',
        categoryarray=categories,
        title_text=texts['x_axis_title'],
        showline=True,
        linewidth=1.5,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 65],
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        showline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    # Adjust margins to prevent titles, labels, or the source text from being clipped.
    margin=dict(l=80, r=40, t=50, b=120),
    # Add annotations for elements like the source line.
    annotations=[
        dict(
            showarrow=False,
            xref='paper', yref='paper',
            x=0.99, y=-0.4,
            xanchor='right', yanchor='bottom',
            text=texts['source'],
            font=dict(family="Arial", size=11, color='#666666')
        )
    ]
)

# The output filename is derived from the input JSON filename.
output_filename = json_path.stem + '.png'

# Save the figure as a high-resolution PNG image.
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")