import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]
path_obj = Path(json_file_path)

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data from the JSON object
data_config = chart_data.get('chart_data', {})
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])
categories = data_config.get('categories', [])
series_data = data_config.get('series', [])

# Create the figure
fig = go.Figure()

# Add a trace for each series
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=categories,
        y=series['data'],
        marker_color=colors[i % len(colors)],
        text=[f"{val}%" for val in series['data']],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False # Allows text to render outside plot area if needed
    ))

# Update layout
fig.update_layout(
    barmode='group',
    font=dict(
        family="Arial",
        size=12
    ),
    xaxis=dict(
        tickfont=dict(size=12),
        showgrid=False,
        zeroline=False,
        title_text=texts.get('x_axis_title')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_font=dict(size=14),
        tickfont=dict(size=12),
        range=[0, 71],
        ticksuffix='%',
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
        font=dict(size=12)
    ),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        dict(
            text=texts.get('source', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.3
        )
    ]
)

# Output the file
output_filename = f"{path_obj.stem}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")