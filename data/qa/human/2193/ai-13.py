import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
num_series = len(texts.get('legend_labels', []))
series_data = [[item['values'][i] for item in chart_data] for i in range(num_series)]

# Create the figure
fig = go.Figure()

# Add a bar trace for each data series
for i in range(num_series):
    fig.add_trace(go.Bar(
        name=texts['legend_labels'][i],
        x=categories,
        y=series_data[i],
        marker_color=colors[i],
        text=series_data[i],
        textposition='outside',
        texttemplate='%{text}',
        cliponaxis=False  # Prevent data labels from being clipped at the top
    ))

# Update layout for a professional look and feel
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    font=dict(family="Arial", size=12, color="#333"),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left',
        font=dict(size=18)
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 400],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        linecolor='black'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showline=True,
        linecolor='black'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=100, t=50),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=-0.32,
            xanchor='right', yanchor='bottom',
            align='right',
            font=dict(size=10, color='#6c757d')
        )
    ]
)

# Derive output filename from the input JSON path
path_obj = pathlib.Path(json_path)
filename_base = path_obj.stem
output_filename = f"{filename_base}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")