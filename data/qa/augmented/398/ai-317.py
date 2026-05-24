import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load the chart data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for plotting
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Format text labels for data points with space as thousand separator
text_labels = [f'{y:,}'.replace(',', ' ') for y in y_values]

# Create the figure object
fig = go.Figure()

# Add the line trace to the figure
fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2),
    marker=dict(color=colors[0], size=6),
    text=text_labels,
    textposition='top center',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='none' # Hides the default hover label
))

# Update the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12, color='#333333'),
    title=texts.get('title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
    xaxis=dict(
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        range=[0, 150000],
        tickvals=[0, 25000, 50000, 75000, 100000, 125000, 150000],
        ticktext=['0', '25 000', '50 000', '75 000', '100 000', '125 000', '150 000']
    )
)

# Add source annotation if it exists
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=1, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=12)
    )

# Determine the output filename and save the chart as a PNG image
output_filename = json_file_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")