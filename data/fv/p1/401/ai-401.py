import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_path = pathlib.Path(sys.argv[1])

# Verify the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load the chart data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and texts from the configuration
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create custom text for each slice to match the original chart's format
# Note: Replicating the exact leader-line layout for small slices is complex in Plotly.
# Placing all labels inside the slices is a robust and clear alternative.
pie_text = [f"{item['label']}<br>{item['value']}%" for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    hoverinfo='label+percent',
    text=pie_text,
    textinfo='text',
    textposition='inside',
    sort=False,  # This is crucial to preserve the order from the JSON file
    direction='clockwise'
))

# Update the layout for a clean and accurate presentation
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=24)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(t=100, b=50, l=50, r=50),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Set the font for the text inside the pie slices
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=11,
        color='black'
    ),
    insidetextorientation='horizontal'
)

# Generate the output filename from the input JSON filename
output_filename = json_path.stem + ".png"

# Save the figure to a PNG file with high resolution
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to '{output_filename}'")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)