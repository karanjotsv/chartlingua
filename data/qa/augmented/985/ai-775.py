import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=[f'{y:,}'.replace(',', ' ') for y in y_values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        range=[0, 25000],
        tickvals=[0, 5000, 10000, 15000, 20000, 25000],
        ticktext=['0', '5 000', '10 000', '15 000', '20 000', '25 000'],
        linecolor='black'
    ),
    showlegend=False,
    margin=dict(l=90, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12)
        )
    ]
)

# Determine output filename and save the image
base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")