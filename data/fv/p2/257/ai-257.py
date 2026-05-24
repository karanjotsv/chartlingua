import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Generates a chart from a JSON data file provided via command-line argument.
    """
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>", file=sys.stderr)
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing JSON file: {e}", file=sys.stderr)
        sys.exit(1)

    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']

    fig = go.Figure()

    for i, series in enumerate(chart_data['series']):
        fig.add_trace(go.Scatter(
            x=chart_data['categories'],
            y=series['y'],
            name=series['name'],
            mode='lines+markers',
            line=dict(color=colors[i]),
            marker=dict(
                symbol=series['marker_symbol'],
                color=colors[i],
                size=8
            ),
            connectgaps=False
        ))

    title_text = f"<b>{texts['title']}</b>"
    if texts.get('subtitle'):
        title_text += f"<br><span style='font-size: 14px;'>{texts['subtitle']}</span>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        xaxis=dict(
            title_text=texts['x_axis_title'],
            showline=True,
            linewidth=1,
            linecolor='black',
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title_text=texts['y_axis_title'],
            range=[0, 100],
            dtick=10,
            showline=True,
            linewidth=1,
            linecolor='black',
            gridcolor='#C0C0C0',
            zeroline=False
        ),
        legend=dict(
            x=1.02,
            y=0.8,
            xanchor='left',
            yanchor='top',
            borderwidth=1,
            bordercolor='black'
        ),
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        paper_bgcolor='white',
        plot_bgcolor='#E5E5E5',
        margin=dict(t=100, b=80, l=80, r=150)
    )

    output_filename = json_path.stem + '.png'
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()