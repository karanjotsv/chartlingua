import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create a new figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x_values'),
        y=series.get('y_values'),
        mode='lines',
        name=series.get('series_name', ''),
        line=dict(color=colors[i % len(colors)], width=4)
    ))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center',
        font=dict(size=18)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black',
        ticks='outside',
        tickvals=chart_data[0].get('x_values') # Ensure all x-axis labels are shown
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[3, 4],
        tickvals=[3, 3.25, 3.5, 3.75, 4],
        gridcolor='#e0e0e0',
        linecolor='black',
        ticks='outside'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=40, t=100, b=80)
)

# Determine output filename from JSON path
if '.' in json_path:
    base_filename = json_path.rsplit('.', 1)[0]
else:
    base_filename = json_path
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")