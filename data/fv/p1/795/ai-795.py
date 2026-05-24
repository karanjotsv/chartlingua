import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']

fig = go.Figure()

# Add the density curve trace
fig.add_trace(go.Scatter(
    x=chart_data['density_curve']['x'],
    y=chart_data['density_curve']['y'],
    mode='lines',
    line=dict(color=colors['line'], width=2),
    fill='tozeroy',
    fillcolor=colors['fill'],
    hoverinfo='none',
    showlegend=False
))

# Update layout to match the original image's style
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=16)
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        range=[-0.1, 4.5],
        tickvals=[0, 1, 2, 3, 4],
        showgrid=True,
        gridcolor=colors['grid'],
        gridwidth=1,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[-0.01, 0.55],
        tickvals=[0.0, 0.2, 0.4],
        showgrid=True,
        gridcolor=colors['grid'],
        gridwidth=1,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=80, b=60),
    showlegend=False
)

# Add the vertical mean line as a shape
mean_line_data = chart_data['mean_line']
fig.add_shape(
    type="line",
    x0=mean_line_data['x'],
    y0=mean_line_data['y_range'][0],
    x1=mean_line_data['x'],
    y1=mean_line_data['y_range'][1],
    line=dict(
        color=colors['mean_line'],
        width=2,
        dash="dash"
    )
)

output_path = json_path.with_suffix(".png")
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")