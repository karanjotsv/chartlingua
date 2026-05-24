import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and configuration from the loaded JSON
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', {})

top_plot_data = chart_data.get('top_plot', {})
bottom_plot_data = chart_data.get('bottom_plot', {})

# Create a figure with two subplots
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.02,
    row_heights=[0.7, 0.3]
)

# --- Top Plot (S&P 500) ---
if top_plot_data:
    # Add the main line trace
    line_data = top_plot_data.get('line_data', [])
    if line_data:
        x_vals = [d['x'] for d in line_data]
        y_vals = [d['y'] for d in line_data]
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode='lines',
            line=dict(color=colors.get('top_line', '#000000'), width=1.5),
            showlegend=False
        ), row=1, col=1)

    # Add markers
    markers = top_plot_data.get('markers', [])
    for marker in markers:
        color = colors.get('marker_up') if marker['symbol'] == 'triangle-up' else colors.get('marker_down')
        fig.add_trace(go.Scatter(
            x=[marker['x']], y=[marker['y']],
            mode='markers',
            marker=dict(
                symbol=marker['symbol'],
                color=color,
                size=12
            ),
            showlegend=False
        ), row=1, col=1)

    # Add shapes (horizontal lines)
    shapes = top_plot_data.get('shapes', [])
    for shape in shapes:
        fig.add_shape(
            type="line",
            x0=shape['x0'], y0=shape['y'],
            x1=shape['x1'], y1=shape['y'],
            line=dict(color=colors.get('shape_line', '#000000'), width=2),
            xref='x1', yref='y1',
            row=1, col=1
        )

    # Add annotations (text labels)
    annotations = top_plot_data.get('annotations', [])
    for ann in annotations:
        fig.add_annotation(
            x=ann['x'], y=ann['y'],
            text=ann['text'],
            showarrow=False,
            font=dict(family="Arial", size=12, color=colors.get('text', '#000000')),
            xref='x1', yref='y1',
            row=1, col=1
        )

# --- Bottom Plot (GITMO-5) ---
if bottom_plot_data:
    line_data = bottom_plot_data.get('line_data', [])
    if line_data:
        x_vals = [d['x'] for d in line_data]
        y_vals = [d['y'] for d in line_data]
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode='lines',
            line=dict(color=colors.get('bottom_line', '#000000'), width=1.5),
            showlegend=False
        ), row=2, col=1)

    # Add "GITMO-5" label as an annotation
    label = bottom_plot_data.get('label')
    if label:
        fig.add_annotation(
            x="1994-06-01", y=90,
            text=label,
            showarrow=False,
            font=dict(family="Arial", size=12, color=colors.get('text', '#000000')),
            xref='x2', yref='y2',
            row=2, col=1
        )

# --- Layout and Styling ---
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=16, color=colors.get('text', '#000000'))
    ),
    plot_bgcolor=colors.get('background', '#ffffff'),
    paper_bgcolor=colors.get('background', '#ffffff'),
    showlegend=False,
    margin=dict(l=50, r=20, t=50, b=40),
    font=dict(family="Arial")
)

# Update Y-axes
fig.update_yaxes(
    range=[350, 1650],
    dtick=200,
    showgrid=True,
    gridwidth=1,
    gridcolor=colors.get('grid'),
    zeroline=False,
    row=1, col=1
)
fig.update_yaxes(
    range=[-5, 105],
    dtick=20,
    showgrid=True,
    gridwidth=1,
    gridcolor=colors.get('grid'),
    zeroline=True,
    zerolinewidth=1,
    zerolinecolor=colors.get('grid'),
    row=2, col=1
)

# Update X-axis (shared, so update the bottom one which is visible)
fig.update_xaxes(
    range=["1993-10-01", "2009-06-01"],
    showgrid=True,
    gridwidth=1,
    gridcolor=colors.get('grid'),
    tickformat='%Y',
    dtick="M12",
    row=2, col=1
)

# --- Output ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2, width=800, height=600)
print(f"Chart saved to {output_filename}")