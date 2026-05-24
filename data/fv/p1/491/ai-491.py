import sys
import json
import os
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Check if the JSON file exists
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    # Extract data from the JSON structure
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    # Prepare data for Plotly
    labels = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the figure
    fig = go.Figure()

    # Add the pie chart trace
    # The first slice in the original chart is slightly pulled out
    pull_values = [0.05] + [0] * (len(values) - 1) if values else []

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
        pull=pull_values,
        sort=False,  # Preserve the order from the JSON data
        hoverinfo='label+percent+value',
        textinfo='none'
    ))

    # Construct the title block
    title_text = f"<b>{texts.get('title', '')}</b>"
    if texts.get('subtitle'):
        title_text += f"<br>{texts.get('subtitle')}"

    # Update layout
    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        font=dict(
            family="Arial",
            size=14
        ),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02
        ),
        margin=dict(t=120, b=80, l=80, r=150),
        showlegend=True
    )
    
    # Although the original is a 3D pie chart, standard Plotly does not support this type.
    # We are creating a 2D pie chart as the modern and standard representation.

    # Add source and note as an annotation if they exist
    source_note_parts = []
    if texts.get('source'):
        source_note_parts.append(f"Source: {texts['source']}")
    if texts.get('note'):
        source_note_parts.append(texts['note'])
    
    if source_note_parts:
        source_note_text = "<br>".join(source_note_parts)
        fig.add_annotation(
            showarrow=False,
            text=source_note_text,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,  # Position below the chart
            xanchor="left",
            yanchor="top",
            align="left"
        )

    # Determine output filename from the input JSON path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Save the chart as a PNG image
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved as '{output_filename}'")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()