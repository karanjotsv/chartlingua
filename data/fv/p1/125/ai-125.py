import sys
import json
import pathlib
import plotly.graph_objects as go

# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get JSON file path from the first command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Derive the base filename for the output image from the JSON filename
filename_base = json_file_path.stem

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text elements from the loaded JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure object
fig = go.Figure()

# Add the pie chart trace
# Note: The original chart has a 3D effect which is not a standard feature in Plotly
# and is often avoided for data clarity. This script creates a 2D pie chart, which is
# the standard and clear way to represent this data.
fig.add_trace(go.Pie(
    labels=chart_data['categories'],
    values=chart_data['values'],
    text=chart_data['text_labels'],
    marker_colors=colors,
    sort=False,  # This is crucial to preserve the original data order
    textinfo='text',
    textposition='outside',
    pull=[0.02, 0.02, 0.02, 0.02] # Slightly pull slices for better label visibility
))

# Update the layout of the chart
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=20)
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=True,
    legend=dict(
        traceorder="normal", # Ensures legend order matches the data input order
        x=1,
        y=0.7,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.5)'
    ),
    margin=dict(l=40, r=250, t=100, b=40) # Add right margin to prevent legend clipping
)

# Define the output image file path and save the figure
output_image_path = f"{filename_base}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")