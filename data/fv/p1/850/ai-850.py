import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Generates a chart from a JSON data file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', {})

    fig = go.Figure()

    for series in chart_data:
        name = series.get('name')
        series_type = series.get('type')
        
        if series_type == 'scatter':
            fig.add_trace(go.Scatter(
                x=series.get('x'),
                y=series.get('y'),
                name=name,
                mode=series.get('mode'),
                marker=dict(
                    symbol='triangle-up' if 'Median' in name else 'square',
                    color='rgba(0,0,0,0)' if 'Median' in name else colors.get(name),
                    size=12 if 'Median' in name else 10,
                    line=dict(
                        color=colors.get(name),
                        width=2 if 'Median' in name else 1.5
                    )
                ) if 'Median' in name else dict(
                    symbol='square',
                    color=colors.get(name),
                    size=10,
                    line=dict(color='white', width=1.5)
                )
            ))
        elif series_type == 'line':
             fig.add_trace(go.Scatter(
                x=series.get('x'),
                y=series.get('y'),
                name=name,
                mode='lines',
                line=dict(color=colors.get(name), width=2)
            ))
        elif series_type == 'line_segment':
             fig.add_trace(go.Scatter(
                x=series.get('x'),
                y=series.get('y'),
                name=name,
                mode='lines',
                line=dict(color=colors.get(name), width=2.5)
            ))
        elif series_type == 'line_bar':
            fig.add_trace(go.Scatter(
                x=series.get('x'),
                y=series.get('y'),
                name=name,
                mode='lines',
                line=dict(color=colors.get(name), width=10)
            ))

    # X-axis ticks
    tickvals = [f"2011-08-{d}" for d in range(25, 32)] + [f"2011-09-0{d}" for d in range(1, 3)]
    ticktext = [
        "Aug<br>25<br>2011", "Aug<br>26<br>2011", "Aug<br>27<br>2011",
        "Aug<br>28<br>2011", "Aug<br>29<br>2011", "Aug<br>30<br>2011",
        "Aug<br>31<br>2011", "Sep<br>01<br>2011", "Sep<br>02<br>2011"
    ]

    fig.update_layout(
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        title=dict(
            text=texts.get('title'),
            y=0.94,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=16)
        ),
        xaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            tickvals=tickvals,
            ticktext=ticktext,
            range=["2011-08-24 18:00", "2011-09-02 06:00"]
        ),
        yaxis=dict(
            title=texts.get('y_axis_title'),
            type='log',
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgrey',
            tickvals=[30, 100, 1000, 10000, 100000, 200000],
            ticktext=['30', '100', '1000', '10000', '100000', '200000'],
            range=[1.4, 5.4],
            minor=dict(showgrid=True, gridcolor='#f0f0f0')
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.35,
            xanchor="center",
            x=0.5,
            traceorder="normal"
        ),
        margin=dict(l=80, r=40, b=180, t=120, pad=4),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=1,
                x1=1,
                y1=1.1,
                fillcolor=colors.get('header_bg'),
                layer="below",
                line_width=0,
            )
        ],
        annotations=[
            dict(
                xref="paper",
                yref="paper",
                x=0.05,
                y=1.05,
                xanchor='left',
                yanchor='middle',
                text=f"<b>{texts.get('usgs_header')}</b>",
                showarrow=False,
                font=dict(size=24, color=colors.get('header_text'), family="Arial Black")
            )
        ]
    )

    output_filename = json_path.stem + ".png"
    fig.write_image(output_filename, scale=2, width=600, height=500)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    main()