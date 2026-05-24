import sys
import json
import plotly.graph_objects as go
import os

def create_chart(json_path):
    """
    Creates a chart from a JSON file and saves it as a PNG image.
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

    fig = go.Figure()

    if not chart_data:
        print("Warning: 'chart_data' is empty. The chart will be empty.")
    else:
        categories = [item['category'] for item in chart_data]
        # Assuming a single series bar chart based on the image
        series_values = [item['values'][0] for item in chart_data]

        fig.add_trace(go.Bar(
            x=categories,
            y=series_values,
            marker_color=colors[0] if colors else None,
            width=0.6 # Adjust bar width for visual similarity
        ))

    # Construct title
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

    # Construct source and note
    source_text = ""
    if texts.get('source'):
        source_text += f"Source: {texts.get('source')}"
    if texts.get('note'):
        if source_text:
            source_text += "<br>"
        source_text += f"Note: {texts.get('note')}"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center',
            font=dict(size=32, weight='bold')
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            showgrid=True,
            gridcolor='lightgrey',
            range=[0, 300],
            tickvals=[0, 100, 200, 300],
            tickfont=dict(size=14)
        ),
        plot_bgcolor='white',
        showlegend=False,
        font=dict(
            family="Arial",
            color="black"
        ),
        margin=dict(t=120, b=80, l=60, r=40)
    )

    if source_text:
        fig.add_annotation(
            text=source_text,
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15, 
            xanchor='left',
            yanchor='top'
        )

    # Determine output filename
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Save the figure
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    create_chart(json_file_path)