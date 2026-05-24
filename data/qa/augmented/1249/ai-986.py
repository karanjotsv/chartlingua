import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument for the JSON file path
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Read the JSON data from the specified file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and text from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data lists for Plotly; data in JSON is pre-sorted for bottom-to-top rendering
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Format text labels for bars with a space as the thousands separator
bar_texts = [f'{v:,}'.replace(',', ' ') for v in values]

# Create the main figure object
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0],
    text=bar_texts,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12
    ),
    cliponaxis=False, # Prevents text labels from being clipped at the plot edge
    hoverinfo='none'
))

# Configure the chart layout
fig.update_layout(
    font=dict(
        family="Arial",
        size=12
    ),
    title=dict(
        text=(texts.get('title') or '') + (f"<br><sub>{texts.get('subtitle')}</sub>" if texts.get('subtitle') else ''),
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        tickformat=',.0f' # Use comma separator for axis ticks
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=250, r=100, t=50, b=80), # Adjust margins for labels and source text
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.12,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Derive the output filename from the input JSON path
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")