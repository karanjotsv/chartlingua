import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Generates a pie chart from a JSON data file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: File not found at '{json_path}'")
        sys.exit(1)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_path}'")
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    labels = [d['category'] for d in chart_data]
    values = [d['value'] for d in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hoverinfo='label+percent',
        textinfo='none',
        marker=dict(
            colors=colors,
            line=dict(color='black', width=1)
        ),
        sort=False,
        direction='clockwise',
        rotation=95 # Adjust start angle to match the original chart
    ))

    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            font=dict(family="Arial", size=18)
        ),
        legend=dict(
            x=0.01,
            y=0.75,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255,255,255,1)',
            bordercolor='black',
            borderwidth=1,
            font=dict(family="Arial")
        ),
        font=dict(family="Arial"),
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=50, r=50, t=100, b=50),
        showlegend=True
    )

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved to {output_filename}")
    except Exception as e:
        print(f"Error writing image file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()