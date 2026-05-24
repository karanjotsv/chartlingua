import sys
import json
import plotly.graph_objects as go
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python recreate_chart.py <path_to_json_file>")
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

    data = chart_data.get('chart_data', [])
    texts = chart_data.get('texts', {})
    colors = chart_data.get('colors', [])

    fig = go.Figure()

    for i, series in enumerate(data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines',
            name=series.get('name', ''),
            line=dict(
                color=colors[i % len(colors)],
                dash=series.get('line_style', 'solid')
            ),
            showlegend=False
        ))
    
    # Custom tick values for log axes
    x_tickvals = [0.1, 0.2, 0.3, 0.5, 0.7, 1, 2, 3, 5, 7, 10, 20, 40, 50, 70]
    y_tickvals = [0.01, 0.02, 0.1, 0.2, 1, 2, 10, 20, 100, 200, 1000, 2000]

    fig.update_layout(
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title=texts.get('x_axis_title'),
            type='log',
            tickvals=x_tickvals,
            ticktext=[str(v) for v in x_tickvals],
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks='outside',
            mirror=True,
            range=[-1, 1.85] # log10(0.1) to log10(70)
        ),
        yaxis=dict(
            title=texts.get('y_axis_title'),
            type='log',
            tickvals=y_tickvals,
            ticktext=[str(v) for v in y_tickvals],
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks='outside',
            mirror=True,
            range=[-2, 3.4] # log10(0.01) to log10(2000+ buffer)
        ),
        margin=dict(l=80, r=40, t=40, b=60),
        showlegend=False
    )
    
    # Add annotations from JSON
    if 'annotations' in texts:
        for ann in texts['annotations']:
            fig.add_annotation(
                text=ann.get('text', ''),
                x=ann.get('x'),
                y=ann.get('y'),
                xref=ann.get('xref', 'x'),
                yref=ann.get('yref', 'y'),
                showarrow=True,
                arrowhead=1,
                ax=ann.get('ax', 0),
                ay=ann.get('ay', -40),
                font=dict(size=11),
                align='left'
            )

    filename_base = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{filename_base}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()