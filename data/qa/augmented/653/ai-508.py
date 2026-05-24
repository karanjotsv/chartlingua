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
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    # Format text labels for bars to match original (e.g., "5%" instead of "5.00%")
    text_labels = [f"{v}%" if v == int(v) else f"{v:.2f}%" for v in values]

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        text=text_labels,
        textposition='outside',
        marker_color=colors[0] if colors else None,
        hoverinfo='none',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False
    ))

    fig.update_layout(
        font=dict(family="Arial", size=12, color="black"),
        title=dict(
            text=texts.get('title'),
            x=0.05,
            xanchor='left'
        ),
        plot_bgcolor='white',
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            title_font=dict(size=12),
            showgrid=True,
            gridcolor='#e9e9e9',
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=1,
            ticksuffix='%',
            range=[-7.5, 10.5],
            tickfont=dict(size=12)
        ),
        margin=dict(l=80, r=40, t=40, b=120),
        bargap=0.25,
        annotations=[
            dict(
                text=texts.get('note'),
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=-0.2,
                xanchor='left',
                yanchor='bottom',
                font=dict(color="#3572c6") # color to mimic hyperlink
            ),
            dict(
                text=texts.get('source'),
                showarrow=False,
                xref="paper",
                yref="paper",
                x=1,
                y=-0.2,
                xanchor='right',
                yanchor='bottom'
            )
        ]
    )
    
    # Adjust position of bar text for negative values
    fig.update_traces(textfont_size=12)

    output_path = json_path.with_suffix('.png')
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()