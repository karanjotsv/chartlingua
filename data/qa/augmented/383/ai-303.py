import sys
import json
import plotly.graph_objects as go

def main():
    """
    Generates a bar chart from a JSON data file.
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_filepath = sys.argv[1]
    output_image_path = json_filepath.rsplit('.', 1)[0] + '.png'

    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_filepath}")
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    fig = go.Figure()

    if not chart_data:
        print("Warning: 'chart_data' is empty. Generating an empty chart.")
    else:
        x_values = [d['x'] for d in chart_data]
        y_values = [d['y'] for d in chart_data]

        bar_texts = [f'{y}%' if y == int(y) else f'{y:.1f}%' for y in y_values]

        fig.add_trace(go.Bar(
            x=x_values,
            y=y_values,
            marker_color=colors[0] if colors else '#2672C7',
            text=bar_texts,
            textposition='outside',
            textfont=dict(family="Arial", size=12, color='black'),
            cliponaxis=False
        ))

    fig.update_layout(
        font=dict(family="Arial", size=12, color="black"),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 80],
            dtick=10,
            ticksuffix='%',
            gridcolor='#E5E5E5',
            zeroline=False,
            showline=False
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            tickfont=dict(size=12)
        ),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=80, r=40, t=40, b=120),
        annotations=[
            dict(
                text=texts.get('note', ''),
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0,
                y=-0.2,
                xanchor='left',
                yanchor='top',
                font=dict(color='#3779B2', size=12)
            ),
            dict(
                text=texts.get('source', ''),
                align='right',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1,
                y=-0.2,
                xanchor='right',
                yanchor='top',
                font=dict(color='#666666', size=12)
            )
        ]
    )

    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")

if __name__ == "__main__":
    main()