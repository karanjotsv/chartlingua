import sys
import json
import plotly.graph_objects as go
import os

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    # Read data from the specified JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}")
        sys.exit(1)

    # Extract data, texts, and colors from the JSON object
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', {})

    # Initialize the figure
    fig = go.Figure()

    # Add traces from chart_data
    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            line=dict(
                color=colors.get('curve', ['#000000'])[i],
                width=3,
                shape='spline',
                smoothing=1.3
            ),
            showlegend=False
        ))

    # Update layout
    fig.update_layout(
        font=dict(
            family="Arial",
            color=colors.get('axis_and_text', '#000000')
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=90, r=40, t=100, b=80),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            title_font=dict(size=18),
            title_standoff=15,
            showgrid=False,
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor=colors.get('axis_and_text', '#000000'),
            showticklabels=False,
            ticks='',
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=1.5
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            title_font=dict(size=18),
            title_standoff=20,
            showgrid=False,
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor=colors.get('axis_and_text', '#000000'),
            showticklabels=False,
            ticks='',
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=1.5
        )
    )

    # Add annotations
    for ann in texts.get('annotations', []):
        fig.add_annotation(
            x=ann.get('x'),
            y=ann.get('y'),
            text=ann.get('text'),
            showarrow=True,
            arrowhead=ann.get('arrowhead', 1),
            ax=ann.get('ax', 0),
            ay=ann.get('ay', -40),
            font=dict(
                size=ann.get('font_size', 12),
                color=colors.get('axis_and_text', '#000000')
            ),
            align=ann.get('align', 'center'),
            arrowsize=ann.get('arrowsize', 1),
            arrowwidth=ann.get('arrowwidth', 1),
            arrowcolor=colors.get('axis_and_text', '#000000')
        )

    # Determine output filename and save the image
    base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
    output_image_path = f"{base_filename}.png"
    
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")

if __name__ == "__main__":
    main()