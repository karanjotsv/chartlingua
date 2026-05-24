import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]
    bar_labels = [item.get('label') for item in chart_data]

    fig = go.Figure()

    # Main bar trace
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=bar_labels,
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        showlegend=False,
        cliponaxis=False 
    ))

    # Dummy trace for the custom legend
    fig.add_trace(go.Bar(
        x=[None],
        y=[None],
        name=texts['legend_label'],
        marker_color='#cccccc'
    ))

    # Combine title and subtitle
    title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title_text=texts['x_axis_title'],
            showline=True,
            linewidth=2,
            linecolor='#0B5394',
            mirror=True,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_text=texts['y_axis_title'],
            range=[0, 1600],
            dtick=250,
            ticksuffix=texts['y_axis_suffix'],
            showline=True,
            linewidth=2,
            linecolor='#0B5394',
            mirror=True,
            gridcolor='#d9d9d9',
            tickfont=dict(size=12)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        font=dict(family="Arial", size=14, color="black"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=80, r=40, t=100, b=120)
    )

    # Add source annotation
    if texts.get('source'):
        fig.add_annotation(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
        
    output_path = json_path.with_suffix('.png')
    fig.write_image(str(output_path), scale=2, width=800, height=600)
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()