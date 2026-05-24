import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Define paths
json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

output_image_path = json_file_path.with_suffix('.png')

# Load data from JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data_series = config['chart_data'][0]
texts = config['texts']
colors = config['colors']
categories = chart_data_series['categories']
values = chart_data_series['values']

# Initialize the figure
fig = go.Figure()

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='auto',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

# Create faint background stripes for alternating years
shapes = []
for i in range(1, len(categories), 2):
    shapes.append(go.layout.Shape(
        type="rect",
        xref="x",
        yref="paper",
        x0=i - 0.5,
        y0=0,
        x1=i + 0.5,
        y1=1,
        fillcolor="#f8f8f8",
        layer="below",
        line_width=0
    ))

# Update the layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts.get('title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickfont=dict(size=12),
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        zeroline=False,
        range=[0, 250],
        dtick=50,
        tickfont=dict(size=12),
        linecolor='black',
        linewidth=1
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    shapes=shapes,
    annotations=[
        dict(
            text=texts.get('note'),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.0,
            y=-0.22,
            xanchor='left',
            yanchor='top',
            font=dict(size=12, color='#0073B2') # Blue color like in the original
        ),
        dict(
            text=texts.get('source'),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#666666')
        )
    ]
)

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to '{output_image_path}'")