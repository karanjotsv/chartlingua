import sys
import json
import plotly.graph_objects as go
from pathlib import Path

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(__file__).name} <json_file_path>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config.get('chart_data', [])
    colors = config.get('colors', [])
    
    labels = [d['category'] for d in chart_data]
    values = [d['value'] for d in chart_data]
    
    # Format the text to be displayed inside the pie slices
    pie_texts = [f"{d['category']}<br>{d['value']}%" for d in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        text=pie_texts,
        textinfo='text',
        textposition='inside',
        marker=dict(
            colors=colors,
            line=dict(color='#000000', width=1)
        ),
        textfont=dict(
            family="Arial",
            size=12,
            color='white'
        ),
        hoverinfo='skip',
        sort=False,
        direction='clockwise'
    ))

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        font=dict(
            family="Arial",
            color="white"
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=True,
    )

    filename_base = json_path.stem
    output_filename = f"{filename_base}.png"
    fig.write_image(output_filename, scale=2)
    # Minimal print to indicate completion
    # print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()