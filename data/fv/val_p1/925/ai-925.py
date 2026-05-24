import sys
import json
import plotly.graph_objects as go

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file {json_path}.")
    sys.exit(1)

# Extract data and text from the JSON object
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [item['x'] for item in data]
y_values = [item['y'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    name='' # Use an empty name to prevent it from appearing in hover text as 'trace 0'
))

# Build the title string
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts.get('subtitle')}"

# Update layout
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 24}
    },
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        tickmode='linear',
        showgrid=False,
        linecolor='black',
        linewidth=2,
        ticks='outside'
    ),
    yaxis=dict(
        range=[0, 40000000],
        gridcolor='lightgrey',
        showgrid=True,
        linecolor='black',
        linewidth=2,
        ticks='outside',
        tickformat=',.0f'
    ),
    margin=dict(l=100, r=20, t=100, b=80)
)

# Derive output filename from the input JSON path
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")