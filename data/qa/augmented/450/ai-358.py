import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_path}'.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly trace
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
data_labels_suffix = texts.get('data_labels_suffix', '')
bar_labels = [f"{v}{data_labels_suffix}" for v in values]

# Initialize the figure
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=bar_labels,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False  # Allow text labels to be rendered outside the plot area
))

# Configure the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        range=[0, 50],
        tickvals=[0, 10, 20, 30, 40, 50],
        ticktext=[f"{i}%" for i in [0, 10, 20, 30, 40, 50]],
        showline=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    )
)

# Add source annotation if present in the JSON
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=0,
        xanchor='right',
        yanchor='top',
        yshift=-50,
        font=dict(size=10, color="#666666")
    )

# Update the font for the data labels on the bars
fig.update_traces(textfont=dict(size=12, color='black'))

# Determine the output filename from the input JSON path
base_name = pathlib.Path(json_path).stem
output_filename = f"{base_name}.png"

# Save the figure to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")