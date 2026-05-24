import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Verify that the specified file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read and parse the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# Extract data, texts, and colors from the JSON structure
data_series = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

# Initialize a new figure
fig = go.Figure()

# Iterate through the data series and add a trace for each one
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=colors[i]),
        connectgaps=False # Ensure gaps for null data points
    ))

# Configure the overall layout of the chart
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='white',
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=80, r=40, t=40, b=80),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,  # Show vertical grid lines
        gridwidth=1,
        gridcolor='lightgray',
        griddash='dot',
        range=[240, 1010]
    ),
    yaxis=dict(
        type='log',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False, # Hide horizontal grid lines as per original
        range=[-4, 3] # Log scale range from 10^-4 to 10^3
    )
)

# Determine the output filename from the input JSON file's base name
output_filename_base = json_file_path.stem
output_png_path = f"{output_filename_base}.png"

# Save the generated figure to a PNG file with a high resolution
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")