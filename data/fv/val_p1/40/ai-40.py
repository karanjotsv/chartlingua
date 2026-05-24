import sys
import json
import plotly.graph_objects as go
import os

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)

    data = chart_data['chart_data']
    texts = chart_data['texts']
    colors = chart_data['colors']

    y_categories = [d['category'] for d in data]
    x_values = [d['value'] for d in data]
    label_colors = [d['label_color'] for d in data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=[i for i, _ in enumerate(y_categories)],
        x=x_values,
        orientation='h',
        marker=dict(color=colors['bar']),
        hoverinfo='none',
        cliponaxis=False
    ))

    annotations = []
    for i, (value, color) in enumerate(zip(x_values, label_colors)):
        annotations.append(
            go.layout.Annotation(
                x=value,
                y=i,
                text=f'{value:,}',
                showarrow=False,
                xanchor='left',
                xshift=5,
                font=dict(
                    family="Arial",
                    size=12,
                    color=color
                )
            )
        )

    title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

    fig.update_layout(
        title=dict(
            text=title_text,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        xaxis=dict(
            title=texts['x_axis_title'],
            showgrid=True,
            gridcolor=colors['grid'],
            zeroline=False,
            tickvals=[0, 200000, 400000, 600000, 800000, 1000000],
            ticktext=['0', '200 k', '400 k', '600 k', '800 k', '1 M'],
            range=[0, max(x_values) * 1.15]
        ),
        yaxis=dict(
            showticklabels=True,
            tickmode='array',
            tickvals=[i for i, _ in enumerate(y_categories)],
            ticktext=y_categories,
            autorange='reversed'
        ),
        font=dict(family="Arial", size=12),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        showlegend=False,
        margin=dict(l=350, r=100, t=100, b=50),
        annotations=annotations
    )
    
    base_filename, _ = os.path.splitext(os.path.basename(json_path))
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()