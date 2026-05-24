import sys
import json
import os
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Ensure the JSON file exists
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    # Read data from the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    # Extract data and texts
    data_series = chart_data.get('chart_data', [])
    texts = chart_data.get('texts', {})
    colors = chart_data.get('colors', [])
    shapes = chart_data.get('shapes', [])
    annotations_data = texts.get('annotations', [])

    # Create figure
    fig = go.Figure()

    # Add traces from JSON data
    for i, series in enumerate(data_series):
        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            name=series['name'],
            mode='lines',
            line=dict(color=colors[i % len(colors)], width=2.5)
        ))

    # Prepare annotations
    annotations = []
    for ann in annotations_data:
        annotations.append(
            go.layout.Annotation(
                text=ann['text'],
                x=ann['x'],
                y=ann['y'],
                showarrow=True,
                arrowhead=0,
                arrowwidth=1,
                arrowcolor='black',
                ax=ann.get('ax', 0),
                ay=ann.get('ay', -40),
                xanchor=ann.get('xanchor', 'auto'),
                yanchor=ann.get('yanchor', 'auto')
            )
        )

    # Update layout
    fig.update_layout(
        font=dict(family="Arial", size=12, color="black"),
        plot_bgcolor='white',
        xaxis=dict(
            title=texts.get('x_axis_title'),
            showticklabels=False,
            showgrid=False,
            linecolor='darkgrey',
            linewidth=1,
            zeroline=False,
            ticks=""
        ),
        yaxis=dict(
            title=texts.get('y_axis_title'),
            range=[0, 1],
            dtick=0.1,
            showgrid=True,
            gridcolor='lightgrey',
            linecolor='darkgrey',
            linewidth=1,
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=80, r=40, t=40, b=120),
        shapes=shapes,
        annotations=annotations
    )

    # Generate output filename
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Write image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()