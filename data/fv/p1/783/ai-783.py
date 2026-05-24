import sys
import json
import plotly.graph_objects as go
import pathlib

# --- Main execution ---
if __name__ == "__main__":
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    # Get paths from command-line argument
    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: File not found at {json_path}")
        sys.exit(1)
        
    output_path = json_path.with_suffix('.png')

    # Load data from JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)

    # Extract data from the loaded JSON
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', {})

    # Create the figure object
    fig = go.Figure()

    # Add traces from chart_data
    for i, series in enumerate(chart_data):
        fig.add_trace(go.Scatter(
            x=series.get('x'),
            y=series.get('y'),
            name=series.get('name'),
            mode='lines',
            line=dict(color=colors.get('series_colors', [])[i])
        ))

    # Build title string
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text = f"{title_text}<br><sub>{texts.get('subtitle')}</sub>" if title_text else texts.get('subtitle')

    # Update layout
    fig.update_layout(
        title_text=title_text,
        title_x=0.5,
        paper_bgcolor=colors.get('background_color', '#FFFFFF'),
        plot_bgcolor=colors.get('background_color', '#FFFFFF'),
        font=dict(
            family="Arial",
            color=colors.get('text_color', '#000000')
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            linecolor=colors.get('grid_color'),
            mirror=True
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            linecolor=colors.get('grid_color'),
            mirror=True
        ),
        showlegend=True,
        legend=dict(
            x=0.98,
            y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        ),
        margin=dict(t=40, r=40, b=40, l=40)
    )

    # Write image to file
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")