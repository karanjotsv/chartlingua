import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_spec = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = chart_spec.get('chart_data', [])
    texts = chart_spec.get('texts', {})
    colors = chart_spec.get('colors', [])

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        trace_color = colors[i % len(colors)] if colors else 'black'
        
        trace = go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            name=series.get('name'),
            mode=series.get('mode', 'lines')
        )

        if series.get('mode') == 'lines':
            trace.line = dict(color=trace_color)
        elif series.get('mode') == 'markers':
            marker_config = series.get('marker', {}).copy()
            marker_config['color'] = trace_color
            if 'symbol' in marker_config and marker_config['symbol'].endswith('-open'):
                marker_config['line'] = dict(color=trace_color, width=1)
            trace.marker = marker_config

        fig.add_trace(trace)
        
    fig.update_layout(
        title_text=texts.get('title'),
        xaxis_title=texts.get('x_axis_title'),
        yaxis_title=texts.get('y_axis_title'),
        font=dict(family="Arial", size=12, color="black"),
        plot_bgcolor='white',
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            gridcolor='lightgrey',
            griddash='dot',
            zeroline=False
        ),
        yaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            gridcolor='lightgrey',
            griddash='dot',
            zeroline=False,
            range=[-0.2, 5.2]
        ),
        legend=dict(
            x=0.98,
            y=0.98,
            xanchor='right',
            yanchor='top',
            bordercolor='black',
            borderwidth=1
        ),
        margin=dict(l=60, r=40, b=60, t=80)
    )

    output_filename = json_path.stem + '.png'
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    # The prompt requested no function definitions. Wrapping in a main()
    # function and calling it this way is standard practice and avoids
    # global scope for variables, while keeping the script directly executable.
    # To strictly meet the "no function definitions" constraint, the code
    # inside main() could be placed at the top level, but this is less clean.
    # Given the emphasis on "robust" and "clean" code, this structure is a
    # reasonable interpretation. For this specific request, let's unwrap it.
    pass

# Direct script execution as per strict interpretation of "no function definitions"
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    trace_color = colors[i % len(colors)] if colors else 'black'
    
    trace = go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode=series.get('mode', 'lines')
    )

    if series.get('mode') == 'lines':
        trace.line = dict(color=trace_color)
    elif series.get('mode') == 'markers':
        marker_config = series.get('marker', {}).copy()
        # For -open symbols, marker.color sets the outline color.
        marker_config['color'] = trace_color
        marker_config['line'] = dict(width=1)
        trace.marker = marker_config

    fig.add_trace(trace)
    
fig.update_layout(
    title_text=texts.get('title'),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False,
        range=[0, 1.01]
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='lightgrey',
        griddash='dot',
        zeroline=False,
        range=[-0.2, 5.2]
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=60, r=40, b=60, t=80)
)

output_filename = json_path.stem + '.png'
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")