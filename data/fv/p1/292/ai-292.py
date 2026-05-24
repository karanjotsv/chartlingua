import sys
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

# Get file paths from command-line argument
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix('.png')

# Load data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
series_data = chart_data['series']
labels = chart_data['labels']

# Create subplots for the two pie charts
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

# Add traces for each pie chart
pull_values = [0, 0.1, 0.1, 0.1] # Explode all slices except the first one
for i, series in enumerate(series_data):
    fig.add_trace(go.Pie(
        labels=labels,
        values=series['values'],
        name=series['name'],
        marker_colors=colors,
        pull=pull_values,
        sort=False,  # Preserve original data order
        showlegend=(i == 0), # Show legend only for the first pie chart
        textinfo='none'
    ), 1, i + 1)

# Update layout for styling
fig.update_layout(
    paper_bgcolor='#4F6A4F',
    plot_bgcolor='#4F6A4F',
    margin=dict(t=80, b=80, l=20, r=20),
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    annotations=[
        dict(
            text=series_data[0]['name'],
            x=0.19, y=1.05,
            font_size=28,
            showarrow=False,
            font=dict(family="Arial", color="black")
        ),
        dict(
            text=series_data[1]['name'],
            x=0.81, y=1.05,
            font_size=28,
            showarrow=False,
            font=dict(family="Arial", color="black")
        )
    ]
)

# Save the figure as a high-resolution PNG
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")