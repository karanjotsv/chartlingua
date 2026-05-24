import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# Extract data for plotting
chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

# Prepare data for the pie chart trace
labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]
pull_values = [0.2 if d.get('exploded', False) else 0 for d in chart_data]
text_labels = [f"{d['category']},<br>{d['value']}%" for d in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    pull=pull_values,
    text=text_labels,
    textinfo='text',
    textposition='auto',
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update the layout
fig.update_layout(
    title=dict(
        text=texts.get('title', ''),
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial",
        size=16
    ),
    showlegend=False,
    margin=dict(t=120, b=80, l=80, r=80),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# Update text font for the traces
fig.update_traces(textfont_size=16)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")