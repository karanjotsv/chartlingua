import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_data_dict = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    fig = go.Figure()

    data_series = chart_data_dict.get('chart_data', [])
    colors = chart_data_dict.get('colors', [])
    texts = chart_data_dict.get('texts', {})

    for i, series in enumerate(data_series):
        color = colors[i % len(colors)] if colors else '#000000'
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            mode='lines+markers',
            name=series.get('name', ''),
            line=dict(color=color, width=2),
            marker=dict(symbol='diamond', color=color, size=8)
        ))

    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            tickmode='linear',
            tick0=1,
            dtick=1,
            side='top'
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            showgrid=True,
            gridcolor='lightgrey',
            autorange='reversed',
            range=[21, 4],
            tickvals=[5, 10, 15, 20]
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=80, b=50)
    )

    filename_base = json_path.split('/')[-1].split('.')[0]
    output_filename = f"{filename_base}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")

if __name__ == "__main__":
    main()