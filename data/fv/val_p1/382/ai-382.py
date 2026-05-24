import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]
    
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
    
    fig = go.Figure()

    if not chart_data:
        print("Warning: No data found in JSON file.")
    else:
        x_values = [d['x'] for d in chart_data]
        y_values = [d['y'] for d in chart_data]
        
        fig.add_trace(go.Bar(
            x=x_values,
            y=y_values,
            marker_color=colors[0] if colors else '#0000FF',
            showlegend=False
        ))

    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

    fig.update_layout(
        title={
            'text': title_text,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title_text=texts.get('x_axis_title'),
        yaxis_title_text=texts.get('y_axis_title'),
        font_family="Arial",
        font_color="black",
        plot_bgcolor='white',
        xaxis={
            'type': 'category',
            'showline': True,
            'linewidth': 1,
            'linecolor': 'black',
            'showgrid': False,
            'mirror': True
        },
        yaxis={
            'range': [0, 1.5],
            'tickvals': [0, 0.5, 1.0, 1.5],
            'showline': True,
            'linewidth': 1,
            'linecolor': 'black',
            'gridcolor': 'gray',
            'mirror': True,
            'zeroline': False
        },
        showlegend=False,
        margin=dict(l=60, r=30, t=80, b=60),
        bargap=0.15
    )
    
    # Add source/note at the bottom
    source_text = texts.get('source')
    if source_text:
        fig.add_annotation(
            text=source_text,
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.15, 
            xanchor='left',
            yanchor='top'
        )

    base_filename = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()