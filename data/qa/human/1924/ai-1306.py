import sys
import json
import os
import plotly.graph_objects as go

# Load data from JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and settings from the JSON object
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    texttemplate='- %{label} %{percent}',
    textposition='outside',
    textfont=dict(family="Arial", size=12),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=105
))

# Update the layout for a clean appearance and to add the source annotation
fig.update_layout(
    showlegend=False,
    margin=dict(l=40, r=40, t=40, b=80),
    font=dict(family="Arial"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            text=texts.get('source', ''),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=0.01,
            yanchor='top',
            xanchor='right'
        )
    ] if texts.get('source') else []
)

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)