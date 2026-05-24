import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        text=values,
        texttemplate='%{text:.1f}%',
        textposition='outside',
        marker_color=colors[0] if colors else None,
        cliponaxis=False 
    ))

    title_text = texts.get('title') if texts.get('title') else ''
    subtitle_text = texts.get('subtitle') if texts.get('subtitle') else ''

    full_title = ""
    if title_text:
        full_title += f"<b>{title_text}</b>"
    if subtitle_text:
        if full_title:
            full_title += "<br>"
        full_title += f"{subtitle_text}"

    fig.update_layout(
        title={
            'text': full_title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis={
            'title': texts.get('y_axis_title', ''),
            'range': [0, 50],
            'ticksuffix': '%',
            'showgrid': True,
            'gridcolor': '#E0E0E0'
        },
        xaxis={
            'title': texts.get('x_axis_title', ''),
            'tickangle': 0
        },
        font={
            'family': "Arial",
            'size': 12
        },
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=80, r=40, t=80, b=180),
        annotations=[
            dict(
                text=texts.get('source', ''),
                showarrow=False,
                xref="paper",
                yref="paper",
                x=1,
                y=-0.38,
                xanchor='right',
                yanchor='bottom',
                align='right'
            )
        ]
    )

    output_path = json_path.with_suffix('.png')
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()