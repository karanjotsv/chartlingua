import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate the chart from JSON data.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = data['chart_data']
    texts = data['texts']
    colors = data['colors']

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines+markers',
            name=series.get('name', ''),
            line=dict(color=colors[i], width=2),
            marker=dict(color=colors[i], size=6)
        ))

    # Construct title and subtitle
    title_text = ""
    if texts.get("title"):
        title_text += f"<b>{texts['title']}</b>"
    if texts.get("subtitle"):
        title_text += f"<br>{texts['subtitle']}"

    fig.update_layout(
        font_family="Arial",
        plot_bgcolor='white',
        showlegend=False,
        title=dict(
            text=title_text,
            x=0.05,
            xanchor='left'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            tickvals=chart_data[0].get('x'),
            ticktext=chart_data[0].get('x_tick_labels'),
            showgrid=False,
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 15500000],
            tickvals=data.get('y_axis_tick_values'),
            ticktext=texts.get('y_axis_tick_labels'),
            showgrid=True,
            gridcolor='#E0E0E0',
            zeroline=False,
            showline=False
        ),
        margin=dict(l=80, r=40, t=50, b=80)
    )

    # Base filename from the input JSON path
    if '/' in json_path:
        filename_base = json_path.split('/')[-1].rsplit('.', 1)[0]
    elif '\\' in json_path:
        filename_base = json_path.split('\\')[-1].rsplit('.', 1)[0]
    else:
        filename_base = json_path.rsplit('.', 1)[0]

    output_filename = f"{filename_base}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()