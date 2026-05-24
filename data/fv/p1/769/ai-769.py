import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Create a figure
fig = go.Figure()

# Add traces from JSON data
for i, series in enumerate(chart_data['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=chart_data['colors'][i], width=1.5),
        marker=dict(symbol='square-open', size=6, color=chart_data['colors'][i])
    ))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=chart_data['texts']['title'],
    xaxis_title=chart_data['texts']['x_axis_title'],
    yaxis_title=chart_data['texts']['y_axis_title'],
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=80, b=60),
    xaxis=dict(
        range=[-60, 60],
        tickvals=[-60, -40, -20, 0, 20, 40, 60],
        ticktext=["-60 V", "-40 V", "-20 V", "0 V", "20 V", "40 V", "60 V"],
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='lightgray',
        griddash='dot',
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        range=[0.97, 1.00],
        tickvals=[0.970, 0.975, 0.980, 0.985, 0.990, 0.995, 1.000],
        tickformat=".3f",
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='lightgray',
        griddash='dot',
        mirror=True,
        ticks='outside'
    )
)

# Add annotations
for ann in chart_data['texts']['annotations']:
    fig.add_annotation(
        text=ann.get('text', ''),
        x=ann.get('x'),
        y=ann.get('y'),
        xref=ann.get('xref', 'x'),
        yref=ann.get('yref', 'y'),
        showarrow=ann.get('showarrow', False),
        ax=ann.get('ax', 0),
        ay=ann.get('ay', 0),
        xanchor=ann.get('xanchor', 'auto'),
        yanchor=ann.get('yanchor', 'auto'),
        align=ann.get('align', 'center'),
        font=dict(family="Arial", size=12, color="black"),
        arrowhead=ann.get('arrowhead', 1),
        arrowsize=ann.get('arrowsize', 1),
        arrowwidth=ann.get('arrowwidth', 1)
    )

# Add the outer dashed rectangle to mimic the original chart's border
fig.add_shape(
    type="rect",
    xref="paper", yref="paper",
    x0=0, y0=0, x1=1, y1=1,
    line=dict(color="black", width=1, dash="dash")
)

# Define output filename and save the image
output_filename = f"{json_file_path.stem}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")