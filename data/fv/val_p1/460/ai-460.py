import sys
import json
import plotly.graph_objects as go

def main():
    """
    Generates a stacked bar chart from a JSON data file.
    Usage: python <script_name>.py <path_to_json_file>
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json>", file=sys.stderr)
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'", file=sys.stderr)
        sys.exit(1)

    chart_data = chart_info['chart_data']
    texts = chart_info['texts']
    colors = chart_info['colors']
    
    categories = chart_data['categories']
    series_list = chart_data['series']

    fig = go.Figure()

    for i, series in enumerate(series_list):
        fig.add_trace(go.Bar(
            name=series['name'],
            x=categories,
            y=series['data'],
            marker_color=colors[i]
        ))

    fig.update_layout(
        barmode='stack',
        font=dict(family="Arial"),
        title_text=texts.get('title'),
        xaxis_title=texts.get('x_axis_title'),
        yaxis_title=texts.get('y_axis_title'),
        plot_bgcolor='white',
        xaxis=dict(
            automargin=True,
            showline=True,
            linewidth=1,
            linecolor='darkgrey'
        ),
        yaxis=dict(
            range=[0, 60],
            gridcolor='lightgray',
            automargin=True,
            showline=True,
            linewidth=1,
            linecolor='darkgrey'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.45,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=60, r=40, b=180, t=50)
    )
    
    # Derive output filename from JSON path
    base_filename = json_path.rsplit('.', 1)[0]
    output_image_path = f"{base_filename}.png"

    fig.write_image(output_image_path, scale=2, width=900, height=600)
    print(f"Chart saved to {output_image_path}")

if __name__ == "__main__":
    main()