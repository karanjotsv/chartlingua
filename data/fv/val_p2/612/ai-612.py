import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and settings from the JSON object
chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
categories = chart_data.get('categories', [])
series_data = chart_data.get('series', [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each series
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        name=series.get('name'),
        x=categories,
        y=series.get('y'),
        marker_color=colors[i % len(colors)] if colors else None,
        text=[f'{val:.2%}' for val in series.get('y', [])],
        textposition='outside',
        textfont=dict(family='Arial', size=10, color='black'),
        marker_line_width=1.5,
        marker_line_color='black'
    ))

# Update layout to match the original chart
fig.update_layout(
    barmode='group',
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family='Arial', size=16, color='black')
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(family='Arial', size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        tickformat='.0%',
        range=[0, 0.8],
        gridcolor='#C0C0C0',
        tickfont=dict(family='Arial', size=12)
    ),
    legend=dict(
        x=0.98,
        y=0.8,
        xanchor='right',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1,
        font=dict(family='Arial', size=10)
    ),
    plot_bgcolor='#DCDCDC',
    paper_bgcolor='white',
    font=dict(family='Arial'),
    margin=dict(t=80, b=50, l=60, r=40)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")