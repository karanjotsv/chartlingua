import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json_file>")
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

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='black', width=1)),
        textinfo='percent',
        texttemplate='%{value:.2f}%',
        insidetextfont=dict(color='white', size=12, family="Arial"),
        hoverinfo='label+percent',
        sort=False,
        direction='clockwise',
        rotation=-80
    ))

    fig.update_layout(
        showlegend=True,
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(family="Arial", color='white'),
        legend=dict(
            font=dict(family="Arial", color='white')
        ),
        margin=dict(l=50, r=50, t=50, b=80),
        annotations=[
            dict(
                text=texts.get('note', ''),
                align='left',
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.01,
                y=0.01,
                font=dict(color='red', size=14, family="Arial"),
                xanchor='left',
                yanchor='bottom'
            )
        ]
    )

    filename_base = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{filename_base}.png"

    fig.write_image(output_filename, scale=2, width=800, height=600)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()