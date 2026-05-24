import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and decode the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_path}'.")
    sys.exit(1)

# Extract data and metadata from the JSON structure
data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']
series_names = texts['legend_items']

# Prepare data for Plotly traces
categories = [d['category'] for d in data]

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series in the specified order
for i, series_name in enumerate(series_names):
    y_values = [d[series_name] for d in data]
    fig.add_trace(go.Bar(
        x=categories,
        y=y_values,
        name=series_name,
        marker_color=colors[i],
        text=y_values,
        texttemplate='%{text}',
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=12,
            color='white'
        )
    ))

# Configure the chart layout
fig.update_layout(
    barmode='stack',
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    xaxis=dict(
        tickangle=-45,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 4],
        dtick=1,
        gridcolor='#e9e9e9',
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=150),
    annotations=[
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.35,
            font=dict(size=10, color='#666666')
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file with high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")