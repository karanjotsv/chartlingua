import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    data = chart_data['chart_data'][0]
    texts = chart_data['texts']
    colors = chart_data['colors']

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=data['x'],
        y=data['y'],
        text=data['y'],
        texttemplate='%{y: }',
        textposition='outside',
        marker_color=colors['series'][0],
        textfont=dict(
            family="Arial",
            color=colors['data_labels']
        ),
        cliponaxis=False
    ))

    title_text = ""
    if texts.get('title'):
        title_text += f"<b>{texts['title']}</b>"
    if texts.get('subtitle'):
        title_text += f"<br>{texts['subtitle']}"
    
    fig.update_layout(
        title_text=title_text,
        title_x=0.05,
        title_font_family="Arial",
        xaxis_title_text=texts['x_axis_title'],
        yaxis_title_text=texts['y_axis_title'],
        yaxis=dict(
            range=[0, 30000],
            tickformat=' ',
            gridcolor=colors['grid'],
            gridwidth=1,
            griddash='dot',
            dtick=5000
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        font=dict(
            family="Arial",
            color=colors['axis_titles']
        ),
        margin=dict(l=80, r=20, t=40, b=100),
        annotations=[
            dict(
                text=texts['source_left'],
                showarrow=False,
                xref="paper", yref="paper",
                x=0, y=-0.18,
                xanchor='left', yanchor='bottom',
                font=dict(
                    family="Arial",
                    color=colors['source_left']
                )
            ),
            dict(
                text=texts['source_right'],
                showarrow=False,
                xref="paper", yref="paper",
                x=1, y=-0.18,
                xanchor='right', yanchor='bottom',
                align='right',
                font=dict(
                    family="Arial",
                    color=colors['source_right']
                )
            )
        ]
    )

    output_filename_base = json_path.stem
    output_path = f"{output_filename_base}.png"
    
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()