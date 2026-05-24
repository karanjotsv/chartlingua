import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]
    
    # Derive the output filename base from the input JSON path
    # e.g., 'path/to/my_chart.json' -> 'my_chart'
    filename_base = json_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
    
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    data = chart_info['chart_data']
    texts = chart_info['texts']
    colors = chart_info['colors']

    fig = go.Figure()

    y_categories = [d['category'] for d in data]
    legend_labels = texts['legend_labels']

    for i, series_name in enumerate(legend_labels):
        x_values = [d['values'][i] for d in data]
        fig.add_trace(go.Bar(
            name=series_name,
            y=y_categories,
            x=x_values,
            orientation='h',
            marker_color=colors[i]
        ))

    fig.update_layout(
        title=dict(
            text=texts['title'],
            x=0.5,
            xanchor='center'
        ),
        barmode='group',
        font=dict(
            family="Arial",
            size=12
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgrey',
            gridwidth=1,
            zeroline=False,
            range=[0, 120]
        ),
        yaxis=dict(
            autorange="reversed",
            showgrid=False
        ),
        plot_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=300, r=40, t=80, b=80),
        height=600
    )

    output_filename = f"{filename_base}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")

if __name__ == '__main__':
    main()