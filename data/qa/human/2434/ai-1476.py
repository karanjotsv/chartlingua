import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{json_path}'.")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    texttemplate='%{label} %{value}%',
    textposition='outside',
    sort=False,  # This is crucial to preserve the original order
    hoverinfo='label+percent',
    direction='counterclockwise'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update the layout for a clean and accurate appearance
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=40, r=40, t=50, b=60),
    autosize=False,
    width=700,
    height=500
)

# Add source annotation if it exists
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=0.01,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=10, color="#808080")
    )


# Determine the output filename from the input JSON path
output_filename = f"{Path(json_path).stem}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")