import sys
import json
import plotly.graph_objects as go
import pathlib

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data from the file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{json_path}'.")
    sys.exit(1)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]
bar_texts = [f"{v}%" for v in values]

# Create the bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=bar_texts,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    hoverinfo='none'
))

# Update layout to match the original image
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        type='category',
        showgrid=False,
        showline=True,
        linecolor='#D3D3D3'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showticklabels=False,
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False,
        range=[0, max(values) * 1.15] # Add padding for top labels
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=texts['additional_info'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            font=dict(color='#007bff') # Use a blue color to indicate a link
        ),
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2
        )
    ]
)

# Determine the output filename from the input JSON path
output_filename_base = pathlib.Path(json_path).stem
output_png_path = f"{output_filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_png_path, scale=2)

print(f"Chart saved as {output_png_path}")