import sys
import json
from pathlib import Path
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    chart_data = data['chart_data']
    texts = data['texts']
    colors = data['colors']

    fig = go.Figure()

    for i, series in enumerate(chart_data['series']):
        fig.add_trace(go.Bar(
            name=series['name'],
            y=chart_data['categories'],
            x=series['data'],
            orientation='h',
            marker_color=colors[i],
            marker_line_color='black',
            marker_line_width=0.5
        ))

    annotations = []
    for i, (cat, val) in enumerate(zip(chart_data['categories'], texts['y_axis_values'])):
        annotations.append(dict(
            xref='paper',
            yref='y',
            x=0,
            y=cat,
            text=val,
            xanchor='right',
            yanchor='middle',
            showarrow=False,
            font=dict(family="Arial", size=10),
            align='right',
            xshift=-5
        ))

    title_text = texts['title']
    if texts['subtitle']:
        title_text += f"<br><sup>{texts['subtitle']}</sup>"

    fig.update_layout(
        barmode='stack',
        title_text=title_text,
        title_x=0.5,
        font_family="Arial",
        plot_bgcolor='white',
        paper_bgcolor='#f8f8f8',
        yaxis_autorange='reversed',
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=False
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=chart_data['categories'],
            ticktext=[f" {c}" for c in chart_data['categories']], # Add space for padding
            tickfont=dict(size=10)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            title=dict(
                text=texts['legend_title'],
                font=dict(size=12, family="Arial")
            ),
            traceorder='normal'
        ),
        margin=dict(l=150, r=20, t=50, b=100),
        annotations=annotations
    )
    
    output_filename = json_path.stem + ".png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()