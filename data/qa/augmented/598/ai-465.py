import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Read the JSON data file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Prepare data for Plotly
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

x_values = [item['x'] for item in data]
y_values = [item['y'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='black'),
    cliponaxis=False # Prevents text labels from being clipped at the top
))

# Update layout
fig.update_layout(
    title_text=texts['title'],
    yaxis_title=texts['y_axis_title'],
    xaxis_title=texts['x_axis_title'],
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=80),
    xaxis=dict(
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black',
        linewidth=1,
        showline=True
    ),
    yaxis=dict(
        range=[0, 16],
        dtick=2.5,
        showgrid=True,
        gridcolor='#e0e0e0',
        linecolor='black',
        zeroline=False
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0.98, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='grey')
        )
    ]
)

# Define output filename and save the image
output_filename = json_file_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")