import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]
    base_filename = json_path.rsplit('.', 1)[0]
    output_image_path = f"{base_filename}.png"

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']
    pull = config.get('pull', [0] * len(chart_data))

    labels = [item['hover_label'] for item in chart_data]
    values = [item['value'] for item in chart_data]
    display_labels = [item['display_label'] for item in chart_data]

    pie_trace = go.Pie(
        labels=labels,
        values=values,
        text=display_labels,
        textinfo='text',
        pull=pull,
        marker=dict(colors=colors, line=dict(color='#000000', width=1)),
        sort=False,
        showlegend=False,
        insidetextfont=dict(family="Arial", color="black"),
        direction='clockwise',
        rotation=-45 # Start angle to approximate original layout
    )

    fig = go.Figure(data=[pie_trace])

    title_parts = []
    if texts.get('title'):
        title_parts.append(f"<b>{texts['title']}</b>")
    if texts.get('subtitle'):
        title_parts.append(texts['subtitle'])
    full_title = "<br>".join(title_parts)

    source_parts = []
    if texts.get('source'):
        source_parts.append(texts['source'])
    if texts.get('note'):
        source_parts.append(texts['note'])
    full_source = "<br>".join(source_parts)

    fig.update_layout(
        title_text=full_title,
        title_x=0.5,
        title_xanchor='center',
        font_family="Arial",
        margin=dict(t=60, b=60, l=40, r=40)
    )

    if full_source:
        fig.add_annotation(
            text=full_source,
            align='left',
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.1,
            xanchor='left', yanchor='top'
        )

    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")

if __name__ == "__main__":
    main()