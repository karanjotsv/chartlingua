import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file at {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file at {json_path} is not a valid JSON file.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for plotting
categories = [item['category'] for item in data]
values = [item['value'] for item in data]
display_texts = [item['display_value'] for item in data]

# Create a new figure
fig = go.Figure()

# Add the bar trace with data and styling from the JSON
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=display_texts,
    textposition='outside',
    marker_color=colors[0],
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevent text labels from being clipped
))

# Configure the layout of the chart
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=80, r=40, t=40, b=80),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showgrid=False,
        showline=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        showline=False,
        zeroline=False,
        showticklabels=False
    )
)

# Add the source text as an annotation
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.98, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=10, color="grey")
    )

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the chart to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as {output_filename}")