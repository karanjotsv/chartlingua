import sys
import json
import plotly.graph_objects as go

# Ensure the script is called with exactly one command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data and settings from the JSON object
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
series_labels = texts['series_labels']

# Prepare data for Plotly traces
categories = [item['category'] for item in chart_data]
series_values = []
for i in range(len(series_labels)):
    series_values.append([item['values'][i] for item in chart_data])

# Create the figure object
fig = go.Figure()

# Add a bar trace for each data series
for i, label in enumerate(series_labels):
    fig.add_trace(go.Bar(
        y=categories,
        x=series_values[i],
        name=label,
        orientation='h',
        marker=dict(color=colors[i])
    ))

# Combine title and subtitle if available
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout of the chart
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        tickformat='.2%',
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0, 0.45]
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=280, r=40, t=80, b=80),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    width=800,
    height=500
)

# Determine the output filename from the input JSON filename
# This approach avoids using os.path for maximum compatibility
last_slash_idx = -1
if '/' in json_path:
    last_slash_idx = json_path.rfind('/')
if '\\' in json_path:
    last_slash_idx = max(last_slash_idx, json_path.rfind('\\'))
filename_with_ext = json_path[last_slash_idx + 1:]
if '.' in filename_with_ext:
    base_name = filename_with_ext.rsplit('.', 1)[0]
else:
    base_name = filename_with_ext
output_filename = f"{base_name}.png"


# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")