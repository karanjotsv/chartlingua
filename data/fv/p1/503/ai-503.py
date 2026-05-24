import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})

# Create a subplot figure with a 2x2 grid, specifying 'domain' for pie charts
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{}, {'type': 'domain'}],
           [{'type': 'domain'}, {'type': 'domain'}]],
    horizontal_spacing=0.1,
    vertical_spacing=0.1
)

# Define the subplot positions for the three charts
# Order: Top-Right, Bottom-Left, Bottom-Right
chart_positions = [(1, 2), (2, 1), (2, 2)]

# Add each pie chart trace to its designated subplot
for i, chart in enumerate(chart_data):
    if i < len(chart_positions):
        row, col = chart_positions[i]
        fig.add_trace(
            go.Pie(
                labels=chart['labels'],
                values=chart['values'],
                marker_colors=chart['colors'],
                hoverinfo='none',
                textinfo='none',
                showlegend=False,
                sort=False
            ),
            row=row, col=col
        )

# --- Create all text elements using annotations for precise layout control ---

annotations = []

# 1. Main title and subtitle in the top-left empty cell
main_title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"
annotations.append(
    go.layout.Annotation(
        text=main_title_text,
        align='left',
        showarrow=False,
        xref='paper', yref='paper',
        x=0.01, y=0.98,
        xanchor='left', yanchor='top',
        font=dict(size=18)
    )
)

# 2. Chart titles and custom legends for each subplot
legend_params = {
    '1-2': {'x': 0.99, 'y': 0.92, 'xanchor': 'left', 'title_x': 0.75, 'title_y': 0.99},
    '2-1': {'x': 0.49, 'y': 0.42, 'xanchor': 'left', 'title_x': 0.25, 'title_y': 0.49},
    '2-2': {'x': 0.99, 'y': 0.42, 'xanchor': 'left', 'title_x': 0.75, 'title_y': 0.49}
}
legend_item_spacing = 0.06

for i, chart in enumerate(chart_data):
    if i < len(chart_positions):
        row, col = chart_positions[i]
        key = f"{row}-{col}"
        params = legend_params[key]

        # Add chart title
        annotations.append(
            go.layout.Annotation(
                text=f"<b>{chart['title']}</b>",
                showarrow=False,
                xref='paper', yref='paper',
                x=params['title_x'], y=params['title_y'],
                xanchor='center', yanchor='top',
                font=dict(size=14)
            )
        )

        # Add custom legend items for the chart
        y_pos = params['y']
        for label, color in zip(chart['labels'], chart['colors']):
            # Legend color marker
            annotations.append(
                go.layout.Annotation(
                    text='■',
                    showarrow=False,
                    xref='paper', yref='paper',
                    x=params['x'] - 0.04, y=y_pos,
                    xanchor=params['xanchor'], yanchor='middle',
                    font=dict(color=color, size=20)
                )
            )
            # Legend text
            annotations.append(
                go.layout.Annotation(
                    text=label,
                    showarrow=False,
                    xref='paper', yref='paper',
                    x=params['x'], y=y_pos,
                    xanchor=params['xanchor'], yanchor='middle',
                    align='left'
                )
            )
            y_pos -= legend_item_spacing

# Update the figure layout with all annotations and global styling
fig.update_layout(
    annotations=annotations,
    margin=dict(l=20, r=20, t=40, b=20),
    width=1100,
    height=700,
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12)
)

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")