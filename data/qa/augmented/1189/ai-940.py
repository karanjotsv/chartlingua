import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Verify the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read the JSON data
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
# Reverse the data to display the highest value at the top
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
categories.reverse()
values.reverse()

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False # Allows text to be drawn outside the plot area
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=texts.get('title') if texts.get('title') else '',
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False,
        showticklabels=True
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=True
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=150, r=50, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='#666666')
        )
    ]
)

# Adjust x-axis range to prevent text clipping
fig.update_xaxes(range=[0, max(values) * 1.15])


# Define the output filename based on the input JSON filename
output_filename = json_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")