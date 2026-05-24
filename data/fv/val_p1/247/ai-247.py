import sys
import json
import plotly.graph_objects as go
import pathlib

def main():
    """
    Main function to generate the chart from a JSON file.
    """
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    # Get the JSON file path from the command-line argument
    json_file_path = pathlib.Path(sys.argv[1])

    # Check if the file exists
    if not json_file_path.is_file():
        print(f"Error: File not found at {json_file_path}")
        sys.exit(1)

    # Read the JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing JSON file: {e}")
        sys.exit(1)

    # Extract data from the config
    chart_data = config.get('chart_data', {})
    texts = config.get('texts', {})
    colors = config.get('colors', [])
    
    # Create the figure object
    fig = go.Figure()

    # Add traces from the JSON data
    x_values = chart_data.get('x_values', [])
    for i, series in enumerate(chart_data.get('series', [])):
        fig.add_trace(go.Scatter(
            x=x_values,
            y=series.get('y_values', []),
            name=series.get('name', ''),
            mode='lines',
            line=dict(color=colors[i] if i < len(colors) else None, width=3)
        ))

    # Update layout
    fig.update_layout(
        title=dict(
            text=texts.get('title'),
            x=0.5,
            font=dict(size=24)
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=True,
            gridcolor='#D3D3D3',
            zeroline=False,
            tickvals=[250, 300, 350, 400],
            range=[240, 410]
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            showgrid=True,
            gridcolor='#D3D3D3',
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=1,
            showline=True,
            linecolor='black',
            linewidth=1,
            range=[0, 450],
            dtick=50
        ),
        font=dict(
            family="Arial",
            size=14
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation='v',
            yanchor="top",
            y=0.7,
            xanchor="right",
            x=0.98,
            bordercolor='white'
        ),
        margin=dict(l=60, r=50, t=80, b=50)
    )

    # Generate output image path
    output_filename = json_file_path.with_suffix('.png')

    # Write the image file
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved to {output_filename}")
    except Exception as e:
        print(f"Error writing image file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()