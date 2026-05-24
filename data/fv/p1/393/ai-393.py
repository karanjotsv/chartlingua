import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
layout_opts = config['layout_options']

fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(
    x=chart_data['scatter_points']['x'],
    y=chart_data['scatter_points']['y'],
    mode='markers',
    marker=dict(color=colors['primary'], size=6),
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=chart_data['ray_optics_solid']['x'],
    y=chart_data['ray_optics_solid']['y'],
    mode='lines',
    line=dict(color=colors['primary'], width=2),
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=chart_data['ray_optics_dashed']['x'],
    y=chart_data['ray_optics_dashed']['y'],
    mode='lines',
    line=dict(color=colors['primary'], width=2, dash='dash'),
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=chart_data['far_field_line']['x'],
    y=chart_data['far_field_line']['y'],
    mode='lines',
    line=dict(color=colors['primary'], width=2),
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=chart_data['spurious_region']['x'],
    y=chart_data['spurious_region']['y'],
    mode='lines',
    line=dict(color=colors['primary'], width=1.5),
    fill='toself',
    fillcolor=colors['spurious_region_fill'],
    fillpattern=dict(shape='/', fgcolor=colors['primary'], solidity=0.3),
    showlegend=False
))

# Create custom axis box with break
shapes = []
x_range = layout_opts['x_range']
y_range = layout_opts['y_range']
break_pos = layout_opts['axis_break_pos']
break_hw = layout_opts['axis_break_width'] / 2

# Box lines with gaps for break symbols
shapes.append(dict(type='line', x0=x_range[0], y0=y_range[0], x1=break_pos - break_hw, y1=y_range[0], line=dict(color=colors['primary'], width=2)))
shapes.append(dict(type='line', x0=break_pos + break_hw, y0=y_range[0], x1=x_range[1], y1=y_range[0], line=dict(color=colors['primary'], width=2)))
shapes.append(dict(type='line', x0=x_range[0], y0=y_range[1], x1=break_pos - break_hw, y1=y_range[1], line=dict(color=colors['primary'], width=2)))
shapes.append(dict(type='line', x0=break_pos + break_hw, y0=y_range[1], x1=x_range[1], y1=y_range[1], line=dict(color=colors['primary'], width=2)))
shapes.append(dict(type='line', x0=x_range[0], y0=y_range[0], x1=x_range[0], y1=y_range[1], line=dict(color=colors['primary'], width=2)))
shapes.append(dict(type='line', x0=x_range[1], y0=y_range[0], x1=x_range[1], y1=y_range[1], line=dict(color=colors['primary'], width=2)))

# Break symbols
y_break_amp = 0.08
x_start, x_end = break_pos - break_hw, break_pos + break_hw
x_mid1, x_mid2 = break_pos - break_hw/2, break_pos + break_hw/2

y0_base = y_range[0]
path_bottom = f"M{x_start},{y0_base} L{x_mid1},{y0_base + y_break_amp} L{x_mid2},{y0_base - y_break_amp} L{x_end},{y0_base}"
shapes.append(dict(type='path', path=path_bottom, line=dict(color=colors['primary'], width=2)))

y1_base = y_range[1]
path_top = f"M{x_start},{y1_base} L{x_mid1},{y1_base + y_break_amp} L{x_mid2},{y1_base - y_break_amp} L{x_end},{y1_base}"
shapes.append(dict(type='path', path=path_top, line=dict(color=colors['primary'], width=2)))

fig.update_layout(
    font=dict(family="Arial", size=14),
    title=texts.get('title'),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    xaxis=dict(
        range=layout_opts['x_range'],
        tickvals=layout_opts['x_tickvals'],
        showline=False,
        showgrid=False,
        zeroline=False,
        ticks='outside',
        tickwidth=2,
        ticklen=8
    ),
    yaxis=dict(
        range=layout_opts['y_range'],
        tickvals=layout_opts['y_tickvals'],
        showline=False,
        showgrid=False,
        zeroline=False,
        ticks='outside',
        tickwidth=2,
        ticklen=8
    ),
    plot_bgcolor='white',
    margin=dict(l=90, r=40, t=60, b=90),
    annotations=[dict(
        xref="x", yref="y",
        x=ann['x'], y=ann['y'],
        text=ann['text'],
        showarrow=ann.get('showarrow', False),
        font=dict(family="Arial", size=14),
        align=ann.get('align', 'center'),
        xanchor=ann.get('xanchor', 'center'),
        yanchor=ann.get('yanchor', 'middle'),
        textangle=ann.get('textangle', 0)
    ) for ann in texts['annotations']],
    shapes=shapes
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")