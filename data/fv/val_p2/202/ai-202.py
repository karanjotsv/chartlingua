import sys
import json
from pathlib import Path
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    categories = chart_data['categories']
    series_data = chart_data['series']

    fig = go.Figure()

    for i, series in enumerate(series_data):
        fig.add_trace(go.Bar(
            x=categories,
            y=series['values'],
            name=series['name'],
            marker_color=colors[i]
        ))

    title_text = texts['title']
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.02,
            y=0.95,
            xanchor='left',
            yanchor='top',
            font=dict(size=18, color='#555555')
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        xaxis=dict(
            title_text=texts['x_axis_title'],
            showgrid=False,
            showline=True,
            linecolor='black',
            linewidth=1
        ),
        yaxis=dict(
            title_text=texts['y_axis_title'],
            showgrid=True,
            gridcolor='#E0E0E0',
            range=[0, 5.1],
            tickmode='linear',
            dtick=1
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        barmode='group',
        legend=dict(
            x=0.98,
            y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255,255,255,0)',
            bordercolor='rgba(255,255,255,0)'
        ),
        margin=dict(t=80, b=50, l=50, r=50)
    )
    
    if texts.get('source'):
        fig.add_annotation(
            text=texts['source'],
            xref="paper", yref="paper",
            x=0, y=-0.15,
            showarrow=False,
            xanchor='left',
            yanchor='top',
            align='left'
        )


    filename_base = json_path.stem
    output_filename = f"{filename_base}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()