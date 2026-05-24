import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Generates a Plotly chart from a JSON data file specified via command-line argument.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    output_filename = json_path.stem + ".png"

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing JSON file: {e}")
        sys.exit(1)

    chart_data = chart_config.get("chart_data", [])
    texts = chart_config.get("texts", {})
    colors = chart_config.get("colors", [])
    categories = chart_config.get("categories", [])

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        color_set = colors[i] if i < len(colors) else 'blue'
        style = series.get("style", {})
        
        marker_properties = {}
        if style.get("type") == "dotted_outline":
            marker_properties = {
                'color': color_set,
                'line': {
                    'color': 'black',
                    'width': 1.5,
                    'dash': 'dot'
                }
            }
        else: # Default to solid bars
            marker_properties = {'color': color_set}
        
        fig.add_trace(go.Bar(
            name=series.get('name', f'Series {i+1}'),
            x=categories,
            y=series.get('y', []),
            marker=marker_properties,
            showlegend=False
        ))

    # Construct title
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

    fig.update_layout(
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center'
        },
        barmode='group',
        xaxis={
            'title_text': texts.get('x_axis_title'),
            'categoryorder': 'array',
            'categoryarray': categories,
            'showgrid': False,
            'zeroline': False
        },
        yaxis={
            'title_text': texts.get('y_axis_title'),
            'range': [0, 60],
            'showgrid': True,
            'gridcolor': 'lightgrey',
            'zeroline': False
        },
        font={
            'family': "Arial",
            'size': 12
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=60, r=40, t=80, b=80),
        bargap=0.15,
        bargroupgap=0.1
    )

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()