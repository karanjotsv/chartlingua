import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
water_area = config.get('water_area')
texts = config.get('texts', {})

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]
bar_colors = [d['color'] for d in chart_data]

fig = go.Figure()

if water_area and 'x_start_index' in water_area and 'x_end_index' in water_area:
    start_bar_x = chart_data[water_area['x_start_index']]['x']
    end_bar_x = chart_data[water_area['x_end_index']]['x']
    
    fig.add_shape(
        type="rect",
        xref="x", yref="y",
        x0=start_bar_x, x1=end_bar_x,
        y0=0, y1=water_area.get('height', 0),
        fillcolor=water_area.get('color', 'lightblue'),
        line_width=0,
        layer='below'
    )

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=bar_colors,
    width=0.8
))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

source_text = texts.get('source') or ''

max_y_val = max(y_values) if y_values else 10

fig.update_layout(
    font_family="Arial",
    title=dict(text=title_text, x=0.01, y=0.99, xanchor='left', yanchor='top'),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showticklabels=False,
        showgrid=False,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black',
        range=[min(x_values) - 0.5, max(x_values) + 0.5] if x_values else None
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        tickmode='linear',
        tick0=0,
        dtick=1,
        range=[0, max_y_val + 1],
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=2,
        linecolor='black'
    ),
    margin=dict(l=40, r=20, t=40, b=40)
)

if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0, y=-0.1,
        showarrow=False,
        xanchor='left', yanchor='top',
        align='left'
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")