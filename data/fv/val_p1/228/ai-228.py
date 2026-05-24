import sys
import json
from pathlib import Path
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    data = chart_data['chart_data']
    texts = chart_data['texts']
    colors = chart_data['colors']
    
    fig = go.Figure()

    categories = [d['Year'] for d in data]
    series_labels = texts['series_labels']
    marker_symbols = ['square', 'triangle-up']

    for i, series_name in enumerate(series_labels):
        y_values = [d.get(series_name) for d in data]
        fig.add_trace(go.Scatter(
            x=categories,
            y=y_values,
            name=series_name,
            mode='lines+markers',
            line=dict(color=colors[i]),
            marker=dict(symbol=marker_symbols[i], color=colors[i], size=6)
        ))

    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    fig.update_layout(
        title={
            'text': title_text,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=texts.get('x_axis_title'),
        yaxis_title=texts.get('y_axis_title'),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='black',
            showgrid=True,
            gridcolor='lightgray',
            tickmode='array',
            tickvals=list(range(1973, 2016, 2)),
            ticktext=[str(y) for y in range(1973, 2016, 2)]
        ),
        yaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='black',
            showgrid=True,
            gridcolor='lightgray',
            range=[0, 4000000000]
        ),
        legend=dict(
            x=0.98,
            y=0.7,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.5)',
            bordercolor='black',
            borderwidth=1
        ),
        margin=dict(l=80, r=40, t=80, b=80)
    )
    
    output_filename = f"{json_path.stem}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")

if __name__ == "__main__":
    main()