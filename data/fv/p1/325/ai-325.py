import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Display the value only for the first bar, as shown in the original image, and make it bold.
    bar_texts = [f"<b>{item['value']}</b>" if i == 0 else '' for i, item in enumerate(chart_data)]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=bar_texts,
        textposition='outside',
        textfont=dict(family="Arial", size=14, color='black'),
        cliponaxis=False
    ))

    title_text = f"<b>{texts.get('title', '')}</b>"
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"
        
    source_text = []
    if texts.get('source'):
        source_text.append(f"Source: {texts['source']}")
    if texts.get('notes'):
        source_text.append(f"Note: {texts['notes']}")
    caption_text = "<br>".join(source_text)


    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 60],
            dtick=10,
            showgrid=True,
            gridcolor='#E0E0E0',
            zeroline=False
        ),
        font=dict(
            family="Arial",
            size=12,
            color="#333"
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=80, r=40, t=100, b=100),
        annotations=[
            dict(
                text=caption_text,
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0,
                y=-0.2, # Adjust this value to position the caption
                xanchor='left',
                yanchor='top',
                align='left'
            )
        ] if caption_text else []
    )
    
    # Apply specific font styles
    fig.update_xaxes(title_font=dict(size=14), tickfont=dict(size=12))
    fig.update_yaxes(title_font=dict(size=14), tickfont=dict(size=12))
    fig.update_layout(title_font=dict(size=20))


    output_path = json_path.with_suffix('.png')
    fig.write_image(str(output_path), scale=2)
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()