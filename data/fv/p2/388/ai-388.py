import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Generates a chart from a JSON data file specified as a command-line argument.
    """
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file at '{json_path}'")
        sys.exit(1)

    fig = go.Figure()

    # Add data series
    chart_data = config.get('chart_data', [])
    colors = config.get('colors', [])
    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            name=series.get('name', ''),
            mode=series.get('mode', 'lines'),
            line=dict(
                color=colors[i] if i < len(colors) else None,
                width=3,
                dash=series.get('line', {}).get('dash', 'solid')
            ),
            showlegend=series.get('showlegend', True)
        ))

    # Configure layout
    texts = config.get('texts', {})
    fig.update_layout(
        font_family="Arial",
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        xaxis=dict(
            visible=False,
            range=[0, 100]
        ),
        yaxis=dict(
            visible=False,
            range=[0, 100]
        ),
        showlegend=True,
        legend=dict(
            x=0.98,
            y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)',
            font=dict(
                color='#FFFFFF'
            )
        ),
        margin=dict(l=5, r=5, t=5, b=5),
        shapes=config.get('shapes', []),
        annotations=texts.get('annotations', [])
    )

    # Generate output filename and save the image
    filename_base = json_path.stem
    output_filename = f"{filename_base}.png"
    
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart successfully saved to '{output_filename}'")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()