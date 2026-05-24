import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

# Add the main curve
fig.add_trace(go.Scatter(
    x=chart_data['curve']['x'],
    y=chart_data['curve']['y'],
    mode='lines',
    line=dict(color=colors['curve'], width=3),
    showlegend=False
))

# Add all dashed lines
for line_data in chart_data['dashed_lines']:
    fig.add_trace(go.Scatter(
        x=line_data['x'],
        y=line_data['y'],
        mode='lines',
        line=dict(color=colors['lines'], width=1.5, dash='dash'),
        showlegend=False
    ))

# Set layout properties
x_range = [-0.5, 5.5]
y_range = [-2.5, 2.5]

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(
        range=x_range,
        visible=False
    ),
    yaxis=dict(
        range=y_range,
        visible=False
    )
)

# Draw custom axes lines
fig.add_shape(type="line", x0=0, y0=0, x1=x_range[1], y1=0,
              line=dict(color=colors['axes'], width=2))
fig.add_shape(type="line", x0=0, y0=y_range[0], x1=0, y1=y_range[1],
              line=dict(color=colors['axes'], width=2))

# Draw custom axis arrows
fig.add_annotation(
    ax=x_range[1] - 0.2, ay=0, x=x_range[1], y=0,
    xref='x', yref='y', axref='x', ayref='y',
    showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor=colors['axes']
)
fig.add_annotation(
    ax=0, ay=y_range[1] - 0.2, x=0, y=y_range[1],
    xref='x', yref='y', axref='x', ayref='y',
    showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor=colors['axes']
)

# Add text annotations from JSON
for ann in texts.get('annotations', []):
    fig.add_annotation(
        text=ann['text'],
        x=ann['x'],
        y=ann['y'],
        xref="x",
        yref="y",
        showarrow=False,
        font=dict(
            family="Arial",
            size=18,
            color=colors['text']
        ),
        xanchor=ann.get('xanchor', 'center'),
        yanchor=ann.get('yanchor', 'middle')
    )

fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")