import sys
import json
from pathlib import Path
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(sys.argv[0]).name} <json_file_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines+markers',
            name=series.get('name', ''),
            line=dict(color=colors[i % len(colors)]),
            marker=dict(
                symbol='diamond',
                color=colors[i % len(colors)],
                size=8
            )
        ))

    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            font=dict(size=18)
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0.60, 0.86],
            tickformat=',.2%',
            dtick=0.05,
            gridcolor='#cccccc',
            gridwidth=1,
            zeroline=False
        ),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=80, r=40, t=80, b=80),
        separators='.,'
    )

    output_filename = json_path.stem + ".png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()