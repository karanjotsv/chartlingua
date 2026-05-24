import sys
import json
import plotly.graph_objects as go
import os

def create_chart(json_path):
    """
    Reads chart data from a JSON file and generates a Plotly chart image.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        return

    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker_color=colors[0] if colors else '#1f497d'
    ))

    # Construct title and subtitle
    title_text = f"<b>{texts.get('title', '')}</b>"
    if texts.get('subtitle'):
        title_text += f"<br>{texts.get('subtitle')}"

    # Proactively calculate height to avoid label overlap
    num_categories = len(categories)
    # Base height + pixels per category, with a minimum
    chart_height = max(400, 150 + num_categories * 25)

    fig.update_layout(
        title={
            'text': title_text,
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis={
            'title_text': texts.get('x_axis_title'),
            'side': 'top',
            'gridcolor': '#e0e0e0',
            'zeroline': False
        },
        yaxis={
            'title_text': texts.get('y_axis_title'),
            'autorange': 'reversed',
            'gridcolor': '#e0e0e0',
            'zeroline': False
        },
        font_family="Arial",
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        height=chart_height,
        margin=dict(l=160, r=40, t=120, b=40)
    )
    
    # Set x-axis range and ticks based on original chart
    fig.update_xaxes(range=[0, 500], tickmode='linear', tick0=0, dtick=50)

    # Derive output filename from JSON path
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_name}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
    else:
        create_chart(sys.argv[1])