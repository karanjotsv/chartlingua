import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Main function to generate the chart from a JSON file.
    """
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>", file=sys.stderr)
        sys.exit(1)

    json_path = sys.argv[1]

    # Read data from JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_json = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}", file=sys.stderr)
        sys.exit(1)

    # Extract data, texts, and colors from the JSON object
    chart_data = chart_json.get('chart_data', [])
    texts = chart_json.get('texts', {})
    colors = chart_json.get('colors', ['#D80000'])

    # Create the figure object
    fig = go.Figure()

    # Add a trace for each data series (each shot)
    for series in chart_data:
        fig.add_trace(go.Scatter3d(
            x=series.get('x'),
            y=series.get('y'),
            z=series.get('z'),
            mode='lines',
            line=dict(color=colors[0], width=3),
            showlegend=False,
            hoverinfo='none'
        ))

    # Prepare scene annotations
    scene_annotations = []
    if texts.get('annotations'):
        for ann in texts['annotations']:
            scene_annotations.append(
                dict(
                    x=ann['x'],
                    y=ann['y'],
                    z=ann['z'],
                    text=ann['text'],
                    showarrow=False,
                    font=dict(family="Arial", size=14, color="black"),
                    xanchor="center",
                    yanchor="middle"
                )
            )

    # Update layout to style the 3D scene
    fig.update_layout(
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        scene=dict(
            xaxis=dict(
                title=texts.get('x_axis_title', ''),
                gridcolor='rgba(0,0,0,0)',
                backgroundcolor='rgba(0,0,0,0)',
                showspikes=False,
                zeroline=False,
                showline=True,
                linecolor='black',
                mirror=True,
                tickvals=[308.5, 309.0, 309.5],
                range=[308.45, 309.75]
            ),
            yaxis=dict(
                title=texts.get('y_axis_title', ''),
                tickvals=texts.get('y_axis_ticks', {}).get('vals', []),
                ticktext=texts.get('y_axis_ticks', {}).get('text', []),
                gridcolor='rgba(0,0,0,0)',
                backgroundcolor='rgba(0,0,0,0)',
                showspikes=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                range=[0, 11]
            ),
            zaxis=dict(
                title=texts.get('z_axis_title', ''),
                showticklabels=False,
                gridcolor='rgba(0,0,0,0)',
                backgroundcolor='rgba(0,0,0,0)',
                showspikes=False,
                showgrid=False,
                zeroline=False,
                showline=False,
                range=[0, 2.5]
            ),
            camera=dict(
                eye=dict(x=-1.6, y=-1.8, z=1.0)
            ),
            annotations=scene_annotations,
            aspectmode='manual',
            aspectratio=dict(x=1, y=1.2, z=0.6)
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    # Determine output filename and save the image
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_image_path = f"{base_filename}.png"
    
    try:
        fig.write_image(output_image_path, scale=2)
        print(f"Chart saved to {output_image_path}")
    except Exception as e:
        print(f"Error writing image file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()