import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the specified file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the JSON file, ensuring UTF-8 encoding for multilingual support
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and texts from the JSON structure
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    sort=False,  # This is critical to preserve the order from the JSON data
    direction='clockwise',
    hoverinfo='label+percent',
    textinfo='none'
))

# Prepare annotations for source/note text to be placed at the bottom
annotations = []
if texts.get('source_left'):
    annotations.append(
        go.layout.Annotation(
            text=texts['source_left'],
            x=0,
            y=0,
            xref="paper",
            yref="paper",
            showarrow=False,
            align="left",
            xanchor="left",
            yanchor="bottom"
        )
    )
if texts.get('source_right'):
    annotations.append(
        go.layout.Annotation(
            text=texts['source_right'],
            x=0.7,
            y=0,
            xref="paper",
            yref="paper",
            showarrow=False,
            align="left",
            xanchor="left",
            yanchor="bottom"
        )
    )

# Update the layout for a clean and accurate presentation
fig.update_layout(
    showlegend=True,
    plot_bgcolor='#D3D3D3',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        x=1.02,
        y=1,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.7)',
        bordercolor='Black',
        borderwidth=1
    ),
    # Add substantial bottom margin to prevent annotations from being clipped
    margin=dict(l=40, r=40, t=40, b=250),
    annotations=annotations
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")