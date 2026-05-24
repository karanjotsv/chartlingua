import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Generates a chart from a JSON data file using Plotly.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    output_filename = json_path.stem + ".png"

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Bar(
            x=series['x_values'],
            y=series['y_values'],
            marker_color=colors[i % len(colors)],
            name=''  # No legend item
        ))

    # Construct title string
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        xaxis=dict(
            title=texts.get('x_axis_title'),
            showgrid=False,
            showline=True,
            linecolor='black',
            linewidth=1,
            zeroline=False
        ),
        yaxis=dict(
            title=texts.get('y_axis_title'),
            range=[0, 60],
            dtick=10,
            showgrid=True,
            gridcolor='lightgrey',
            showline=False,
            zeroline=False
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=80, b=80)
    )
    
    # Add the vertical tick mark between categories
    # It seems to be part of the axis styling in the original chart.
    # We can replicate this with a shape.
    fig.add_shape(
        type="line",
        xref="x",
        yref="y",
        x0=0.5,
        y0=0,
        x1=0.5,
        y1=60,
        line=dict(
            color="lightgrey",
            width=1
        ),
        layer="below"
    )


    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()