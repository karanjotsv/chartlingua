import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_path}'.")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace, ensuring data order is preserved
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#FF0000',
    showlegend=False
))

# Configure the layout to match the original chart
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=16
    ),
    plot_bgcolor='white',
    xaxis=dict(
        type='category',
        showgrid=False,
        showline=True,
        linecolor='black',
        mirror=True,
        ticks='outside',
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        range=[0, 600],
        showgrid=True,
        gridcolor='#dddddd',
        showline=True,
        linecolor='black',
        mirror=True,
        ticks='outside',
        tickfont=dict(size=14)
    ),
    margin=dict(l=90, r=40, t=80, b=80),
    bargap=0.2
)

# Determine the output filename from the input JSON path
if json_path.lower().endswith('.json'):
    output_filename = json_path[:-5] + ".png"
else:
    output_filename = json_path + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")