import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
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

# Extract data for plotting
data = chart_info.get('chart_data', {})
labels = data.get('labels', [])
series_data = data.get('series', [])
colors = chart_info.get('colors', [])
texts = chart_info.get('texts', {})

# Create subplots for the three pie charts
subplot_titles = [s.get('name', '') for s in series_data]
fig = make_subplots(rows=1, cols=3,
                    specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]],
                    subplot_titles=subplot_titles)

# Add a pie chart trace for each series
for i, series in enumerate(series_data):
    fig.add_trace(go.Pie(
        labels=labels,
        values=series.get('values', []),
        marker_colors=colors,
        name=series.get('name', ''),
        sort=False,  # Preserve the original order of data
        showlegend=(i == 0)  # Show legend only for the first pie chart
    ), row=1, col=i + 1)

# Update trace properties
fig.update_traces(
    textinfo='none',
    hoverinfo='label+percent',
    hole=.0
)

# Update layout for a clean, accurate look
fig.update_layout(
    font_family="Arial",
    paper_bgcolor='white',
    plot_bgcolor='white',
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.8,
        xanchor="left",
        x=0.01
    ),
    margin=dict(l=150, r=40, t=60, b=40)
)

# Update subplot title font size
for annotation in fig['layout']['annotations']:
    annotation['font']['size'] = 16

# Determine output filename and save the image
base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)