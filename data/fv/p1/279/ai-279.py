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
            chart_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    fig = go.Figure()

    data = chart_data['chart_data']
    colors = chart_data['colors']
    texts = chart_data['texts']

    for i, series in enumerate(data):
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            name=series['name'],
            mode='lines',
            line=dict(color=colors[i % len(colors)], width=3)
        ))

    fig.update_layout(
        title=dict(
            text=texts['title'],
            x=0.5,
            font=dict(size=20)
        ),
        xaxis=dict(
            title_text=texts['x_axis_title'],
            tickangle=-90,
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks='outside'
        ),
        yaxis=dict(
            title_text=texts['y_axis_title'],
            range=[0, 290000],
            dtick=10000,
            tickformat=',',
            gridcolor='lightgrey',
            gridwidth=1,
            griddash='dash',
            showline=True,
            linewidth=1,
            linecolor='black',
            ticks='outside'
        ),
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.25,
            xanchor='center',
            x=0.5
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        plot_bgcolor='white',
        margin=dict(l=80, r=40, t=80, b=120)
    )

    base_filename = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()