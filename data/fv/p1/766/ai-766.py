import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
    
# Derive the output filename from the JSON filename
output_filename = json_path.with_suffix(".png").name

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON file at {json_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = config['chart_data'][0]
colors = config['colors']
texts = config['texts']

# Create the figure object
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=chart_data['labels'],
    values=chart_data['values'],
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1.5)
    ),
    textinfo='percent',
    textfont=dict(
        family="Arial",
        size=18,
        color='black'
    ),
    hoverinfo='none',
    sort=False,
    direction='clockwise',
    rotation=92
))

# Update the layout of the figure
fig.update_layout(
    title_text=None,
    font=dict(
        family="Arial"
    ),
    showlegend=True,
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    plot_bgcolor='black',
    paper_bgcolor='black',
    margin=dict(l=40, r=40, t=40, b=40),
    width=800,
    height=600
)

# Write the figure to a PNG image file
try:
    fig.write_image(output_filename, scale=2)
except ValueError as e:
    # This block can catch errors if kaleido is not installed
    print(f"Error writing image file: {e}")
    print("Please ensure you have the 'kaleido' package installed (`pip install kaleido`)")
    sys.exit(1)

print(f"Chart saved to {output_filename}")