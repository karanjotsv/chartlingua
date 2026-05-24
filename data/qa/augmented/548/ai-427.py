import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    """
    Generates a chart from a JSON data file using Plotly.
    The path to the JSON file is provided as a command-line argument.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <json_file_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    output_filename = json_path.stem + '.png'

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        sys.exit(1)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker=dict(color=colors[0]),
        text=values,
        texttemplate='%{text:.2f}',
        textposition='outside',
        cliponaxis=False,
        hoverinfo='none'
    ))
    
    # Construct title string
    title_text = ""
    if texts.get("title"):
        title_text += f'<b>{texts["title"]}</b>'
    if texts.get("subtitle"):
        title_text += f'<br><sub>{texts["subtitle"]}</sub>'

    fig.update_layout(
        title_text=title_text if title_text else None,
        title_x=0.05,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12, color='black'),
        showlegend=False,
        margin=dict(l=260, r=40, t=50, b=80),
        xaxis=dict(
            title=texts.get('x_axis_title'),
            showgrid=True,
            gridcolor='#EAEAEA',
            gridwidth=1,
            griddash='dot',
            zeroline=False,
            range=[0, max(values) * 1.25]
        ),
        yaxis=dict(
            title=texts.get('y_axis_title'),
            showgrid=False,
            zeroline=False
        )
    )

    annotations = []
    if texts.get("source"):
        annotations.append(dict(
            xref="paper", yref="paper",
            x=0.99, y=-0.14,
            text=texts['source'],
            showarrow=False,
            xanchor='right',
            yanchor='top',
            font=dict(size=10, color="#888888")
        ))
    
    if annotations:
        fig.update_layout(annotations=annotations)
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")

if __name__ == "__main__":
    main()