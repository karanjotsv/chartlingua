import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0] if colors else '#297ab0'),
    text=text_labels,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False,
    hoverinfo='none'
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticks='outside',
        tickvals=[0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000],
        ticktext=['0', '250', '500', '750', '1 000', '1 250', '1 500', '1 750', '2 000'],
        range=[0, max(values) * 1.15] # Extend range to avoid text clipping
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # This ensures the order from the JSON is preserved top-to-bottom
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    margin=dict(l=150, r=20, t=30, b=80),
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
            font=dict(family="Arial", size=12)
        )
    ]
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")