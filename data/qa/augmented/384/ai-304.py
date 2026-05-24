import sys
import json
from pathlib import Path
import plotly.graph_objects as go

def main():
    """
    Main function to generate a bar chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python recreate_chart.py <path_to_json_file>", file=sys.stderr)
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}", file=sys.stderr)
        sys.exit(1)

    output_filename_base = json_path.stem

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    chart_data = chart_info.get('chart_data', [])
    texts = chart_info.get('texts', {})
    colors = chart_info.get('colors', [])

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        text=values,
        textposition='outside',
        marker_color=colors[0] if colors else '#297ACC',
        texttemplate='<b>%{text}</b>',
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            size=12,
            color="black"
        )
    ))

    title_text = ""
    if texts.get('title'):
        title_text += f"<b>{texts['title']}</b>"
    if texts.get('subtitle'):
        title_text = f"{title_text}<br>{texts['subtitle']}" if title_text else texts['subtitle']
    
    source_text = ""
    if texts.get('source'):
        source_text += texts['source']
    if texts.get('note'):
        source_text = f"{source_text}<br>{texts['note']}" if source_text else texts['note']


    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showline=True,
            linewidth=1,
            linecolor='black',
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 300],
            dtick=50,
            showgrid=True,
            gridcolor='#E5E5E5',
            showline=False,
            tickfont=dict(size=12)
        ),
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=80, r=40, t=50, b=100),
        annotations=[
            dict(
                showarrow=False,
                text=source_text,
                xref="paper", yref="paper",
                x=0.99, y=-0.25,
                xanchor='right', yanchor='top',
                align='right',
                font=dict(size=10)
            )
        ]
    )

    output_path = f"{output_filename_base}.png"
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()