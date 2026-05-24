import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and text elements from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f'{v}%' for v in values],
    textposition='outside',
    cliponaxis=False,  # Prevents text labels from being clipped
    textfont=dict(
        family="Arial",
        size=12
    )
))

# Configure the layout of the chart
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 300],
        tickvals=[0, 50, 100, 150, 200, 250, 300],
        ticksuffix='%',
        gridcolor='#E0E0E0',
        griddash='dot',
        tickfont=dict(size=12),
        title_font=dict(size=14)
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#808080')
        )
    ],
    margin=dict(l=60, r=40, t=40, b=120)  # Adjust bottom margin for source text
)

# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")