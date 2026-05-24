import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

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

# Extract data, texts, and colors from the JSON object
data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Initialize a Plotly figure
fig = go.Figure()

# Add a line trace for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=colors[i], width=2)
    ))

# Combine title and subtitle for the main chart title
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    if title_text:
        title_text += "<br>"
    title_text += texts['subtitle']

# Configure the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 4500],
        tickvals=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500],
        showgrid=True,
        gridcolor='#D3D3D3'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickmode='linear',
        tick0=1992,
        dtick=2,
        showgrid=True,
        gridcolor='#D3D3D3'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=200, t=80, b=50)
)

# Add annotations to serve as a custom legend next to the lines
for i, series in enumerate(data_series):
    fig.add_annotation(
        x=series['x'][-1],
        y=series['y'][-1],
        text=series['name'],
        showarrow=False,
        xshift=10,
        font=dict(color=colors[i]),
        xanchor='left',
        yanchor='middle'
    )

# Determine the output filename from the input JSON path
# e.g., 'path/to/my_chart.json' -> 'my_chart.png'
base_name = json_path.split('/')[-1].split('\\')[-1]
if '.' in base_name:
    base_name = base_name.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)