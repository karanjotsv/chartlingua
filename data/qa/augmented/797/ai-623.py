import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

# Extract data and texts
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for plotting
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the line trace
fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers',
    line=dict(color=colors[0] if colors else None, width=3),
    marker=dict(color=colors[0] if colors else None, size=6),
    name='' # No legend entry
))

# Update layout
fig.update_layout(
    title_text=texts.get('title'),
    font=dict(family="Arial", size=12),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        range=[0, 2500],
        dtick=250,
        tickfont=dict(size=12),
        tickformat=','
    ),
    margin=dict(l=100, r=40, t=50, b=100)
)

# Add annotations for source and note
annotations = []
if texts.get('note'):
    annotations.append(dict(
        xref="paper", yref="paper",
        x=0, y=-0.2,
        xanchor='left', yanchor='top',
        text=texts['note'],
        showarrow=False,
        font=dict(family="Arial", size=12, color="#000000")
    ))
if texts.get('source'):
    annotations.append(dict(
        xref="paper", yref="paper",
        x=1, y=-0.2,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color="#000000")
    ))

fig.update_layout(annotations=annotations)

# Determine output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_image_filename, scale=2)

print(f"Chart saved to {output_image_filename}")