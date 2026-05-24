import sys
import json
import plotly.graph_objects as go

def main():
    """
    Main function to generate the chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{json_path}' is not a valid JSON file.")
        sys.exit(1)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']
    
    labels = [d['label'] for d in chart_data]
    values = [d['value'] for d in chart_data]

    # Manually create the text for each slice to include label and value
    slice_texts = [f"{d['label']}<br>{d['value']}%" for d in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
        hoverinfo='label+percent',
        text=slice_texts,
        textinfo='text',
        textposition='auto',
        sort=False,
        rotation=150
    ))

    # Combine title and subtitle
    title_text = f"<b>{texts['title']}</b>"
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"
        
    # Combine note and source
    source_note_text = []
    if texts.get('note'):
        source_note_text.append(texts['note'])
    if texts.get('source'):
        source_note_text.append(texts['source'])
    source_note_text = "<br>".join(source_note_text)
    
    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.01,
            y=0.95,
            xanchor='left',
            yanchor='top'
        ),
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        showlegend=False,
        margin=dict(l=40, r=40, t=100, b=100),
        paper_bgcolor='white',
        plot_bgcolor='white',
        annotations=[
            dict(
                text=source_note_text,
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=0,
                xanchor='left',
                yanchor='top',
                align='left'
            )
        ]
    )
    
    # Customize text properties for inside/outside labels
    fig.update_traces(
        textfont=dict(family="Arial", size=12),
        insidetextfont=dict(color='black'),
        outsidetextfont=dict(color='black')
    )

    # Determine output filename from JSON path
    base_filename = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()