import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)

    chart_data = chart_data_json['chart_data']
    texts = chart_data_json['texts']
    colors = chart_data_json['colors']

    # Reverse data for horizontal bar chart (Plotly plots from bottom up)
    categories = [item['category'] for item in chart_data][::-1]
    values = [item['value'] for item in chart_data][::-1]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker=dict(color=colors[0]),
        text=[f'{v:,}' for v in values],
        textposition='outside',
        textfont=dict(family='Arial', size=10, color='#333333'),
        cliponaxis=False
    ))

    fig.update_layout(
        title=dict(
            text=texts['title'],
            x=0.5,
            font=dict(family='Arial', size=20)
        ),
        xaxis=dict(
            title=texts['x_axis_title'],
            tickvals=[0, 500000000, 1000000000, 1500000000, 2000000000, 2500000000],
            ticktext=['0', '500 M', '1 G', '1.5 G', '2 G', '2.5 G'],
            range=[0, 3000000000],
            showgrid=True,
            gridcolor='white',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=True
        ),
        font=dict(family="Arial", size=12),
        plot_bgcolor='#E6E6E6',
        paper_bgcolor='#E6E6E6',
        height=1400,
        margin=dict(l=350, r=120, t=100, b=80),
        showlegend=False
    )

    output_path = json_path.with_suffix('.png')
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()