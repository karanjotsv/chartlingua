import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Main function to generate the chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    categories = config['categories']
    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=categories,
            y=series['y'],
            name=series['name'],
            mode='lines',
            line=dict(color=colors[i], width=2)
        ))

    fig.update_layout(
        title_text=texts['title'],
        title_x=0.5,
        yaxis_title_text=texts['y_axis_title'],
        xaxis_title_text=texts['x_axis_title'],
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=80, r=40, t=80, b=120),
        xaxis=dict(
            tickmode='array',
            tickvals=categories,
            ticktext=[str(val) for val in categories],
            showline=True,
            linewidth=1.5,
            linecolor='black',
            mirror=True,
            showgrid=False
        ),
        yaxis=dict(
            range=[0, 250],
            showline=True,
            linewidth=1.5,
            linecolor='black',
            mirror=True,
            gridcolor='lightgray',
            showgrid=True
        )
    )

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_image_path = f"{base_filename}.png"

    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")

if __name__ == '__main__':
    main()