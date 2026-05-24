import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
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

    chart_data = chart_info.get('chart_data', [])
    texts = chart_info.get('texts', {})
    colors = chart_info.get('colors', [])

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines',
            name=series.get('name', ''),
            line=dict(color=colors[i % len(colors)], width=1.5),
            showlegend=False
        ))

    fig.update_layout(
        title=dict(
            text=texts.get('title'),
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(family="Arial", size=28, color='black')
        ),
        xaxis=dict(
            title=dict(
                text=texts.get('x_axis_title'),
                font=dict(family="Arial", size=22, color='black')
            ),
            range=[-5, 255],
            tickvals=[0, 100, 200],
            tickfont=dict(family="Arial", size=20, color='black'),
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=False,
            gridcolor='white',
            zeroline=False
        ),
        yaxis=dict(
            title=dict(
                text=texts.get('y_axis_title', ''),
                font=dict(family="Arial", size=22, color='black')
            ),
            range=[-5, 15.5],
            tickvals=[-5, 0, 5, 10, 15],
            tickfont=dict(family="Arial", size=20, color='black'),
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=False,
            gridcolor='white',
            zeroline=False
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=70, r=30, t=100, b=80)
    )

    base_name = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_name}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()