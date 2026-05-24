import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'")
        sys.exit(1)

    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[item['category'] for item in chart_data],
        y=[item['value'] for item in chart_data],
        marker_color=colors[0] if colors else None,
        name=''
    ))

    title_text = texts.get('title')
    x_axis_title_text = texts.get('x_axis_title')
    y_axis_title_text = texts.get('y_axis_title')

    fig.update_layout(
        template="plotly_white",
        font_family="Arial",
        title=dict(
            text=title_text,
            font=dict(size=20),
            x=0.05,
            y=0.95,
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(
            title_text=x_axis_title_text,
            tickangle=-45,
            automargin=True
        ),
        yaxis=dict(
            title_text=y_axis_title_text,
            range=[0, 12.5],
            dtick=2,
            gridcolor='#d9d9d9'
        ),
        showlegend=False,
        margin=dict(t=100, b=150, l=50, r=50)
    )

    base_filename = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()