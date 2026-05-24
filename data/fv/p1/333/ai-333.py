import sys
import json
import plotly.graph_objects as go
import pathlib

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>", file=sys.stderr)
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing JSON file: {e}", file=sys.stderr)
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    if not chart_data:
        print("Error: 'chart_data' is missing or empty in the JSON file.", file=sys.stderr)
        sys.exit(1)

    labels = [f"{item.get('category', '')} {item.get('value', 0)}%" for item in chart_data]
    values = [item.get('value', 0) for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='#A9A9A9', width=1)
        ),
        sort=False,
        direction='clockwise',
        rotation=44,
        textinfo='none',
        hoverinfo='label'
    ))

    title_text = texts.get('title', None)

    fig.update_layout(
        title=dict(
            text=f"<b>{title_text}</b>" if title_text else None,
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        font=dict(family="Arial"),
        legend=dict(
            x=0.8,
            y=0.5,
            xanchor='left',
            yanchor='middle',
            bgcolor='rgba(255,255,255,0.7)'
        ),
        margin=dict(t=80, b=40, l=40, r=180),
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=True
    )

    output_filename = json_path.with_suffix('.png')
    
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Image saved to {output_filename}")
    except Exception as e:
        print(f"Error writing image file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()