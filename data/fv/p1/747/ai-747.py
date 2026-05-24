import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Initialize Figure ---
fig = go.Figure()
shapes = []
annotations = []

# --- 3. Add data traces ---
for series in chart_data['chart_data']:
    if series['mode'] == 'lines':
        trace = go.Scatter(
            x=series['x'],
            y=series['y'],
            mode=series['mode'],
            name=series['name'],
            line=dict(color=series['line_color'], width=2)
        )
    elif series['mode'] == 'markers':
        trace = go.Scatter(
            x=series['x'],
            y=series['y'],
            mode=series['mode'],
            name=series['name'],
            marker=dict(
                symbol=series['marker_symbol'],
                color=series['marker_color'],
                size=series['marker_size'],
                line=dict(
                    color=series['marker_line_color'],
                    width=series['marker_line_width']
                )
            )
        )
    fig.add_trace(trace)

# --- 4. Handle special elements ---
# Header banner
banner_color = chart_data['special_elements']['header_banner']['color']
shapes.append(
    dict(
        type="rect",
        xref="paper", yref="paper",
        x0=0, y0=0.92, x1=1, y1=1,
        fillcolor=banner_color,
        layer="below",
        line_width=0
    )
)
# Add USGS text on the banner
annotations.append(
    dict(
        xref="paper", yref="paper",
        x=0.03, y=0.96,
        text="<b>USGS</b>",
        showarrow=False,
        font=dict(family="Arial", size=24, color="white"),
        xanchor="left", yanchor="middle"
    )
)

# "Period of approved data" visual element and legend entry
approved_data_info = chart_data['special_elements']['approved_data_period']
y0 = approved_data_info['y_value'] - approved_data_info['height'] / 2
y1 = approved_data_info['y_value'] + approved_data_info['height'] / 2
shapes.append(
    dict(
        type="rect",
        xref="paper", yref="y",
        x0=0, y0=y0, x1=1, y1=y1,
        fillcolor=approved_data_info['color'],
        layer="below",
        line_width=0
    )
)

# Add a dummy trace for the legend of "Period of approved data"
fig.add_trace(go.Scatter(
    x=[None], y=[None],
    mode='lines',
    name=approved_data_info['name'],
    line=dict(color=approved_data_info['color'], width=10)
))

# --- 5. Configure Layout ---
layout_opts = chart_data['layout_options']
texts = chart_data['texts']

fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.90,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=14)
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        type=layout_opts['y_axis_type'],
        tickvals=layout_opts['y_axis_tickvals'],
        range=layout_opts['y_axis_range_log'],
        gridcolor='#D3D3D3',
        zeroline=False
    ),
    xaxis=dict(
        tickvals=texts['x_axis_tickvals'],
        ticktext=texts['x_axis_ticktext'],
        showgrid=True,
        gridcolor='#D3D3D3',
        zeroline=False,
        tickfont=dict(size=10)
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.3, # Pushed down to avoid overlap
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    shapes=shapes,
    annotations=annotations,
    margin=dict(l=80, r=20, t=100, b=150),
    autosize=False,
    width=700,
    height=550
)

# --- 6. Write output image ---
output_filename = json_path.with_suffix(".png")
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")