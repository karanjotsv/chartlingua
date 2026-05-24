import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data in lists for Plotly
y_categories = [item['category'] for item in chart_data]
x_values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f'{v:,}' for v in x_values],
    textposition='auto' # Let Plotly decide best position, but we'll refine
))

# Update trace properties for text labels
fig.update_traces(
    texttemplate='%{x:,}',
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(
        family='Arial',
        size=12,
        color='black'
    ),
    # Adjust bar width
    width=0.8
)


# Update the layout for a clean, professional look
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center',
        font=dict(size=18)
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#e0e0e0',
        tickformat='s' # Use 's' for SI units (e.g., M for millions)
    ),
    yaxis=dict(
        showgrid=False,
        autorange=True, # Automatically determines range
        automargin=True # Prevents y-axis labels from being cut off
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='#f0f0f0',
    paper_bgcolor='#f0f0f0',
    showlegend=False,
    margin=dict(l=10, r=40, t=80, b=50) # Use automargin on y-axis, but set others
)

# Generate the output filename from the input JSON path
output_filename = json_path.with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")