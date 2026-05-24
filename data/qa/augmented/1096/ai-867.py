import sys
import json
import os
import plotly.graph_objects as go

# Read the JSON file path from the command-line argument
if len(sys.argv) != 2:
    # A single print for usage is acceptable for script usability
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly trace
x_data = [item['x'] for item in data]
y_data = [item['y'] for item in data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace with data and styling from the JSON
fig.add_trace(go.Bar(
    x=x_data,
    y=y_data,
    marker_color=colors[0],
    text=[f"<b>{y:,}</b>".replace(',', ' ') for y in y_data],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

# Combine title and subtitle if they exist
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout of the chart
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='lightgrey',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 105000],
        tickvals=[0, 20000, 40000, 60000, 80000, 100000],
        ticktext=['0', '20 000', '40 000', '60 000', '80 000', '100 000'],
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=50, b=120),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.22,
            xanchor='right', yanchor='top',
            text=texts.get('source', ''),
            showarrow=False,
            font=dict(size=12, color='grey')
        )
    ]
)

# Derive the output filename from the input JSON file path
base_name = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_file = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_image_file, scale=2)