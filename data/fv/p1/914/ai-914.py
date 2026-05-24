import sys
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Ensure a single command-line argument is provided for the JSON file path.
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Resolve the input JSON file path.
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load chart data and texts from the JSON file.
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Create a figure with two subplots for the pie charts.
fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

# Add the first pie chart (Export).
data1 = chart_info['chart_data'][0]
fig.add_trace(go.Pie(
    labels=data1['labels'],
    values=data1['values'],
    marker_colors=data1['colors'],
    pull=[0.05] * len(data1['values']),
    textposition='outside',
    sort=False,
    showlegend=False
), 1, 1)

# Add the second pie chart (Import).
data2 = chart_info['chart_data'][1]
fig.add_trace(go.Pie(
    labels=data2['labels'],
    values=data2['values'],
    marker_colors=data2['colors'],
    pull=[0.05] * len(data2['values']),
    textposition='outside',
    sort=False,
    showlegend=False
), 1, 2)

# Configure the global layout and annotations.
fig.update_layout(
    font_family="Arial",
    margin=dict(t=50, b=120, l=50, r=50),
    annotations=[
        dict(
            text=chart_info['chart_data'][0]['title'],
            x=0.225,
            y=-0.1,
            font_size=16,
            showarrow=False,
            xref="paper",
            yref="paper",
            xanchor='center',
            yanchor='top'
        ),
        dict(
            text=chart_info['chart_data'][1]['title'],
            x=0.775,
            y=-0.1,
            font_size=16,
            showarrow=False,
            xref="paper",
            yref="paper",
            xanchor='center',
            yanchor='top'
        )
    ]
)

# Standardize the font size for the labels outside the pie slices.
fig.update_traces(textfont_size=14)

# Generate the output PNG filename from the input JSON filename.
output_filename = f"{json_path.stem}.png"

# Save the generated chart as a PNG image and confirm completion.
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")