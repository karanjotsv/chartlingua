import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Create a figure with subplots for the two pie charts
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'domain'}, {'type': 'domain'}]],
    subplot_titles=[d.get('title') for d in data]
)

# Add the first pie chart
if len(data) > 0:
    fig.add_trace(go.Pie(
        labels=data[0]['labels'],
        values=data[0]['values'],
        name=data[0]['title'],
        marker_colors=colors,
        textinfo='none',
        hoverinfo='label+percent',
        sort=False
    ), 1, 1)

# Add the second pie chart
if len(data) > 1:
    fig.add_trace(go.Pie(
        labels=data[1]['labels'],
        values=data[1]['values'],
        name=data[1]['title'],
        marker_colors=colors,
        textinfo='none',
        hoverinfo='label+percent',
        sort=False
    ), 1, 2)

# Update layout for a professional look, ensuring no elements are clipped
fig.update_layout(
    font_family="Arial",
    margin=dict(l=20, r=20, t=80, b=20),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=1.05,
        font=dict(size=10)
    ),
    annotations=[
        dict(
            font=dict(size=14),
            showarrow=False,
            x=0.20,
            y=1.08,
            xref="paper",
            yref="paper"
        ),
        dict(
            font=dict(size=14),
            showarrow=False,
            x=0.80,
            y=1.08,
            xref="paper",
            yref="paper"
        )
    ]
)

# Generate the output filename from the input JSON path
base_filename = json_path.rsplit('.', 1)[0]
output_image_path = f"{base_filename}.png"

# Save the figure to a PNG file and print a confirmation
fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")