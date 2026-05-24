import sys
import json
import os
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'")
        sys.exit(1)

    # Extract data from the JSON structure
    data_series = chart_data.get('chart_data', [])
    texts = chart_data.get('texts', {})
    colors = chart_data.get('colors', [])

    # Initialize the figure
    fig = go.Figure()

    # Add traces from the chart_data
    for i, series in enumerate(data_series):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            name=series.get('name', ''),
            mode='lines',
            line=dict(color=colors[i % len(colors)] if colors else None, width=1.5),
            showlegend=False
        ))
    
    # --- Title and Annotation Handling ---
    title_text = texts.get('title')
    subtitle_text = texts.get('subtitle')
    full_title = ""
    if title_text:
        full_title += f"<b>{title_text}</b>"
    if subtitle_text:
        full_title += f"<br><sub>{subtitle_text}</sub>"

    source_text = texts.get('source')
    note_text = texts.get('note')
    caption_text = []
    if source_text:
        caption_text.append(source_text)
    if note_text:
        caption_text.append(note_text)

    # --- Layout Configuration ---
    fig.update_layout(
        title=dict(
            text=full_title,
            x=0.05,
            xanchor='left'
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(family="Arial", color='white'),
        margin=dict(l=40, r=20, t=50, b=80),
        xaxis=dict(
            showline=False,
            showgrid=True,
            gridcolor='#444444',
            gridwidth=1,
            griddash='dot',
            zeroline=False,
            tickfont=dict(color='white'),
            dtick=2,
            range=[1990, 2017]
        ),
        yaxis=dict(
            showline=False,
            showgrid=True,
            gridcolor='#AAAAAA',
            gridwidth=1,
            zeroline=False,
            tickfont=dict(color='white'),
            range=[0, 105]
        )
    )

    # Add source and note as a single annotation
    if caption_text:
        fig.add_annotation(
            text="<br>".join(caption_text),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15,
            xanchor='left',
            yanchor='top',
            font=dict(size=10)
        )

    # --- Output ---
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()