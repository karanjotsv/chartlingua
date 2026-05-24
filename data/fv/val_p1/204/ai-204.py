import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Create a Plotly figure
fig = go.Figure()

# Add a trace for each data series specified in the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(color=colors[i % len(colors)], width=2) # Cycle through colors if needed
    ))

# Configure the layout of the chart
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(size=24)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickmode='linear',
        dtick=25,
        showgrid=True,
        gridcolor='#B4B4A2',
        gridwidth=1,
        zeroline=False
    ),
    yaxis=dict(
        type='log',
        title=texts.get('y_axis_title'),
        exponentformat='E',
        showexponent='all',
        showgrid=True,
        gridcolor='#B4B4A2',
        gridwidth=1,
        minor=dict(
            showgrid=True,
            gridcolor='#C9C9B5',
            gridwidth=1
        )
    ),
    plot_bgcolor='#D8D8C2',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='whitesmoke',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=80, r=40, t=80, b=80)
)

# Derive the output filename from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")