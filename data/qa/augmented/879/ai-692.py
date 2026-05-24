import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Format text labels for display on bars
text_labels = [f"{v:.1f}" if v % 1 != 0 else f"{int(v)}" for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=text_labels,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Define shapes for alternating background color
background_shapes = []
for i in range(len(categories)):
    if i % 2 != 0:
        shape = go.layout.Shape(
            type="rect",
            xref="x",
            yref="paper",
            x0=i - 0.5,
            y0=0,
            x1=i + 0.5,
            y1=1,
            fillcolor="#f5f5f5",
            layer="below",
            line_width=0
        )
        background_shapes.append(shape)

# Update layout
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 10000],
        tickvals=[0, 2000, 4000, 6000, 8000, 10000],
        ticktext=['0', '2 000', '4 000', '6 000', '8 000', '10 000'],
        showgrid=True,
        gridwidth=1,
        gridcolor='#e0e0e0',
        zeroline=False,
        ticksuffix=" " # Add padding to tick labels
    ),
    margin=dict(l=90, r=40, t=50, b=80),
    showlegend=False,
    shapes=background_shapes,
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
            font=dict(size=12)
        )
    ]
)

# Define output filename and save the image
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")