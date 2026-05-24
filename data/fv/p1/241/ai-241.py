import sys
import json
import plotly.graph_objects as go
import os

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{json_file_path}' is not a valid JSON file.")
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    if not chart_data:
        print("Error: 'chart_data' is missing or empty in the JSON file.")
        sys.exit(1)

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        marker_line_color='black',
        marker_line_width=1,
        showlegend=False
    ))

    title_text = texts.get('title', '') or ''
    subtitle_text = texts.get('subtitle', '') or ''
    if subtitle_text:
        title_text += f"<br><sub>{subtitle_text}</sub>"

    source_text = texts.get('source', '') or ''

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5
        ),
        font=dict(family="Arial"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=60, r=40, t=50, b=80),
        xaxis=dict(
            title_text=texts.get('xaxis_title'),
            showline=False,
            showgrid=False,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_text=texts.get('yaxis_title'),
            range=[0.105, 0.145],
            tickvals=[0.105, 0.115, 0.125, 0.135, 0.145],
            ticktext=['0,105', '0,115', '0,125', '0,135', '0,145'],
            showgrid=True,
            gridcolor='#d3d3d3',
            showline=False,
            zeroline=False
        ),
        annotations=[
            dict(
                text=source_text,
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=-0.2, # Adjust this value to position the source text
                xanchor='left',
                yanchor='top',
                align='left'
            )
        ] if source_text else []
    )

    base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
    output_image_path = f"{base_filename}.png"

    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")

if __name__ == "__main__":
    main()