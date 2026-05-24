import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    hole=0,
    sort=False,
    direction='clockwise',
    textinfo='none',  # Percentages are in the labels
    hoverinfo='label+percent'
))

# Update layout for a clean and accurate representation
fig.update_layout(
    title=dict(
        text=texts['title'],
        font=dict(size=20, family="Arial", color="black"),
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        x=0.8,
        y=0.9,
        traceorder='normal',
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(0, 0, 0, 0)'
    ),
    margin=dict(l=50, r=50, t=100, b=50),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=True
)

# Determine output filename from JSON path
output_filename_base = pathlib.Path(json_path).stem
output_png_path = f"{output_filename_base}.png"

# Save the figure to a PNG file
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")