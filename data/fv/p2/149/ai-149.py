import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the base filename for the output image from the JSON path
# e.g., /path/to/my_chart.json -> my_chart
base_filename = json_path.split('/')[-1].split('\\')[-1].replace('.json', '')
output_image_path = f"{base_filename}.png"

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
series_colors = chart_info.get("colors", [])
background_color = chart_info.get("background_color", "#FFFFFF")

# Prepare data in the format Plotly expects
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
# Note: The original chart has a 3D extruded effect which is not a standard
# feature in Plotly. This script creates a 2D pie chart, which is the
# closest representation possible with the library.
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=series_colors,
        line=dict(color='black', width=2)
    ),
    textfont=dict(
        family="Arial",
        size=24,
        color='white'
    ),
    textinfo='text',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=30,  # Rotates the chart to position the "Ind" slice at the top
    pull=[0.02, 0.02, 0.02] # Creates slight separation between slices
)

# Create the figure and add the trace
fig = go.Figure(data=[pie_trace])

# Update the layout for a clean and accurate appearance
fig.update_layout(
    showlegend=False,
    paper_bgcolor=background_color,
    plot_bgcolor=background_color,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    annotations=[
        dict(
            text=texts.get('title', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.05,
            font=dict(
                family="Arial",
                size=16,
                color="black"
            )
        )
    ],
    margin=dict(l=20, r=20, t=20, b=80) # Add bottom margin for the title
)

# Write the image to a file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")