import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]
    input_path = pathlib.Path(json_path)
    output_path = input_path.with_suffix('.png')

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    if not chart_data:
        print("Error: 'chart_data' is empty or missing in the JSON file.")
        sys.exit(1)

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0] if colors else None,
        name=''
    ))

    fig.update_layout(
        title={
            'text': texts.get('title'),
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        font={
            'family': "Arial",
            'size': 12,
            'color': "black"
        },
        xaxis={
            'title_text': texts.get('x_axis_title'),
            'tickangle': -90,
            'showline': True,
            'linewidth': 1,
            'linecolor': 'black'
        },
        yaxis={
            'title_text': texts.get('y_axis_title'),
            'range': [0, 120],
            'tickmode': 'linear',
            'tick0': 0,
            'dtick': 10,
            'showgrid': True,
            'gridwidth': 1,
            'gridcolor': 'black',
            'showline': True,
            'linewidth': 1,
            'linecolor': 'black'
        },
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=60, r=40, t=120, b=150)
    )

    try:
        fig.write_image(str(output_path), scale=2)
        print(f"Chart successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()