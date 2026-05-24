import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Read the chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and settings from the JSON object
chart_data = chart_info.get('chart_data', [])
colors = chart_info.get('colors', [])
texts = chart_info.get('texts', {})

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the donut chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.65,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=1)
    ),
    hoverinfo='label+percent',
    textinfo='value',
    texttemplate='%{value:.1f}%',
    textfont=dict(
        family="Arial",
        size=16,
        color='white'
    ),
    sort=False,
    direction='clockwise',
    rotation=98  # Adjust rotation to match the small slices at the top
))

# Configure the layout
fig.update_layout(
    showlegend=True,
    legend=dict(
        x=0.85,
        y=0.95,
        xanchor='left',
        yanchor='top',
        traceorder='normal',
        font=dict(
            family="Arial",
            size=14,
            color="black"
        ),
        bgcolor='rgba(0,0,0,0)' # Transparent legend background
    ),
    font=dict(
        family="Arial"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=20, b=20),
    autosize=False,
    width=800,
    height=600
)

# Generate the output filename from the input JSON path stem
output_filename = f"{json_path.stem}.png"

# Save the figure as a high-resolution PNG image and print a confirmation
fig.write_image(output_filename, scale=2)
print(f"Chart saved as {output_filename}")