import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Generates a chart from a JSON data file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    fig = go.Figure()

    # Add data traces
    for i, series in enumerate(chart_config['chart_data']):
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            name=series.get('series_name', ''),
            line=dict(color=chart_config['colors'][i], width=3),
            showlegend=False
        ))

    # Add annotations and shapes
    if 'annotations' in chart_config:
        for ann in chart_config['annotations']:
            if 'line' in ann:
                fig.add_shape(
                    type="line",
                    x0=ann['line']['x0'], y0=ann['line']['y0'],
                    x1=ann['line']['x1'], y1=ann['line']['y1'],
                    line=dict(
                        color=ann['line']['color'],
                        width=ann['line']['width']
                    )
                )
            fig.add_annotation(
                x=ann['x'],
                y=ann['y'],
                text=ann['text'],
                showarrow=False,
                font=dict(family="Arial", size=12),
                xanchor='center',
                yanchor='bottom',
                yshift=5
            )

    # Update layout
    texts = chart_config['texts']
    
    # Combine title and subtitle
    title_text = f"<b>{texts['title']}</b>" if texts['title'] else ""
    if texts['subtitle']:
        title_text += f"<br><span style='font-size: 12px;'>{texts['subtitle']}</span>" if title_text else texts['subtitle']

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.05,
            xanchor='left'
        ),
        xaxis=dict(
            title_text=texts['x_axis_title'],
            showgrid=False,
            zeroline=False,
            range=[1985, 2015],
            tickvals=[1985, 1990, 1995, 2000, 2005, 2010, 2015]
        ),
        yaxis=dict(
            title_text=texts['y_axis_title'],
            showgrid=True,
            gridcolor='lightgrey',
            gridwidth=1,
            zeroline=False,
            range=[0, 60],
            tickvals=[0, 15, 30, 45, 60]
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=60, r=40, t=60, b=60),
        autosize=False,
        width=800,
        height=600
    )

    # Output image
    output_path = json_path.with_suffix('.png')
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()