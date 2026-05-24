import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Generates a pie chart from a JSON data file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
        sys.exit(1)
    
    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    data = chart_info['chart_data']
    texts = chart_info['texts']
    colors = chart_info['colors']

    labels = [item['label'] for item in data]
    values = [item['value'] for item in data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#000000', width=1)),
        textposition='outside',
        textinfo='label',
        sort=False,
        direction='clockwise',
        rotation=89,
        hoverinfo='label+percent'
    ))

    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    fig.update_layout(
        title={
            'text': title_text,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=False,
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=80, r=80, t=80, b=40)
    )
    
    fig.update_traces(
        outsidetextfont=dict(size=12, color='black')
    )

    output_filename = json_path.stem + ".png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()