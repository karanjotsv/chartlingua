import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_details = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing JSON file: {e}")
        sys.exit(1)

    fig = go.Figure()

    for i, series in enumerate(chart_details['chart_data']):
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            name=series.get('name', ''),
            line=dict(color=chart_details['colors'][i])
        ))

    title_text = chart_details['texts']['title']
    if chart_details['texts']['subtitle']:
        title_text += f"<br><sub>{chart_details['texts']['subtitle']}</sub>"

    fig.update_layout(
        title_text=title_text,
        title_x=0.5,
        font=dict(
            family="Arial",
            size=12
        ),
        xaxis=dict(
            title_text=chart_details['texts']['x_axis_title'],
            range=[-4, 4],
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='outside',
            showgrid=False
        ),
        yaxis=dict(
            title_text=chart_details['texts']['y_axis_title'],
            range=[0, 8],
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            ticks='outside',
            showgrid=False
        ),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=40, r=20, t=60, b=40)
    )

    output_filename_base = Path(json_path).stem
    fig.write_image(f"{output_filename_base}.png", scale=2)

if __name__ == "__main__":
    main()