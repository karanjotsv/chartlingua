import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_filename = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']

fig = go.Figure()

boundaries = []
# Define a base boundary at y=0
base_x = chart_data['series'][0]['boundary_points']['pre_fire']['x'] + chart_data['series'][0]['boundary_points']['post_fire']['x']
boundaries.append({'x': base_x, 'y': [0] * len(base_x)})

# Process each series to create fillable polygons and dashed lines
for i, series in enumerate(chart_data['series']):
    s_data = series['boundary_points']
    x_boundary = s_data['pre_fire']['x'] + s_data['post_fire']['x']
    y_boundary = s_data['pre_fire']['y'] + s_data['post_fire']['y']
    boundaries.append({'x': x_boundary, 'y': y_boundary})

    # Create polygon for fill
    lower_boundary = boundaries[i]
    x_fill = x_boundary + lower_boundary['x'][::-1]
    y_fill = y_boundary + lower_boundary['y'][::-1]

    fig.add_trace(go.Scatter(
        x=x_fill,
        y=y_fill,
        mode='lines',
        line_width=0,
        fill='toself',
        fillpattern=series['fill_pattern'],
        hoverinfo='none',
        showlegend=False
    ))

    # Add dashed boundary line
    fig.add_trace(go.Scatter(
        x=x_boundary,
        y=y_boundary,
        mode='lines',
        line=dict(color=series['line_color'], dash='dash', width=2),
        hoverinfo='none',
        showlegend=False
    ))

# Add vertical lines
y_axis_line = chart_data['y_axis_line']
fig.add_shape(type="line",
              x0=y_axis_line['x'], y0=y_axis_line['y_range'][0],
              x1=y_axis_line['x'], y1=y_axis_line['y_range'][1],
              line=dict(color="black", width=2))

zero_line = chart_data['vertical_line_at_zero']
fig.add_shape(type="line",
              x0=zero_line['x'], y0=zero_line['y_range'][0],
              x1=zero_line['x'], y1=zero_line['y_range'][1],
              line=dict(color="black", width=1))

# Add fire event annotation
fire = chart_data['fire_event']
fig.add_annotation(
    x=fire['x'],
    y=fire['y'],
    text=fire['text'],
    showarrow=False,
    font=dict(color=fire['color'], size=fire['size'], family="Arial")
)

# Custom Legend
fig.add_annotation(
    x=0.7, y=1.0,
    xref="paper", yref="paper",
    text=texts['legend_title'],
    showarrow=False,
    font=dict(size=14, family="Arial"),
    xanchor='left',
    yanchor='bottom'
)

legend_y_start = 0.9
legend_spacing = 0.08
for item in chart_data['legend_items']:
    fig.add_trace(go.Scatter(
        x=[0.7], y=[legend_y_start],
        mode='markers',
        xaxis='x2',
        yaxis='y2',
        marker=dict(
            symbol=item['pattern']['symbol'],
            color=item['pattern']['color'],
            size=item['pattern']['size']
        ),
        showlegend=False,
        hoverinfo='none'
    ))
    fig.add_annotation(
        x=0.75, y=legend_y_start,
        xref="paper", yref="paper",
        text=item['name'],
        showarrow=False,
        font=dict(size=12, family="Arial"),
        xanchor='left',
        yanchor='middle'
    )
    legend_y_start -= legend_spacing


fig.update_layout(
    title=dict(text=texts['title'], x=0.05, y=0.95, xanchor='left', yanchor='top'),
    xaxis_title=texts['xaxis_title'],
    yaxis_title=texts['yaxis_title'],
    font=dict(family="Arial", size=12, color="black"),
    xaxis=dict(
        range=[-25, 115],
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[-5, 110],
        showline=False,
        showticklabels=False,
        showgrid=False,
        zeroline=False
    ),
    # Secondary axes for legend markers
    xaxis2=dict(
        domain=[0, 1],
        range=[0,1],
        anchor='y2',
        overlaying='x',
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        showline=False
    ),
    yaxis2=dict(
        domain=[0, 1],
        range=[0,1],
        anchor='x2',
        overlaying='y',
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        showline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=40, r=40, t=80, b=50),
    width=800,
    height=600
)

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")