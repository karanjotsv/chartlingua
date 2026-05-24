import sys
import os
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

labels = [item.get('category', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    sort=False,
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent'
))

# Update layout
fig.update_layout(
    title_text=texts.get('title'),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=True,
    legend=dict(
        x=0.8,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        traceorder="normal"
    ),
    margin=dict(t=80, b=40, l=40, r=200), # Increase right margin for legend
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)