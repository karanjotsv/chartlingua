import sys
import json
import plotly.graph_objects as go
import pathlib

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}", file=sys.stderr)
    sys.exit(1)

output_image_path = json_file_path.with_suffix('.png')

# --- 2. Load and Parse JSON Data ---
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# --- 3. Create Figure and Traces ---
fig = go.Figure()

for i, series in enumerate(chart_data):
    trace_properties = {
        'x': series.get('x'),
        'y': series.get('y'),
        'mode': series.get('mode', 'markers'),
        'showlegend': False
    }

    if 'markers' in trace_properties['mode']:
        trace_properties['marker'] = {
            'color': colors[i],
            'size': series.get('marker', {}).get('size', 8)
        }

    if 'lines' in trace_properties['mode']:
        trace_properties['line'] = {
            'color': colors[i],
            'width': 2
        }

    if 'text' in series:
        trace_properties['text'] = series['text']
        trace_properties['textposition'] = series.get('textposition', 'top center')
        trace_properties['textfont'] = {'family': 'Arial', 'size': 14, 'color': 'black'}
        trace_properties['dx'] = series.get('text_dx', 0)

    fig.add_trace(go.Scatter(**trace_properties))

# --- 4. Configure Layout ---
fig.update_layout(
    title={
        'text': f"<b>{texts['title']}</b>",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'family': 'Arial', 'size': 20}
    },
    xaxis={
        'title': {'text': texts['x_axis_title'], 'font': {'family': 'Arial', 'size': 14}},
        'range': [0, 120000],
        'tickvals': [0, 30000, 60000, 90000, 120000],
        'ticktext': ['$0', '$30,000', '$60,000', '$90,000', '$120,000'],
        'showgrid': False,
        'zeroline': False,
        'showline': True,
        'mirror': True,
        'linecolor': 'black',
        'ticks': 'outside'
    },
    yaxis={
        'title': {'text': f"<b>{texts['y_axis_title']}</b>", 'font': {'family': 'Arial', 'size': 14}},
        'range': [0, 105],
        'tickvals': list(range(0, 101, 10)),
        'showgrid': True,
        'gridcolor': 'lightgrey',
        'zeroline': False,
        'showline': True,
        'mirror': True,
        'linecolor': 'black',
        'ticks': 'outside'
    },
    annotations=[
        {
            'text': texts['source'],
            'showarrow': False,
            'xref': 'paper',
            'yref': 'paper',
            'x': 0,
            'y': -0.2,
            'xanchor': 'left',
            'yanchor': 'top',
            'align': 'left',
            'font': {'family': 'Arial', 'size': 12}
        }
    ],
    plot_bgcolor='white',
    paper_bgcolor='white',
    font={'family': 'Arial', 'color': 'black'},
    margin={'l': 120, 'r': 40, 't': 80, 'b': 100},
)

# --- 5. Save Output Image ---
fig.write_image(str(output_image_path), scale=2)
print(f"Chart saved to {output_image_path}")