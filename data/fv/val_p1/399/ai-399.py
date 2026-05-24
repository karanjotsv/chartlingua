import sys
import json
import plotly.graph_objects as go

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Load data from the specified JSON file
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data structures from the loaded JSON
chart_data = config['chart_data'][0]
texts = config['texts']
colors = config['colors']

# Create a figure with a single pie chart trace to represent the circle
fig = go.Figure(data=[go.Pie(
    values=chart_data['values'],
    labels=chart_data['labels'],
    marker_colors=colors['chart_colors'],
    hoverinfo='none',
    textinfo='none',
    sort=False  # Preserve original data order
)])

# Update the figure's layout and styling
fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.9,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    showlegend=False,
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],
    font=dict(
        family="Arial",
        color=colors['text']
    ),
    margin=dict(t=120, b=40, l=40, r=40),
    annotations=[dict(
        text=texts['central_annotation'],
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(
            family="Arial",
            size=80,
            color=colors['text']
        )
    )]
)

# Derive the output filename from the input JSON file path
# This handles paths like './path/to/filename.json' -> 'filename.png'
base_name = json_path.split('/')[-1].replace('.json', '')
output_filename = f"{base_name}.png"

# Save the generated chart to a PNG file with high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")