import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Derive output filename from JSON path
if json_path.endswith('.json'):
    output_filename = json_path[:-5] + '.png'
else:
    output_filename = json_path + '.png'

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])

# Create the figure
fig = go.Figure()

# Add a trace for each series
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['values'],
        y=categories,
        orientation='h',
        marker=dict(color=colors[i % len(colors)]),
        text=series['values'],
        texttemplate='%{x}',
        textposition='outside',
        textfont=dict(size=10, color='black')
    ))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(size=24)
    ),
    barmode='group',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[0, 6],
        showgrid=True,
        gridcolor='#d9d9d9'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        # The table in the original image lists Series 3, 2, 1.
        # Plotly adds traces in order 1, 2, 3, so we reverse the legend order.
        traceorder='reversed'
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='#f0f0f0',
    paper_bgcolor='#f0f0f0',
    margin=dict(l=120, r=40, t=100, b=120),
    bargap=0.2,
    bargroupgap=0.1
)

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")