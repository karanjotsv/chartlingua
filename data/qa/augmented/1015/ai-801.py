import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from {json_file_path}.")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Create the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data['series']):
    # Format text labels to remove trailing .0 for integers
    text_labels = [f'{v:g}%' for v in series['values']]

    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['values'],
        name=series['name'],
        marker_color=colors[i % len(colors)],
        text=text_labels,
        textposition='outside',
        textfont=dict(
            family="Arial, bold",
            size=12,
            color='black'
        ),
        cliponaxis=False
    ))

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts['xaxis_title'],
        showgrid=False,
        linecolor='lightgrey',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts['yaxis_title'],
        range=[0, 60],
        tickvals=[0, 10, 20, 30, 40, 50, 60],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        zeroline=False,
        linecolor='lightgrey',
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            text=texts['additional_info'],
            showarrow=False,
            font=dict(family="Arial", size=12, color=colors[0])
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='#666666')
        )
    ]
)

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")