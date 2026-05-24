import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    subplot_titles = [
        chart_data['texts']['panel_a_title'],
        chart_data['texts']['panel_b_title'],
        chart_data['texts']['panel_c_title']
    ]

    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=subplot_titles,
        horizontal_spacing=0.08
    )

    color = chart_data['colors'][0]

    for i, panel in enumerate(chart_data['chart_data']):
        subplot_idx = i + 1
        for series in panel.get('series', []):
            fig.add_trace(go.Scatter(
                x=series['x'],
                y=series['y'],
                mode='lines',
                line=dict(
                    color=color,
                    dash=series['line']['dash'],
                    width=1.5
                ),
                showlegend=False
            ), row=1, col=subplot_idx)

        for ann in panel.get('annotations', []):
            fig.add_annotation(
                x=ann['x'],
                y=ann['y'],
                text=ann['text'],
                showarrow=ann.get('showarrow', False),
                font=dict(family="Arial", size=12),
                xref=f"x{subplot_idx}",
                yref=f"y{subplot_idx}",
                xanchor=ann.get('xanchor', 'center'),
                yanchor='top',
                ax=ann.get('ax', 0),
                ay=ann.get('ay', 0)
            )

        fig.update_xaxes(
            range=panel['x_range'],
            visible=False,
            row=1,
            col=subplot_idx
        )
        fig.update_yaxes(
            range=panel['y_range'],
            visible=False,
            row=1,
            col=subplot_idx
        )

    fig.update_layout(
        height=300,
        width=1000,
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=100),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Position subplot titles below the plots
    for i in fig['layout']['annotations']:
        i['y'] = -0.3
        i['yanchor'] = 'top'


    base_filename = pathlib.Path(json_path).stem
    output_filename = f"{base_filename}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    main()