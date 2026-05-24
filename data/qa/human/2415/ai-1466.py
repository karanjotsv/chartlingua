import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a command-line argument for the JSON file is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = pathlib.Path(json_path_str)

# Read all data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly, preserving the original order
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace using data from the JSON
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    texttemplate='%{text}%',
    textposition='outside',
    marker_color=colors[0],
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Ensure text labels outside the bars are not clipped
))

# Configure the layout, styling, and annotations
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='lightgrey',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, max(values) * 1.2],  # Set range dynamically with padding
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E5E5E5',
        showline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=90, r=30, t=30, b=120),  # Adjust margins for titles and annotations
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('notes'),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.22,  # Position below x-axis
            xanchor='left',
            yanchor='top',
            font=dict(size=11, color='#666666')
        ),
        dict(
            text=texts.get('source'),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.22,  # Position below x-axis
            xanchor='right',
            yanchor='top',
            font=dict(size=11, color='#666666')
        )
    ]
)

# Derive the output PNG filename from the input JSON path
output_filename = json_path.with_suffix('.png')

# Save the figure to a high-resolution PNG file
fig.write_image(str(output_filename), scale=2)

print(f"Chart saved to {output_filename}")