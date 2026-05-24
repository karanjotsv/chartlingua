import sys
import json
import plotly.graph_objects as go
import os

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent'
))

# Combine title and source note for the annotation
annotation_text_parts = []
if texts.get('title'):
    annotation_text_parts.append(f"<b>{texts['title']}</b>")
if texts.get('source_note'):
    annotation_text_parts.append(texts['source_note'])
annotation_text = "<br>".join(annotation_text_parts)

# Update layout for styling, legend, and annotations
fig.update_layout(
    showlegend=True,
    legend=dict(
        x=1,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        traceorder='normal',
        bgcolor='rgba(0,0,0,0)' # Transparent background for the legend box
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    paper_bgcolor='#D3D3D3',
    plot_bgcolor='white',
    # Adjust margins to prevent clipping of legend and annotation
    margin=dict(l=40, r=280, t=40, b=180),
    annotations=[
        dict(
            text=annotation_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")