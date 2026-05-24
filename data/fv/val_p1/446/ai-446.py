import sys
import json
import pathlib
import plotly.graph_objects as go

# --- Main execution ---
if __name__ == "__main__":
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)

    # Load data from the specified JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)

    data = chart_info['chart_data']
    texts = chart_info['texts']
    colors = chart_info['colors']

    # Initialize figure
    fig = go.Figure()

    # Add trend line
    fig.add_trace(go.Scatter(
        x=data['trendline']['x'],
        y=data['trendline']['y'],
        mode='lines',
        line=dict(color=colors['plot'], width=2),
        hoverinfo='none'
    ))

    # Add slope triangle (dashed lines)
    fig.add_trace(go.Scatter(
        x=data['slope_triangle']['x'],
        y=data['slope_triangle']['y'],
        mode='lines',
        line=dict(color=colors['plot'], width=2, dash='dash'),
        hoverinfo='none'
    ))
    
    # Add planet data points
    fig.add_trace(go.Scatter(
        x=data['planets']['x'],
        y=data['planets']['y'],
        mode='markers',
        marker=dict(color=colors['plot'], size=8),
        hoverinfo='none'
    ))

    # Configure layout
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        showlegend=False,
        xaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            range=[0, 9.5]
        ),
        yaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            range=[0, 14]
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        annotations=texts.get('annotations', [])
    )

    # Generate output image
    output_path = json_path.with_suffix('.png')
    fig.write_image(output_path, scale=2)

    print(f"Chart saved to {output_path}")