import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file '{json_path}'.")
        sys.exit(1)

    fig = go.Figure()

    chart_data = config.get('chart_data', [])
    colors = config.get('colors', [])

    for i, trace_data in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=trace_data.get('x'),
            y=trace_data.get('y'),
            mode=trace_data.get('mode', 'lines'),
            line=dict(
                color=colors[i % len(colors)],
                dash=trace_data.get('line', {}).get('dash', 'solid'),
                width=3
            ),
            showlegend=False
        ))

    texts = config.get('texts', {})

    fig.update_layout(
        xaxis_title=texts.get('x_axis_title'),
        yaxis_title=texts.get('y_axis_title'),
        font=dict(family="Arial", size=14),
        plot_bgcolor='white',
        showlegend=False,
        xaxis=dict(
            showline=True,
            linewidth=1.5,
            linecolor='black',
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            ticks=""
        ),
        yaxis=dict(
            showline=True,
            linewidth=1.5,
            linecolor='black',
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            ticks=""
        ),
        margin=dict(l=90, r=30, t=30, b=70)
    )

    # Derive the base filename from the JSON path to create the output PNG filename
    if '/' in json_path:
        base_name = json_path.split('/')[-1]
    elif '\\' in json_path:
        base_name = json_path.split('\\')[-1]
    else:
        base_name = json_path
    
    if '.' in base_name:
        base_name = base_name.rsplit('.', 1)[0]

    output_filename = f"{base_name}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()