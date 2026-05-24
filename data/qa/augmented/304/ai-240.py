import sys
import json
import plotly.graph_objects as go

def create_chart(json_path):
    """
    Reads chart data from a JSON file and generates a Plotly chart.

    Args:
        json_path (str): The path to the input JSON file.
    """
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

    if not chart_data:
        print("Error: 'chart_data' is missing or empty in the JSON file.")
        sys.exit(1)

    x_values = [d['x'] for d in chart_data]
    y_values = [d['y'] for d in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values,
        marker_color=colors[0] if colors else None,
        name=''
    ))

    # Combine title and subtitle
    title_text = texts.get('title') or ''
    subtitle_text = texts.get('subtitle') or ''
    if title_text and subtitle_text:
        full_title = f"{title_text}<br><sub>{subtitle_text}</sub>"
    else:
        full_title = title_text or subtitle_text

    # Combine source and note for annotation
    source_text = texts.get('source', '')
    note_text = texts.get('note', '')
    if source_text and note_text:
        source_note_text = f"{source_text}<br>{note_text}"
    else:
        source_note_text = source_text or note_text
    
    annotations = []
    if source_note_text:
        annotations.append(
            dict(
                xref='paper', yref='paper',
                x=1.0, y=-0.22,
                xanchor='right', yanchor='top',
                text=source_note_text,
                showarrow=False,
                align='right',
                font=dict(size=12)
            )
        )

    fig.update_layout(
        title_text=full_title,
        title_x=0.5,
        yaxis_title_text=texts.get('y_axis_title'),
        xaxis_title_text=texts.get('x_axis_title'),
        font=dict(family="Arial"),
        showlegend=False,
        plot_bgcolor='white',
        xaxis=dict(
            type='category',
            showgrid=False,
            showline=True,
            linecolor='lightgray',
            tickangle=0
        ),
        yaxis=dict(
            range=[0, 1000],
            tickvals=[0, 200, 400, 600, 800, 1000],
            ticktext=['0', '200', '400', '600', '800', '1 000'],
            gridcolor='#E5E5E5',
            gridwidth=1,
            zeroline=False,
            showline=False
        ),
        margin=dict(l=80, r=40, t=50, b=120),
        annotations=annotations
    )

    # Determine output filename from input JSON path
    if json_path.endswith('.json'):
        output_filename = json_path[:-5] + '.png'
    else:
        output_filename = json_path + '.png'
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    create_chart(json_file_path)