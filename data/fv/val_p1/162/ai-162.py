import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Generates a chart from a JSON specification file provided as a command-line argument.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)

    chart_data = spec['chart_data']
    texts = spec['texts']
    colors = spec['colors']

    fig = go.Figure()

    # --- Data Traces and Annotations ---
    categories = chart_data['categories']
    for i, series in enumerate(chart_data['series']):
        fig.add_trace(go.Scatter(
            x=categories,
            y=series['values'],
            name=series['name'],
            mode='lines',
            line=dict(color=colors[i], width=4),
            showlegend=True
        ))

        # Add data labels as annotations for precise placement
        text_y_offsets = series.get('text_y_offsets', [10] * len(categories))
        for j, val in enumerate(series['values']):
            fig.add_annotation(
                x=categories[j],
                y=val,
                text=str(val),
                showarrow=False,
                font=dict(family="Arial", size=11, color="black"),
                yshift=text_y_offsets[j]
            )

    # --- Layout Configuration ---
    title_text = f"<b>{texts['title']}</b>" if texts.get('title') else ""
    if texts.get('subtitle'):
        title_text += f"<br>{texts['subtitle']}"

    fig.update_layout(
        title=dict(
            text=title_text,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        title_font=dict(
            family="Arial",
            size=20,
            color="black"
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            tickfont=dict(family="Arial", size=12, weight='bold', color="black")
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 800],
            tickvals=list(range(0, 801, 100)),
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            tickfont=dict(family="Arial", size=12, weight='bold', color="black")
        ),
        legend=dict(
            x=0.75,
            y=0.6,
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)',
            font=dict(family="Arial", size=12)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        margin=dict(l=60, r=50, t=80, b=60)
    )
    
    # --- Add Source/Note Annotation ---
    if texts.get('source'):
        fig.add_annotation(
            text=texts['source'],
            xref="paper", yref="paper",
            x=0, y=-0.15,
            showarrow=False,
            align="left",
            font=dict(family="Arial", size=10, color="grey")
        )

    # --- Output ---
    output_filename = json_path.stem + ".png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()