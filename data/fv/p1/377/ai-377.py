import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Main function to generate the chart.
    """
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <path_to_json_file>", file=sys.stderr)
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at '{json_path}'", file=sys.stderr)
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    chart_data = chart_info.get('chart_data', [])
    texts = chart_info.get('texts', {})
    colors = chart_info.get('colors', [])

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            name=series.get('name'),
            mode='lines',
            line=dict(color=colors[i % len(colors)], width=2.5)
        ))

    fig.update_layout(
        title=dict(
            text=texts.get('title'),
            x=0.5,
            font=dict(size=18)
        ),
        xaxis_title=texts.get('x_axis_title'),
        yaxis_title=texts.get('y_axis_title'),
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            x=0.05,
            y=0.75,
            xanchor='left',
            yanchor='top',
            bgcolor='white',
            bordercolor='black',
            borderwidth=1
        ),
        margin=dict(l=80, r=40, t=80, b=80),
        xaxis=dict(
            range=[-4.2, 4.2],
            tickmode='array',
            tickvals=[-4, -2, 0, 2, 4],
            showline=True,
            linewidth=1.5,
            linecolor='black',
            mirror=True,
            gridcolor='#f0f0f0'
        ),
        yaxis=dict(
            range=[-0.05, 1.05],
            tickmode='array',
            tickvals=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            tickformat=".1f",
            showline=True,
            linewidth=1.5,
            linecolor='black',
            mirror=True,
            gridcolor='#f0f0f0'
        )
    )

    output_filename = f"{json_path.stem}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()