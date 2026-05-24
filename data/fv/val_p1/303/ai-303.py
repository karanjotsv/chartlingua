import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
input_path = Path(json_file_path)

# Ensure the JSON file exists
if not input_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# Extract data for the chart
chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

# Prepare data for Plotly Pie trace
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# The original chart displays custom labels with values and line breaks outside the slices.
# We create these custom labels and configure the trace to display them.
custom_text_labels = [f"{item['label']}<br>{item['value']}%" for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the Pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    # Use the 'text' property for our custom-formatted labels
    text=custom_text_labels,
    # 'textinfo' is set to 'text' to display the content of the 'text' property
    textinfo='text',
    textposition='outside',
    # Attempt to match the visual rotation of the original chart
    rotation=45,
    hoverinfo='none',
    showlegend=True,
    sort=False # Preserve the original data order
))

# Update the layout for a clean and accurate presentation
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    # Adjust margins to prevent labels or the legend from being cut off
    margin=dict(l=100, r=200, t=50, b=50),
    legend=dict(
        x=1.05,
        y=0.9,
        xanchor='left',
        yanchor='top',
        traceorder='normal',
        bordercolor='black',
        borderwidth=1
    )
)

# Generate the output PNG filename from the input JSON filename
output_filename = input_path.stem + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")