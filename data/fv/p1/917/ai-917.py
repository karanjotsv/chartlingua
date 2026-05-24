import sys
import json
import plotly.graph_objects as go
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
filename_base = Path(json_path).stem

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

# Extract data from JSON
data = chart_data['chart_data']
texts = chart_data['texts']
styles = chart_data['styles']
bg_shapes = chart_data['background_colors']['shapes']
x_values = data['x']

# Add data series traces
for i, series in enumerate(data['series']):
    style = styles[i]
    
    marker_config = {
        'symbol': style.get('marker_symbol', 'circle'),
        'size': 8
    }
    if 'marker_color' in style:
        marker_config['color'] = style['marker_color']
    if 'marker_line_color' in style:
        marker_config['line'] = {
            'color': style['marker_line_color'],
            'width': style.get('marker_line_width', 1)
        }

    fig.add_trace(go.Scatter(
        x=x_values,
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=style['line_color'], width=1.5),
        marker=marker_config,
        showlegend=True
    ))

# Update layout
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.98,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        tickvals=x_values,
        ticktext=x_values
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        autorange='reversed',
        range=[14.5, 0.5],
        tickmode='linear',
        tick0=1,
        dtick=1,
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        gridcolor='LightGray',
        gridwidth=1
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=80, b=150),
    width=1000,
    height=700
)

# Add background shapes
for shape_info in bg_shapes:
    fig.add_shape(
        type="rect",
        xref="paper",
        yref="y",
        x0=0,
        y0=shape_info['y0'],
        x1=1,
        y1=shape_info['y1'],
        fillcolor=shape_info['color'],
        layer="below",
        line_width=0
    )

output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")