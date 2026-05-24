import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = chart_info['chart_data']
    texts = chart_info['texts']
    colors = chart_info['colors']

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    bar_texts = ['{:,}'.format(v).replace(',', ' ') for v in values]

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        text=bar_texts,
        textposition='outside',
        marker_color=colors[0],
        cliponaxis=False,
        textfont=dict(family="Arial")
    ))
    
    shapes = []
    for i, _ in enumerate(categories):
        if i % 2 != 0:
            shapes.append(go.layout.Shape(
                type="rect",
                xref="x",
                yref="paper",
                x0=i - 0.5,
                y0=0,
                x1=i + 0.5,
                y1=1,
                fillcolor="#f7f7f7",
                layer="below",
                line_width=0,
            ))

    fig.update_layout(
        title_text=texts.get('title') if texts.get('title') else None,
        xaxis_title=texts['x_axis_title'],
        yaxis_title=texts['y_axis_title'],
        yaxis=dict(
            range=[0, 105000],
            tickvals=[0, 20000, 40000, 60000, 80000, 100000],
            ticktext=['0', '20 000', '40 000', '60 000', '80 000', '100 000'],
            gridcolor='#e0e0e0',
            zeroline=False,
            showline=False,
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='black',
            linewidth=1,
            tickfont=dict(size=12)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12, color="black"),
        margin=dict(l=90, r=40, b=80, t=50),
        shapes=shapes,
        showlegend=False,
        annotations=[
            dict(
                text=texts['source'],
                showarrow=False,
                xref='paper', yref='paper',
                x=0.99, y=-0.22,
                xanchor='right', yanchor='bottom',
                align='right',
                font=dict(family="Arial", size=10, color="#666666")
            )
        ]
    )

    base_filename = json_path.split('/')[-1].split('.')[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Image saved to {output_filename}")

if __name__ == "__main__":
    main()