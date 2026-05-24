import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{json_path}' is not a valid JSON.")
        sys.exit(1)

    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']

    fig = go.Figure()

    suffix = texts.get('data_labels_suffix', '')

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Bar(
            name=series['name'],
            x=series['x'],
            y=series['y'],
            marker_color=colors[i],
            text=[f"<b>{val}</b>{suffix}" for val in series['y']],
            textposition='auto',
            textfont=dict(family="Arial", size=14, color='black'),
            insidetextfont=dict(family="Arial", size=14, color='white'),
            cliponaxis=False
        ))

    fig.update_layout(
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12, color='#333333'),
        yaxis=dict(
            title=texts.get('yaxis_title'),
            range=[0, 105],
            dtick=20,
            ticksuffix='%',
            showgrid=True,
            gridcolor='#e0e0e0',
            zeroline=False,
            showline=False
        ),
        xaxis=dict(
            title=texts.get('xaxis_title'),
            showline=False,
            tickfont=dict(size=14)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        ),
        margin=dict(l=80, r=40, t=40, b=150),
        shapes=[
            go.layout.Shape(
                type="rect", xref="x", yref="paper",
                x0=-0.5, y0=0, x1=0.5, y1=1,
                fillcolor="#F8F8F8", layer="below", line_width=0
            ),
            go.layout.Shape(
                type="rect", xref="x", yref="paper",
                x0=1.5, y0=0, x1=2.5, y1=1,
                fillcolor="#F8F8F8", layer="below", line_width=0
            )
        ]
    )

    if texts.get('source'):
        fig.add_annotation(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper', yref='paper',
            x=1, y=-0.28,
            xanchor='right', yanchor='bottom',
            font=dict(size=12)
        )

    base_filename = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    # This structure is used to avoid defining functions at the top level as requested,
    # but still allows for clean execution.
    main()