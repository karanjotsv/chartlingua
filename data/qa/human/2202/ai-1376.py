import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Generates a stacked horizontal bar chart from a JSON data file.
    Usage: python script.py <path_to_json_file>
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    output_png_path = json_path.with_suffix(".png")

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    chart_data = chart_info['chart_data']
    texts = chart_info['texts']
    colors = chart_info['colors']

    fig = go.Figure()

    for i, series in enumerate(chart_data['series']):
        text_font_colors = ['black' if v == 0 else 'white' for v in series['data']]
        
        fig.add_trace(go.Bar(
            y=chart_data['categories'],
            x=series['data'],
            name=series['name'],
            orientation='h',
            marker=dict(
                color=colors[i],
                line=dict(color='white', width=2)
            ),
            texttemplate='%{x}%',
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(
                family="Arial",
                color=text_font_colors,
                size=12,
                weight='bold'
            ),
            hoverinfo='skip'
        ))

    fig.update_layout(
        barmode='stack',
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=180, r=20, t=30, b=100),
        xaxis=dict(
            title=texts.get('x_axis_title'),
            title_standoff=15,
            range=[0, 100],
            tickvals=[0, 20, 40, 60, 80, 100],
            ticktext=[f"{v}%" for v in [0, 20, 40, 60, 80, 100]],
            showgrid=True,
            gridcolor='#e0e0e0',
            zeroline=False,
            showline=False,
            ticks='',
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            autorange='reversed'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.3,
            xanchor='center',
            x=0.5,
            traceorder='normal',
            font=dict(size=14)
        ),
        showlegend=True
    )
    
    if texts.get('source'):
        fig.add_annotation(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.35,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )

    fig.write_image(str(output_png_path), scale=2)
    print(f"Chart saved to {output_png_path}")

if __name__ == "__main__":
    main()