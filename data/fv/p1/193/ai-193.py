import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get file path from command-line argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from JSON
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Create subplots
fig = make_subplots(rows=1, cols=3)

# Define panel configurations
panels = [
    {'id': 'a', 'col': 1, 'x_center': 0.16},
    {'id': 'b', 'col': 2, 'x_center': 0.5},
    {'id': 'c', 'col': 3, 'x_center': 0.84}
]

# Common properties
line_color = chart_data['colors']['lines']
axis_range = [0, 11]

for panel in panels:
    panel_id = panel['id']
    col = panel['col']
    panel_data = chart_data['chart_data'][f'panel_{panel_id}']
    texts = chart_data['texts']

    # Add traces for the panel
    for trace_name, trace_data in panel_data.items():
        fig.add_trace(go.Scatter(
            x=trace_data['x'],
            y=trace_data['y'],
            mode='lines',
            line=dict(
                color=line_color,
                dash=trace_data.get('style', 'solid'),
                width=trace_data.get('width', 2)
            ),
            showlegend=False
        ), row=1, col=col)

    # Configure axes for the subplot
    fig.update_xaxes(
        title_text=texts['x_axis_label'],
        title_standoff=0,
        range=axis_range,
        tickvals=[t['value'] for t in texts.get(f'panel_{panel_id}_x_ticks', [])],
        ticktext=[t['label'] for t in texts.get(f'panel_{panel_id}_x_ticks', [])],
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        zeroline=False,
        row=1, col=col
    )
    fig.update_yaxes(
        title_text=texts['y_axis_label'],
        title_standoff=5,
        range=axis_range,
        tickvals=[t['value'] for t in texts.get(f'panel_{panel_id}_y_ticks', [])],
        ticktext=[t['label'] for t in texts.get(f'panel_{panel_id}_y_ticks', [])],
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        zeroline=False,
        row=1, col=col
    )
    
    # Add axis arrows
    xref = f'x{col}'
    yref = f'y{col}'
    fig.add_annotation(
        x=axis_range[1], y=0, xref=xref, yref=yref,
        ax=axis_range[1] - 0.5, ay=0, axref=xref, ayref=yref,
        showarrow=True, arrowhead=2, arrowwidth=1.5, arrowcolor=line_color
    )
    fig.add_annotation(
        x=0, y=axis_range[1], xref=xref, yref=yref,
        ax=0, ay=axis_range[1] - 0.5, axref=xref, ayref=yref,
        showarrow=True, arrowhead=2, arrowwidth=1.5, arrowcolor=line_color
    )

    # Add panel caption
    fig.add_annotation(
        text=texts[f'panel_{panel_id}_caption'],
        xref="paper", yref="paper",
        x=panel['x_center'], y=-0.3,
        showarrow=False,
        font=dict(size=12, family="Arial"),
        xanchor='center',
        yanchor='top'
    )

# Update global layout
fig.update_layout(
    width=1000,
    height=450,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=14, color=line_color),
    margin=dict(l=50, r=50, t=50, b=150)
)

# Output image
filename_base = json_path.stem
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")