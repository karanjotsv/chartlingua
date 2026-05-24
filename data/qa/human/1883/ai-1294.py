import sys
import json
import os
import plotly.graph_objects as go

# Ensure the script is called with one argument: the path to the JSON file
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]
text_labels = [f"{v}%" for v in values]

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors,
    text=text_labels,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    ),
    cliponaxis=False
))

# Update the layout for a professional look and feel
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=280, r=40, t=40, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        title_font=dict(family="Arial", size=14, color='#555'),
        tickfont=dict(family="Arial", size=12),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.18],
        ticksuffix='%'
    ),
    yaxis=dict(
        autorange='reversed',  # To display categories from top to bottom
        showgrid=False,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        tickfont=dict(family="Arial", size=14)
    )
)

# Add the source text as an annotation
fig.add_annotation(
    text=texts.get('source'),
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.98,
    y=-0.15,
    xanchor='right',
    yanchor='top',
    font=dict(family="Arial", size=12, color='#888')
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")