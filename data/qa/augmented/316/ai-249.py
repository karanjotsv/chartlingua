import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_file_path = Path(sys.argv[1])
    if not json_file_path.is_file():
        print(f"Error: JSON file not found at '{json_file_path}'")
        sys.exit(1)

    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]
    bar_texts = [str(item['value']) for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        text=bar_texts,
        textposition='outside',
        marker_color=colors[0],
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

    y_tick_values = list(range(0, 12001, 2000))
    y_tick_labels = [f'{v:,}'.replace(',', ' ') for v in y_tick_values]

    fig.update_layout(
        font=dict(family="Arial"),
        plot_bgcolor='white',
        showlegend=False,
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            ticks='outside',
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 12000],
            tickvals=y_tick_values,
            ticktext=y_tick_labels,
            gridcolor='#e0e0e0',
            zeroline=False,
            showline=False,
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        margin=dict(t=50, r=30, b=100, l=90)
    )

    annotations = []
    if texts.get('source'):
        annotations.append(
            dict(
                text=texts['source'],
                align='right',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1,
                y=-0.18,
                xanchor='right',
                yanchor='top',
                font=dict(size=12)
            )
        )
    
    fig.update_layout(annotations=annotations)


    output_path = json_file_path.with_suffix(".png")
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()