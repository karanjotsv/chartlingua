import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    """
    Generates a chart from a JSON data file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <json_file_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    output_path = json_path.with_suffix(".png")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing JSON file: {e}")
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    fig = go.Figure()

    for i, series in enumerate(chart_data):
        fig.add_trace(go.Bar(
            x=series.get('x'),
            y=series.get('y'),
            name=series.get('name', ''),
            marker_color=colors[i % len(colors)] if colors else None
        ))

    # Construct title and subtitle
    title_text = ""
    if texts.get("title"):
        title_text += f'<b>{texts["title"]}</b>'
    if texts.get("subtitle"):
        title_text += f'<br><sub>{texts["subtitle"]}</sub>'

    # Construct source and note annotation
    source_note_parts = []
    if texts.get('source'):
        source_note_parts.append(f"Source: {texts['source']}")
    if texts.get('note'):
        source_note_parts.append(f"Note: {texts['note']}")
    source_note_text = "<br>".join(source_note_parts)
    
    bottom_margin = 60
    if source_note_text:
        # Increase bottom margin if source/note exists
        bottom_margin += 20 * len(source_note_parts)

    fig.update_layout(
        font_family="Arial",
        plot_bgcolor='white',
        showlegend=False,
        title=dict(
            text=title_text if title_text else None,
            x=0.05,
            xanchor='left'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 250],
            tickvals=[0, 50, 100, 150, 200, 250],
            showgrid=True,
            gridcolor='#CCCCCC',
            gridwidth=1,
            griddash='dot',
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            zeroline=False
        ),
        margin=dict(l=60, r=20, t=50, b=bottom_margin)
    )

    if source_note_text:
        fig.add_annotation(
            text=source_note_text,
            align='left',
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=0,
            xanchor='left', yanchor='top',
            yshift=-bottom_margin + 10 # Position it inside the margin
        )

    try:
        fig.write_image(output_path, scale=2)
        print(f"Chart saved to {output_path}")
    except Exception as e:
        print(f"Error writing image file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()