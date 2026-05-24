import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])

# Check if the provided path is a valid file
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and texts from the JSON object
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1.5)),
    sort=False,
    direction='clockwise',
    rotation=100,
    textinfo='none',
    hoverinfo='label+percent',
    domain={'x': [0, 0.65], 'y': [0.1, 0.9]} # Allocate space for the legend
))

# Update the layout of the chart
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(size=24)
    ),
    font=dict(
        family="Arial",
        size=16
    ),
    legend=dict(
        x=0.68,
        y=0.8,
        traceorder='normal',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)',
        font=dict(size=16)
    ),
    margin=dict(l=20, r=20, t=80, b=120),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=True,
    annotations=[
        dict(
            text=texts.get('source_left', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.01,
            y=0,
            xanchor='left',
            yanchor='bottom',
            align='left',
            font=dict(size=10)
        ),
        dict(
            text=texts.get('source_right', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=0.02,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Generate the output PNG filename from the input JSON filename
output_filename = json_file_path.stem + ".png"

# Write the figure to a PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")