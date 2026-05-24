import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
texts = chart_data['texts']
charts = chart_data['chart_data']

# Create a 2x2 subplot grid. Pie charts are of 'domain' type.
# The top-left cell is left empty for the main title annotation.
fig = make_subplots(
    rows=2,
    cols=2,
    specs=[[{}, {'type': 'domain'}],
           [{'type': 'domain'}, {'type': 'domain'}]],
    horizontal_spacing=0.05,
    vertical_spacing=0.15
)

# Define the positions for the three charts in the grid
chart_positions = [(1, 2), (2, 1), (2, 2)]
chart_pull = [0.05] * 5 # Explode slices slightly for visual separation

# Add each pie chart to its respective subplot
for i, chart in enumerate(charts):
    row, col = chart_positions[i]
    fig.add_trace(go.Pie(
        labels=chart['labels'],
        values=chart['values'],
        marker_colors=chart['colors'],
        pull=chart_pull,
        title={
            'text': f"<b>{chart['title']}</b>",
            'position': 'top center',
            'font': {'size': 16, 'family': 'Arial'}
        },
        hoverinfo='label+percent',
        textinfo='none',
        sort=False  # Preserve original data order
    ), row=row, col=col)

# Combine main title and subtitle using HTML and place in the empty top-left area
main_title_text = f"<span style='font-size: 24px;'><b>{texts['title']}</b></span><br><span style='font-size: 16px;'>{texts['subtitle']}</span>"
fig.add_annotation(
    text=main_title_text,
    align='left',
    showarrow=False,
    xref='paper', yref='paper',
    x=0.02, y=0.85,
    xanchor='left', yanchor='top'
)

# Update layout for a clean and professional look
fig.update_layout(
    height=700,
    width=1100,
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.95,
        xanchor="right",
        x=1.15,  # Position legend outside plot area
        font=dict(
            family="Arial",
            size=12
        )
    ),
    margin=dict(l=40, r=200, t=80, b=40),
    paper_bgcolor='white',
    font_family="Arial"
)

# Derive output filename from JSON path
p = pathlib.Path(json_path)
output_filename = p.with_suffix('.png').name

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")