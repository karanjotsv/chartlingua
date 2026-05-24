import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_filepath = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_filepath}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Prepare data lists
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    text=y_values,
    textposition='outside',
    cliponaxis=False,  # Ensures text labels are not clipped by plot area
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Update layout
title_text = texts.get('title')
y_axis_title = texts.get('y_axis_title')
source_text = texts.get('source')

fig.update_layout(
    title_text=title_text,
    yaxis_title=y_axis_title,
    xaxis_title=texts.get('x_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=90),
    xaxis=dict(
        tickfont=dict(size=12),
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        range=[0, 85],
        gridcolor='#EAEAEA',
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.22,
            xanchor="right",
            yanchor="top",
            font=dict(size=10)
        )
    ]
)

# Generate output filename from input JSON path
output_filename = json_filepath.rsplit('.', 1)[0] + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")