import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            name=series['name'],
            line=dict(color=colors[i], width=3),
            showlegend=False
        ))

    legend_annotations = [
        # Legend label for Precision
        dict(xref="paper", yref="paper", x=0.21, y=1.045, xanchor='left', yanchor='middle',
             text=texts['legend_labels'][0], showarrow=False, font=dict(color='white', size=12, family="Arial")),
        # Legend label for Recall
        dict(xref="paper", yref="paper", x=0.41, y=1.045, xanchor='left', yanchor='middle',
             text=texts['legend_labels'][1], showarrow=False, font=dict(color='white', size=12, family="Arial")),
        # Legend label for Filter rate
        dict(xref="paper", yref="paper", x=0.59, y=1.045, xanchor='left', yanchor='middle',
             text=texts['legend_labels'][2], showarrow=False, font=dict(color='white', size=12, family="Arial"))
    ]

    legend_shapes = [
        # Legend box for Precision
        dict(type="rect", xref="paper", yref="paper", x0=0.15, y0=1.02, x1=0.20, y1=1.07,
             line=dict(color=colors[0], width=3), fillcolor='rgba(0,0,0,0)'),
        # Legend box for Recall
        dict(type="rect", xref="paper", yref="paper", x0=0.35, y0=1.02, x1=0.40, y1=1.07,
             line=dict(color=colors[1], width=3), fillcolor='rgba(0,0,0,0)')
    ]


    fig.update_layout(
        template="plotly_dark",
        title=dict(
            text=texts['title'],
            x=0.5,
            xanchor='center',
            font=dict(size=16)
        ),
        xaxis=dict(
            title=texts['x_axis_title'],
            range=[0, 1.01],
            tickvals=[i/10 for i in range(11)],
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='gray',
            zeroline=False
        ),
        yaxis=dict(
            title=texts['y_axis_title'],
            range=[0, 1.05],
            tickvals=[i/10 for i in range(11)],
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='gray',
            zeroline=False
        ),
        font=dict(
            family="Arial",
            color="white"
        ),
        margin=dict(t=120, b=60, l=60, r=40),
        showlegend=False,
        annotations=legend_annotations,
        shapes=legend_shapes
    )

    output_filename = json_path.rsplit('.', 1)[0] + '.png'
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()