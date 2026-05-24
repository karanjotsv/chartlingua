import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1)),
    textinfo='percent',
    hoverinfo='label+percent',
    sort=False,  # Preserve the order from the JSON file
    direction='counterclockwise',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
))

# Update the layout for a professional look and feel
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(
            family="Arial",
            size=18,
            color='black'
        )
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.75,
        xanchor="left",
        x=0.8,
        font=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='black',
        borderwidth=1
    ),
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=40, r=40, t=100, b=40)
)

# Determine the output filename from the input JSON path
output_path = pathlib.Path(json_file_path)
output_filename = output_path.with_suffix('.png').name

# Write the image to a file
try:
    fig.write_image(output_filename, scale=2, width=800, height=500)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)