import sys
import json
import os
import plotly.graph_objects as go

# Load data from the JSON file provided as a command-line argument
json_path = sys.argv[1]
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [d['x'] for d in data]
y_values = [d['y'] for d in data]

# Create the figure object
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=[f'{y:.2f}%' for y in y_values],
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False
))

# Update layout for a clean and accurate presentation
fig.update_layout(
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        ticks=''
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 40],
        showgrid=True,
        gridcolor='#E0E0E0',
        showline=False,
        ticksuffix='%'
    ),
    margin=dict(l=80, r=40, t=80, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=10, color='grey')
        )
    ]
)

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")