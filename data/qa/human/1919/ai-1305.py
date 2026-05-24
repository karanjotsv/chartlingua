import sys
import json
import os
import plotly.graph_objects as go

# Read chart data from the JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the plot
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=[f'{v}%' for v in values],
    textposition='outside',
    marker_color=colors[0],
    textfont=dict(family="Arial", size=12, weight="bold", color='black'),
    cliponaxis=False  # Allow text to be drawn outside the plot area
))

# Configure layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    yaxis_title=texts.get('y_axis_title'),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 61],
        tick0=0,
        dtick=10,
        ticksuffix='%'
    ),
    margin=dict(t=40, r=40, b=160, l=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=-0.35,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")