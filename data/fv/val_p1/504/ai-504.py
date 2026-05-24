import sys
import json
import os
import plotly.graph_objects as go

# Load data from the JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data for plotting
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f"<b>{v}</b>" for v in values],
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(
        family="Arial",
        size=16,
        color='white'
    ),
    hoverinfo='none'
))

# Customize the layout to match the original image
fig.update_layout(
    title=dict(
        text=f"<b>{texts['title']}</b>",
        x=0.5,
        y=0.9,
        xanchor='center',
        yanchor='top',
        font=dict(size=26, color='black')
    ),
    xaxis=dict(visible=False),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange='reversed',
        tickfont=dict(size=18, color='black')
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=160, r=20, t=120, b=20),
    font=dict(family="Arial")
)

# Derive the output filename from the input JSON path
base_name = os.path.basename(json_path)
output_filename = os.path.splitext(base_name)[0] + '.png'

# Write the output image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")