import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data from JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})

# Create subplots figure
num_charts = len(chart_data)
fig = make_subplots(
    rows=num_charts,
    cols=1,
    specs=[[{'type': 'domain'}] for _ in range(num_charts)],
    vertical_spacing=0.08
)

# Define subplot vertical positions for annotations
y_positions = {
    1: [0.75],
    2: [0.8, 0.2],
    3: [0.845, 0.5, 0.155]
}
subplot_y_anchors = y_positions.get(num_charts, [0.5] * num_charts)

# Add a pie chart for each entry in chart_data
for i, subplot_spec in enumerate(chart_data):
    row_num = i + 1
    series_data = subplot_spec.get('series', [])
    title = subplot_spec.get('title', '')

    labels = [s['label'] if s['label'] is not None else "" for s in series_data]
    values = [s['value'] for s in series_data]
    colors = [s['color'] for s in series_data]

    texttemplate = ''
    if title == 'GHG':
        texttemplate = '%{value:.2f}%'
    elif title == 'Energy':
        texttemplate = '%{value}'
    
    textinfo = 'none' if not texttemplate else None

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        sort=False,
        texttemplate=texttemplate,
        textinfo=textinfo,
        hoverinfo='label+percent',
        legendgroup=f'group{row_num}',
        name=title
    ), row=row_num, col=1)

    # Add title annotation to the left of each subplot
    fig.add_annotation(
        text=f'<b>{title}</b>',
        align='center',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=-0.05,
        y=subplot_y_anchors[i],
        xanchor='right',
        yanchor='middle',
        font=dict(size=14)
    )

# Update layout
fig.update_layout(
    height=800,
    width=750,
    margin=dict(l=100, r=250, t=50, b=50),
    font=dict(family="Arial", size=12),
    legend=dict(
        traceorder='grouped',
        x=1,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        title=dict(text='Categories')
    ),
    plot_bgcolor='#F0F0F0',
    paper_bgcolor='#F0F0F0'
)

# Update trace-specific properties
fig.update_traces(
    textposition='auto',
    textfont_size=10,
    insidetextorientation='radial',
    selector=dict(type='pie')
)

# Define output filename and save the image
output_filename = json_file_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")