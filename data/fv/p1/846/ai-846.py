import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>")
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

    fig = go.Figure()

    is_first_area = True
    for i, series in enumerate(chart_data):
        series_color = colors[i % len(colors)]
        if series.get('type') == 'area':
            fill_mode = 'tozeroy' if is_first_area else 'tonexty'
            is_first_area = False
            fig.add_trace(go.Scatter(
                x=series['x'],
                y=series['y'],
                name=series['name'],
                mode='lines',
                line=dict(width=0),
                fill=fill_mode,
                stackgroup='one',
                fillcolor=series_color,
                connectgaps=False,
                hoverinfo='x+y+name'
            ))
        elif series.get('type') == 'line':
            fig.add_trace(go.Scatter(
                x=series['x'],
                y=series['y'],
                name=series['name'],
                mode='lines',
                line=dict(color=series_color, width=3),
                connectgaps=False,
                hoverinfo='x+y+name'
            ))

    # Reverse trace order to match original legend (Napster, Kazaa, Morpheus)
    fig.data = fig.data[::-1]

    title_text = texts.get('title')
    source_text = texts.get('source')
    
    fig.update_layout(
        title=dict(
            text=title_text if title_text else '',
            x=0.04,
            y=0.95,
            xanchor='left',
            yanchor='top',
            font=dict(size=18)
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(family="Arial", color='white'),
        xaxis=dict(
            tickvals=[
                'Jan 00', 'May 00', 'Jul 00', 'Sep 00', 'Nov 00', 
                'Jan 01', 'Mar 01', 'May 01', 'Jul 01', 'Sep 01', 'Nov 01', 
                'Jan 02'
            ],
            ticktext=[
                '\'00', 'May', 'Jul', 'Sep', 'Nov', 
                '\'01', 'Mar', 'May', 'Jul', 'Sep', 'Nov', 
                '\'02'
            ],
            showgrid=True,
            gridcolor='#555555',
            zeroline=False
        ),
        yaxis=dict(
            range=[0, 20],
            dtick=5,
            showgrid=True,
            gridcolor='#555555',
            zeroline=False
        ),
        legend=dict(
            x=0.98,
            y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        ),
        margin=dict(t=80, b=100, l=60, r=40),
        annotations=[
            dict(
                text=source_text if source_text else '',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0,
                y=-0.22,
                xanchor='left',
                yanchor='bottom',
                align='left',
                font=dict(size=10)
            )
        ]
    )

    output_basename = pathlib.Path(json_path).stem
    output_filename = f"{output_basename}.png"
    
    fig.write_image(output_filename, scale=2, width=600, height=480)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()