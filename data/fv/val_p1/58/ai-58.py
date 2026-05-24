import sys
import json
import plotly.graph_objects as go
import os

def main():
    """
    Generates a pie chart from a JSON data file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{json_path}' contains invalid JSON.")
        sys.exit(1)

    # Extract data from the JSON structure
    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the pie chart trace
    pie_trace = go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=1)
        ),
        textinfo='percent',
        texttemplate='%{value:.1f}%',
        hoverinfo='label+percent',
        sort=False,  # Preserve the order from the JSON file
        direction='clockwise'
    )

    fig = go.Figure(data=[pie_trace])

    # Construct title string
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    # Update layout
    fig.update_layout(
        title_text=title_text,
        title_x=0.5,
        font=dict(
            family="Arial",
            size=12
        ),
        legend_title_text=texts.get('legend_title'),
        showlegend=True,
        margin=dict(l=40, r=40, t=80, b=80)
    )

    # Add note as an annotation
    note_text = texts.get('note')
    if note_text:
        fig.add_annotation(
            text=f"<i>{note_text}</i>",
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=0,
            xanchor='right',
            yanchor='top'
        )

    # Determine output filename and save the image
    base_filename = os.path.splitext(json_path)[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")

if __name__ == '__main__':
    main()