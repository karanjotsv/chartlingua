import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the JSON structure
chart_data = chart_info.get('chart_data', [])
bar_color = chart_info.get('colors', ["#EA3323"])[0]

# Prepare for subplot creation
subplot_titles = [d.get('title', '') for d in chart_data]
specs = [[{}, {}], [{}, {}], [{}, {}], [{'colspan': 2}, None]]
positions = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2), (4, 1)]

# Create subplots figure
fig = make_subplots(
    rows=4,
    cols=2,
    specs=specs,
    subplot_titles=subplot_titles,
    vertical_spacing=0.12,
    horizontal_spacing=0.15
)

# Determine a consistent x-axis range for all subplots
max_value = 0
for data_series in chart_data:
    if data_series['values']:
        max_value = max(max_value, max(data_series['values']))
x_range = [0, max_value * 1.15]

# Add a trace for each chart
for i, data_series in enumerate(chart_data):
    row, col = positions[i]

    # Plotly plots horizontal bars from bottom to top, so we reverse the data
    categories = data_series['categories'][::-1]
    values = data_series['values'][::-1]

    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker=dict(color=bar_color),
        text=values,
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color=bar_color
        ),
        hoverinfo='none',
        cliponaxis=False # Prevents text labels from being clipped
    ), row=row, col=col)

# Update layout and styling
fig.update_layout(
    font_family="Arial",
    height=1200,
    width=1000,
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=250, r=50, t=80, b=50) # Increased left margin for labels
)

# Style subplot titles (annotations)
for annotation in fig.layout.annotations:
    annotation.update(
        x=0,
        xanchor='left',
        font=dict(size=16)
    )

# Hide all x-axes but set their range for consistent scaling
fig.update_xaxes(
    visible=False,
    range=x_range
)

# Style all y-axes to show labels but no lines or ticks
fig.update_yaxes(
    showgrid=False,
    showline=False,
    ticks='',
    automargin=True,
    tickfont=dict(
        family="Arial",
        size=14,
        color='#333333'
    )
)

# Generate output file path and save the image
output_filename = pathlib.Path(json_path).stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")