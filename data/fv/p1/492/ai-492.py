import sys
import json
import os
import plotly.graph_objects as go

# 1. Read JSON from command line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# 2. Extract data from JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', {})
layout_options = chart_info.get('layout_options', {})
trace_colors = colors.get('traces', [])

# 3. Create Figure
fig = go.Figure()

# 4. Add Traces
for i, series in enumerate(chart_data):
    color = trace_colors[i] if i < len(trace_colors) else None
    
    marker_props = series.get('marker', {})
    marker_symbol = marker_props.get('symbol', 'circle')
    
    is_open_marker = marker_symbol.endswith('-open')
    
    trace = go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode=series.get('mode', 'lines'),
        line=dict(
            color=color,
            width=series.get('line', {}).get('width', 1.5)
        ),
        marker=dict(
            color=color if not is_open_marker else 'rgba(0,0,0,0)',
            symbol=marker_symbol,
            size=marker_props.get('size', 10),
            line=dict(color=color, width=1.5)
        )
    )
    fig.add_trace(trace)

# 5. Update Layout
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    margin=dict(l=90, r=40, t=140, b=120),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5,
        traceorder="normal"
    ),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor=colors.get('grid', 'lightgrey'),
        tickmode='array',
        tickvals=layout_options.get('x_axis_tickvals'),
        ticktext=layout_options.get('x_axis_ticktext')
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        type=layout_options.get('y_axis_type', 'linear'),
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor=colors.get('grid', 'lightgrey'),
        tickmode='array',
        tickvals=layout_options.get('y_axis_tickvals'),
        ticktext=[f'{v:.1f}' for v in layout_options.get('y_axis_tickvals', [])]
    ),
    shapes=[
        dict(
            type="rect",
            xref="paper", yref="paper",
            x0=-0.01, y0=1.05, x1=1.01, y1=1.12,
            fillcolor=colors.get('header', '#006A4E'),
            line_width=0
        )
    ],
    annotations=[
        dict(
            xref="paper", yref="paper",
            x=0.01, y=1.02,
            text=f"<b>{texts.get('logo_text', '')}</b>",
            showarrow=False,
            font=dict(size=20, color=colors.get('logo_text', '#006A4E')),
            align="left",
            xanchor='left', yanchor='top',
            borderpad=10,
            bgcolor=colors.get('logo_bg', '#FFFFFF')
        ),
        dict(
            xref="paper", yref="paper",
            x=0.5, y=1.02,
            text=f"<b>{texts.get('title', '')}</b>",
            showarrow=False,
            font=dict(size=16, color='black'),
            xanchor='center', yanchor='top'
        )
    ]
)

# 6. Output image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2, width=600, height=500)

print(f"Chart saved to {output_filename}")