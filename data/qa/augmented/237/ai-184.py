import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Read the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data and texts
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else '#3182CE',
    text=[f"{y:.1f}" for y in y_values],
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='black'),
    cliponaxis=False
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 12.5],
        tickvals=[0, 2, 4, 6, 8, 10, 12],
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    showlegend=False,
    margin=dict(l=80, r=20, t=30, b=100),
    annotations=[
        dict(
            text=texts.get('note'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='bottom',
            font=dict(family="Arial", size=12, color='#0073e5')
        ),
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=12, color='grey')
        )
    ]
)

# Derive output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")