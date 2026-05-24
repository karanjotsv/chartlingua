import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    texttemplate='%{text:.2f}',
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Update layout for a professional appearance
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 5],
        gridcolor='#d9d9d9',
        zeroline=False,
        showline=False,
        ticks='outside'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        type='category',
        showline=True,
        linecolor='black',
        gridcolor='#f0f0f0' # Faint vertical separators
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=[
        # Note annotation
        dict(
            text=texts.get('note'),
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.28,
            xanchor='left', yanchor='bottom',
            align='left',
            font=dict(size=12, color='#0073bb')
        ),
        # Source annotation
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.28,
            xanchor='right', yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)