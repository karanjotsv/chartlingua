import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for the pie chart
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create custom text labels to match the original chart's annotations
# Note: Replicating the exact annotation style (background box, leader lines, conditional inside/outside placement)
# is complex and can be brittle. This implementation uses standard outside labels for robustness.
custom_text = [f"{item['category']}, {item['value']:,}, {item['percentage']}%" for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    text=custom_text,
    textinfo='none',  # Use the custom text from the 'text' property
    textposition='outside',
    hoverinfo='label+percent+value',
    sort=False,  # Preserve the order from the JSON file
    rotation=60  # Adjust rotation to approximate the original layout
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        x=0.95,
        y=0.5,
        xanchor='left',
        yanchor='middle'
    ),
    paper_bgcolor='#FFFFFF',
    plot_bgcolor='#FFFFFF',
    margin=dict(l=40, r=40, t=100, b=40),
    showlegend=True
)

# Update trace properties for text styling
fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    insidetextorientation='radial'
)

# Determine output filename from the input JSON path
output_filename = f"{Path(json_path).stem}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)