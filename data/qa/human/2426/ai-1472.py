import sys
import json
import plotly.graph_objects as go

# 1. Argument Parsing: Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# 2. File I/O and Data Loading: Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data from the loaded JSON, using .get() for safety
chart_data = config.get('chart_data', {})
texts = config.get('texts', {})
colors = config.get('colors', [])
categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])

# 3. Chart Creation: Initialize a Figure object
fig = go.Figure()

# Add a bar trace for each series, preserving order from the JSON
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('data', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=[f"{val}%" for val in series.get('data', [])],
        textposition='outside',
        cliponaxis=False, # Prevent text from being clipped at the top of the plot
        textfont=dict(size=12, family="Arial", color='black')
    ))

# 4. Layout Configuration: Style the chart to match the original image
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial"),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 85], # Set range to give space for text labels above bars
        tickvals=[0, 20, 40, 60, 80],
        ticktext=['0%', '20%', '40%', '60%', '80%'],
        zeroline=False,
        title_font=dict(size=14),
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2, # Position legend below the x-axis
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=100, t=40), # Adjust margins for labels and source
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source'),
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.3, # Position source text at the bottom right
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    ]
)

# 5. Output: Save the figure to a high-resolution PNG image
# Derive the output filename from the input JSON path without using 'os' module
path_parts = json_path.replace('\\', '/').split('/')
filename_with_ext = path_parts[-1]
base_filename = filename_with_ext.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")