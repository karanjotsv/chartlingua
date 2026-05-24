import sys
import json
import pathlib
import math
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and settings from the JSON object
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', {})

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
# Series 1: Scatter plot of data points
scatter_series = data_series[0]
fig.add_trace(go.Scatter(
    x=scatter_series['x'],
    y=scatter_series['y'],
    mode='markers',
    marker=dict(
        color=colors.get('traces', ['#000000'])[0],
        size=5
    ),
    name=scatter_series.get('name', '')
))

# Series 2: Trendline
line_series = data_series[1]
fig.add_trace(go.Scatter(
    x=line_series['x'],
    y=line_series['y'],
    mode='lines',
    line=dict(
        color=colors.get('traces', ['#000000', '#FF0000'])[1],
        width=2
    ),
    name=line_series.get('name', '')
))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(size=20)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1.5,
        linecolor=colors.get('axes'),
        mirror=False,
        showgrid=True,
        gridwidth=1,
        gridcolor=colors.get('grid_vertical'),
        tickvals=[2003, 2004, 2005, 2006, 2007],
        ticktext=['2003', '2004', '2005', '2006', '2007'],
        range=[2002.5, 2007.5],
        ticks='outside',
        minor=dict(
            ticks='outside',
            ticklen=5,
            showgrid=False
        )
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        type='log',
        showline=True,
        linewidth=1.5,
        linecolor=colors.get('axes'),
        mirror=False,
        showgrid=True,
        gridwidth=1,
        gridcolor=colors.get('grid_horizontal'),
        griddash='solid',
        minor=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor=colors.get('grid_horizontal'),
            griddash='dash'
        ),
        tickmode='array',
        tickvals=texts.get('y_axis_labels', {}).get('values'),
        ticktext=texts.get('y_axis_labels', {}).get('texts'),
        range=[math.log10(70000), math.log10(4500000)]
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color=colors.get('axes')
    ),
    margin=dict(l=60, r=40, t=80, b=50)
)

# Define output filename and save the image
output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as '{output_filename}'")