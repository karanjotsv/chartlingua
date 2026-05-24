import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    # --- 1. Argument and File Handling ---
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>", file=sys.stderr)
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
        sys.exit(1)

    output_filename = json_path.with_suffix(".png")

    # --- 2. Data Loading ---
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing JSON file: {e}", file=sys.stderr)
        sys.exit(1)

    chart_data = data.get('chart_data', {})
    texts = data.get('texts', {})
    colors = data.get('colors', [])
    categories = chart_data.get('categories', [])
    series_list = chart_data.get('series', [])

    # --- 3. Chart Creation ---
    fig = go.Figure()

    # Iterate through series in reverse for correct z-order drawing (bottom layers first).
    # The JSON is ordered by desired legend appearance (top to bottom).
    for i in range(len(series_list) - 1, -1, -1):
        series = series_list[i]
        color = colors[i]
        
        # legendrank controls the order in the legend; smaller numbers are higher up.
        # We want to preserve the original JSON order in the legend.
        legend_rank = i + 1

        if series.get('type') == 'area':
            fig.add_trace(go.Scatter(
                x=categories,
                y=series.get('data'),
                name=series.get('name'),
                mode='lines',
                line=dict(width=0),
                fill='tozeroy',
                fillcolor=color,
                hoverinfo='skip',
                legendrank=legend_rank
            ))
        elif series.get('type') == 'line':
            fig.add_trace(go.Scatter(
                x=categories,
                y=series.get('data'),
                name=series.get('name'),
                mode='lines',
                line=dict(color=color, width=2.5),
                hoverinfo='skip',
                legendrank=legend_rank
            ))

    # --- 4. Layout and Styling ---
    # Combine source and note for the annotation
    source_text = texts.get('source')
    note_text = texts.get('note')
    annotation_parts = [text for text in [note_text, source_text] if text]
    annotation_text = "<br>".join(annotation_parts)

    # Determine X-axis ticks to match the yearly labels from the original chart
    tickvals = [i for i, cat in enumerate(categories) if cat.startswith('Q1')]
    ticktext = [f"'{cat.split(' ')[1]}" for cat in categories if cat.startswith('Q1')]

    fig.update_layout(
        font=dict(family="Arial", size=12, color="white"),
        plot_bgcolor='black',
        paper_bgcolor='black',
        title=texts.get('title'),
        margin=dict(l=50, r=40, t=50, b=100),
        xaxis=dict(
            title=texts.get('x_axis_title'),
            tickmode='array',
            tickvals=tickvals,
            ticktext=ticktext,
            showgrid=False,
            zeroline=False,
            linecolor='white',
            linewidth=1,
            ticks='outside',
            tickcolor='white'
        ),
        yaxis=dict(
            title=texts.get('y_axis_title'),
            range=[0, 30],
            dtick=5,
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.2)',
            zeroline=False,
            linecolor='white',
            linewidth=1,
            ticks='outside',
            tickcolor='white'
        ),
        legend=dict(
            x=0.98,
            y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='black',
            borderwidth=0
        ),
        showlegend=True if any(s.get('name') for s in series_list) else False
    )

    if annotation_text:
        fig.add_annotation(
            text=annotation_text,
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.0,
            y=-0.25,
            xanchor='left',
            yanchor='top',
            font=dict(size=10)
        )

    # --- 5. Output ---
    try:
        fig.write_image(output_filename, scale=2, width=600, height=480)
        print(f"Chart saved to {output_filename}")
    except Exception as e:
        print(f"Error writing image file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()