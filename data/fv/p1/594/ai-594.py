import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get file path from argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the donut chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.6,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=4) # Creates the separation between slices
    ),
    texttemplate='<b>%{value}%</b>',
    textposition='inside',
    textfont=dict(
        family='Arial',
        size=16,
        color='white'
    ),
    hoverinfo='label+percent',
    sort=False,  # Preserve the original order
    direction='clockwise'
))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        y=0.97,
        xanchor='center',
        yanchor='top',
        font=dict(
            family='Arial',
            size=20,
            color='black'
        )
    ),
    showlegend=True,
    legend=dict(
        x=0.5,
        y=-0.1,
        xanchor='center',
        yanchor='top',
        font=dict(
            family='Arial',
            size=14
        )
    ),
    font=dict(
        family="Arial"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=120, b=120, l=40, r=40)
)

# Generate the output PNG file path from the input JSON file path
output_png_path = json_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")