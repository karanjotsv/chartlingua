import sys
import json
import plotly.graph_objects as go

def create_chart(json_path):
    """
    Reads chart data from a JSON file and generates a Plotly chart image.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_path}'", file=sys.stderr)
        sys.exit(1)

    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    if not chart_data:
        print("Error: 'chart_data' is missing or empty in the JSON file.", file=sys.stderr)
        sys.exit(1)

    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#000000', width=1)),
        texttemplate='%{value:.2f}%',
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        hoverinfo='label+percent',
        sort=False,
        direction='counterclockwise',
        rotation=75 
    ))

    title_text = texts.get('title')
    
    fig.update_layout(
        title=dict(
            text=f"<b>{title_text}</b>" if title_text else None,
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top',
            font=dict(family="Arial", size=18, color='black')
        ),
        font=dict(family="Arial", size=12, color='black'),
        legend=dict(
            x=0.85,
            y=0.6,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='black',
            borderwidth=1
        ),
        margin=dict(l=40, r=40, t=80, b=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        # Recreate the outer border
        shapes=[
            dict(
                type='rect',
                xref='paper',
                yref='paper',
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color='black',
                    width=2
                )
            )
        ],
        showlegend=True
    )

    # Determine output filename from input JSON path
    if '/' in json_path:
        base_name = json_path.split('/')[-1].rsplit('.', 1)[0]
    else:
        base_name = json_path.rsplit('.', 1)[0]
    
    output_filename = f"{base_name}.png"

    fig.write_image(output_filename, scale=2, width=600, height=450)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>", file=sys.stderr)
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    # Wrap main logic in a function for clarity and potential reusability
    create_chart(json_file_path)