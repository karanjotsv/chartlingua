import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Read data from JSON file
json_path = pathlib.Path(sys.argv[1])
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and texts
chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

# Prepare data for Plotly
x_values = [item.get('x') for item in chart_data]
y_values = [item.get('y') for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker=dict(
        color=colors,
        line=dict(color='black', width=1)
    ),
    showlegend=False
))

# Update layout
fig.update_layout(
    title_text=texts.get('title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 60],
        showgrid=True,
        gridcolor='lightgrey'
    ),
    margin=dict(t=80, b=80, l=50, r=30),
    showlegend=False
)

# Generate output filename from JSON path
output_filename = f"{json_path.stem}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except ValueError as e:
    if "requires the kaleido" in str(e):
        print("Error: The 'kaleido' package is required to save static images.", file=sys.stderr)
        print("Please install it using: pip install kaleido", file=sys.stderr)
        sys.exit(1)
    else:
        raise e