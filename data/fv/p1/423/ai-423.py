import sys
import json
import plotly.graph_objects as go
import math

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    color = colors[i]
    trace_args = {
        'x': series['x'],
        'y': series['y'],
        'name': series['name'],
        'mode': series.get('mode', 'lines')
    }

    if 'lines' in trace_args['mode']:
        trace_args['line'] = dict(
            color=color,
            width=series.get('line_width', 1)
        )
    if 'markers' in trace_args['mode']:
        trace_args['marker'] = dict(
            color=color,
            symbol=series.get('marker_symbol', 'circle'),
            size=series.get('marker_size', 8),
            line=dict(
                width=series.get('marker_line_width', 0),
                color=series.get('marker_line_color', 'black')
            )
        )
    fig.add_trace(go.Scatter(**trace_args))

fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.93,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        type='log',
        range=[math.log10(25), math.log10(8000)],
        tickvals=[30, 100, 1000, 7000],
        ticktext=['30', '100', '1000', '7000'],
        showline=True,
        linewidth=2,
        linecolor='black',
        showgrid=True,
        gridcolor='lightgray',
        griddash='dot'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        range=['2017-02-23T20:00:00', '2017-02-27T04:00:00'],
        tickformat='%H:%M<br>%b %d<br>%Y',
        dtick=12 * 60 * 60 * 1000, # Ticks every 12 hours
        showline=True,
        linewidth=2,
        linecolor='black',
        showgrid=True,
        gridcolor='lightgray'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.55,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=90, r=40, t=120, b=200),
    shapes=[
        dict(
            type="rect",
            xref="paper",
            yref="paper",
            x0=0,
            y0=1,
            x1=1,
            y1=1.09,
            fillcolor="#006A4D",
            line=dict(width=0)
        )
    ]
)

# Derive output filename from the input JSON path
base_name = json_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")