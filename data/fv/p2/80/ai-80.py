import sys
import json
import os
import plotly.graph_objects as go

def create_chart(json_path):
    """
    Generates a chart from a JSON file and saves it as a PNG image.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='black', width=1.5)
        ),
        sort=False,
        direction='clockwise',
        textinfo='none',
        hoverinfo='label+percent',
        showlegend=True
    ))

    annotations = []
    if texts.get('bottom_left_text'):
        annotations.append(go.layout.Annotation(
            text=texts['bottom_left_text'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=0.01,
            xanchor='left',
            yanchor='top',
            font=dict(size=10)
        ))
    if texts.get('bottom_right_text'):
        annotations.append(go.layout.Annotation(
            text=texts['bottom_right_text'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.7,
            y=0.01,
            xanchor='left',
            yanchor='top',
            font=dict(size=10)
        ))

    fig.update_layout(
        width=800,
        height=700,
        plot_bgcolor='#D3D3D3',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        showlegend=True,
        legend=dict(
            x=0.7,
            y=0.95,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.5)'
        ),
        margin=dict(l=40, r=40, t=40, b=200),
        annotations=annotations
    )
    
    # Use the JSON filename to create the output PNG filename
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    create_chart(json_file_path)