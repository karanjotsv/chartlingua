import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the chart data and configuration from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='value',
    texttemplate='%{value}%',
    textposition='outside',
    sort=False,  # Preserve the original data order
    direction='clockwise'
))

# Update layout for a professional look, matching the original's style
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center',
        font=dict(size=22)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    font=dict(
        family="Arial",
        size=12,
        color="#000000"
    ),
    paper_bgcolor='#F0F0FA',
    plot_bgcolor='#F0F0FA',
    margin=dict(t=100, b=120, l=40, r=40),
    showlegend=True
)

fig.update_traces(
    textfont_size=14,
    insidetextorientation='radial'
)

# Determine the output filename from the input JSON filename
base_name = pathlib.Path(json_file_path).stem
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")