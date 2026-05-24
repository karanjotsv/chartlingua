import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

# Extract data, texts, and colors from the JSON object
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series in the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=[f"{val}{texts.get('data_labels_suffix', '')}" for val in series['y']],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=14,
            color='black',
            weight='bold'
        ),
        cliponaxis=False
    ))

# Update the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12, color="#333333"),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left',
        font=dict(size=24)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 120],
        tickvals=[0, 20, 40, 60, 80, 100, 120],
        ticksuffix='%',
        gridcolor='#e0e0e0',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=texts.get('additional_info', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.25,
            xanchor='left',
            yanchor='top',
            font=dict(size=14, color="#0d6efd")
        ),
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color="#555555")
        )
    ]
)

# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)
print(f"Chart successfully generated and saved as {output_filename}")