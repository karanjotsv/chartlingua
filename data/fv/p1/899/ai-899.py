import sys
import json
import plotly.graph_objects as go
import os

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
    colors = chart_config.get('colors', {})

    fig = go.Figure()

    # Add traces
    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            name=series.get('name'),
            mode='lines',
            line=dict(color=colors.get('series', [])[i], width=2)
        ))

    # Update layout
    title_text = texts.get('title')
    
    fig.update_layout(
        title=dict(
            text=title_text,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        font=dict(
            family="Arial",
            size=14,
            color=colors.get('font', '#FFFFFF')
        ),
        paper_bgcolor=colors.get('background', '#000000'),
        plot_bgcolor=colors.get('background', '#000000'),
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=False,
            linecolor=colors.get('axes', '#FFFFFF'),
            linewidth=1,
            title_text=texts.get('x_axis_title'),
            zeroline=False,
            ticks=''
        ),
        yaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=False,
            linecolor=colors.get('axes', '#FFFFFF'),
            linewidth=1,
            title_text=texts.get('y_axis_title'),
            zeroline=False,
            ticks=''
        ),
        showlegend=True,
        legend=dict(
            x=0.98,
            y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)',
            bordercolor=colors.get('axes', '#FFFFFF'),
            borderwidth=0
        ),
        margin=dict(l=40, r=40, b=40, t=80)
    )

    # Output file
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