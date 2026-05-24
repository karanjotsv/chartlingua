import sys
import json
import os
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

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

    x_values = [d['x'] for d in chart_data]
    y_values = [d['y'] for d in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        line=dict(color=colors[0], width=2.5),
        marker=dict(color=colors[0], size=7),
        showlegend=False
    ))

    annotations = []
    for point in chart_data:
        if point.get('label'):
            y_anchor = 'bottom' if point['label_pos'] == 'above' else 'top'
            y_shift = 10 if point['label_pos'] == 'above' else -10
            annotations.append(
                go.layout.Annotation(
                    x=point['x'],
                    y=point['y'],
                    text=point['label'],
                    showarrow=False,
                    font=dict(family="Arial", size=12, color="#333"),
                    xanchor='center',
                    yanchor=y_anchor,
                    yshift=y_shift
                )
            )
            
    if texts.get('source'):
        annotations.append(go.layout.Annotation(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.18,
            xanchor='right',
            yanchor='top'
        ))

    if texts.get('note'):
        annotations.append(go.layout.Annotation(
            text=texts['note'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.01,
            y=-0.18,
            xanchor='left',
            yanchor='top'
        ))

    fig.update_layout(
        annotations=annotations,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12, color="#333"),
        margin=dict(l=80, r=40, t=40, b=100),
        xaxis=dict(
            showgrid=False,
            tickmode='array',
            tickvals=x_values,
            ticktext=[str(x) for x in x_values],
            tickangle=0,
            linecolor='lightgrey'
        ),
        yaxis=dict(
            title=texts.get('y_axis_title'),
            showgrid=True,
            gridcolor='#E5E7EB',
            gridwidth=1,
            range=[34000, 46000],
            tickformat=" ",
            linecolor='lightgrey'
        )
    )

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()