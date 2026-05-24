import sys
import json
import plotly.graph_objects as go
import os

def create_chart(json_path):
    """
    Creates a chart from a JSON file and saves it as a PNG image.
    """
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']

    categories = [item['category'] for item in data]
    values = [item['value'] for item in data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0],
        text=values,
        textposition='outside',
        texttemplate='%{text}',
        cliponaxis=False,
        hoverinfo='none'
    ))

    # Construct combined title string if subtitle exists
    title_text = texts.get('title')
    if texts.get('subtitle'):
        title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}" if texts.get('title') else texts['subtitle']

    fig.update_layout(
        font_family="Arial",
        title_text=title_text,
        title_x=0.05,
        title_font_size=20,
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=12),
            title_font=dict(size=14)
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            showgrid=True,
            gridcolor='#e5e5e5',
            zeroline=False,
            range=[0, 3000],
            dtick=500,
            tickfont=dict(size=12),
            title_font=dict(size=14)
        ),
        margin=dict(l=90, r=40, t=60, b=100),
        annotations=[
            dict(
                showarrow=False,
                text=texts.get('source', ''),
                xref='paper',
                yref='paper',
                x=1.0,
                y=-0.20,
                xanchor='right',
                yanchor='top',
                align='right',
                font=dict(size=12, color='#666666')
            )
        ]
    )
    
    fig.update_traces(textfont_size=12)

    # Generate output filename from JSON path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
        sys.exit(1)
    
    # Wrap the script execution in a function for clarity
    create_chart(sys.argv[1])