import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a command-line argument for the JSON file is provided
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Verify that the specified JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the chart data and configuration from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data series, texts, and colors from the loaded JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly by extracting labels and values
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace using data from the JSON file
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1.5)),
    texttemplate='- %{label} %{value}%',
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='#333333'),
    sort=False,  # Preserve the original data order from the JSON
    direction='clockwise',
    showlegend=False
)])

# Update the figure's layout
fig.update_layout(
    font=dict(family="Arial"),
    margin=dict(t=40, r=150, b=60, l=150),  # Generous margins for outside labels
    paper_bgcolor='white',
    plot_bgcolor='white',
    autosize=False,
    width=800,
    height=600
)

# Add source annotation if present in the JSON
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=0.01,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=10, color='grey')
    )

# Determine the output image filename from the input JSON filename
output_path = json_file_path.with_suffix('.png')

# Save the generated chart to a PNG file with high resolution
try:
    fig.write_image(output_path, scale=2)
    print(f"Chart successfully saved to '{output_path}'")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)