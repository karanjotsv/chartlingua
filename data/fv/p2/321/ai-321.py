import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(color=colors[i % len(colors)], width=1.5)
    ))

# Update layout
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        linecolor='black',
        linewidth=1,
        mirror=True,
        ticks='outside',
        minor=dict(
            showgrid=True,
            gridcolor='lightgrey',
            griddash='dot'
        )
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        type='log',
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        linecolor='black',
        linewidth=1,
        mirror=True,
        ticks='outside',
        minor=dict(
            showgrid=True,
            gridcolor='lightgrey',
            griddash='dot'
        )
    ),
    legend=dict(
        x=1,
        y=1,
        xanchor='right',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=80, r=20, t=20, b=70)
)

# Generate output filename from input JSON path
if json_file_path.endswith('.json'):
    output_filename = json_file_path[:-5] + '.png'
else:
    output_filename = json_file_path + '.png'


# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")