import sys
import json
import os
import plotly.graph_objects as go

# Read chart data from the JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for plotting
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Reverse the lists to display the chart in the same order as the image (top to bottom)
categories.reverse()
values.reverse()

# Create the figure object
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    texttemplate='%{text:.2f}',
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12)
))

# Configure the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=300, r=50, t=30, b=80),
    xaxis=dict(
        title=texts['x_axis_title'],
        title_font=dict(size=12),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        range=[0, 8.5],
        dtick=1
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    annotations=[
        dict(
            text=texts['source'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")