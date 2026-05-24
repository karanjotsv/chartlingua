import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
        textinfo='percent',
        texttemplate='%{value}%',
        textposition='auto',
        hoverinfo='label+percent',
        sort=False,
        direction='clockwise',
        rotation=75
    ))

    # Combine title and subtitle
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    # Combine source and note
    caption_text = []
    if texts.get('source'):
        caption_text.append(texts['source'])
    if texts.get('note'):
        caption_text.append(texts['note'])
    caption_full_text = "<br>".join(caption_text)

    fig.update_layout(
        title_text=title_text,
        title_x=0.5,
        title_font=dict(size=22),
        font=dict(family="Arial", size=12),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        ),
        margin=dict(l=40, r=40, t=100, b=80 if caption_full_text else 40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        annotations=[
            dict(
                text=caption_full_text,
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0,
                y=-0.15,
                xanchor='left',
                yanchor='top',
                align='left'
            )
        ] if caption_full_text else []
    )
    
    fig.update_traces(
        textfont_size=16,
        insidetextfont=dict(color='white'),
        outsidetextfont=dict(color='black')
    )

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()