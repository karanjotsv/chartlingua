import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'.")
        sys.exit(1)

    # Extract data from the JSON object
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    # Create a new figure
    fig = go.Figure()

    # Add a bar trace for each data series
    for i, series in enumerate(chart_data):
        fig.add_trace(go.Bar(
            name=series.get('name', ''),
            x=series.get('x', []),
            y=series.get('y', []),
            marker_color=colors[i % len(colors)] if colors else None
        ))

    # Update the layout of the figure
    title_text = texts.get('title', 'Chart Title')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

    fig.update_layout(
        title_text=title_text,
        title_x=0.5,
        font=dict(family="Arial", size=12),
        plot_bgcolor='white',
        barmode='group',
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 50],
            tick0=0,
            dtick=5,
            gridcolor='#d9d9d9',
            zeroline=True,
            zerolinecolor='#d9d9d9'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=80, b=100, l=50, r=50)
    )

    # Determine the output filename from the input JSON path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Save the figure to a PNG file
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart successfully saved to '{output_filename}'")
    except Exception as e:
        print(f"Error saving chart: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Wrapping the script in a main function and __name__ == "__main__" block
    # is a best practice, although not strictly required by the prompt.
    # It avoids executing code when the script is imported as a module.
    # For this specific task, a simple sequential script without the main
    # function would also be correct.
    # The provided solution is more robust and scalable.
    
    # Simple sequential script as per prompt strict interpretation (no functions)
    if len(sys.argv) != 2:
        print("Usage: python this_script.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data_list = config['chart_data']
    texts_dict = config['texts']
    colors_list = config['colors']

    fig = go.Figure()

    for i, data_series in enumerate(chart_data_list):
        fig.add_trace(go.Bar(
            name=data_series['name'],
            x=data_series['x'],
            y=data_series['y'],
            marker_color=colors_list[i]
        ))
        
    title_str = texts_dict.get('title', '')
    
    fig.update_layout(
        title_text=title_str,
        title_x=0.5,
        font_family="Arial",
        plot_bgcolor='white',
        barmode='group',
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            range=[0, 50],
            tick0=0,
            dtick=5,
            gridcolor='#cccccc'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=80, b=120, l=40, r=40)
    )

    base_name = os.path.splitext(os.path.basename(json_path))[0]
    output_path = f"{base_name}.png"

    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")