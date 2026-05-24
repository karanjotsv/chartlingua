import sys
import json
import plotly.graph_objects as go
import os

def create_chart_from_json(json_path):
    """
    Reads chart data from a JSON file and generates a Plotly chart image.
    The path to the JSON file is provided as a command-line argument.
    """
    # Ensure a file path is provided
    if not json_path:
        print("Error: JSON file path must be provided as a command-line argument.")
        sys.exit(1)

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file '{json_path}'.")
        sys.exit(1)

    # Extract data and texts from the JSON structure
    chart_data = chart_config['chart_data']
    series_names = chart_config['series_names']
    texts = chart_config['texts']
    colors = chart_config['colors']

    # Prepare data for Plotly
    categories = [item['category'] for item in chart_data]
    
    # Initialize a list of lists to hold data for each series
    num_series = len(series_names)
    series_values = [[] for _ in range(num_series)]

    # Populate the series data lists
    for item in chart_data:
        for i in range(num_series):
            series_values[i].append(item['values'][i])

    # Create the figure
    fig = go.Figure()

    # Add a bar trace for each data series
    for i in range(num_series):
        fig.add_trace(go.Bar(
            x=categories,
            y=series_values[i],
            name=series_names[i],
            marker_color=colors[i]
        ))

    # Construct the title string
    title_text = texts['title']
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    # Construct the source/notes string
    source_text = texts.get('source', '')

    # Update layout for a professional appearance
    fig.update_layout(
        barmode='group',
        title=dict(
            text=title_text,
            x=0.05,
            xanchor='left',
            font=dict(
                family="Arial",
                size=18
            )
        ),
        xaxis=dict(
            title_text=texts['x_axis_title'],
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='black'
        ),
        yaxis=dict(
            title_text=texts['y_axis_title'],
            range=[0, 8],
            dtick=1,
            gridcolor='lightgray'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(
            family="Arial",
            size=12
        ),
        margin=dict(l=60, r=40, t=100, b=100),
        annotations=[
            dict(
                showarrow=False,
                text=source_text,
                x=0,
                xref="paper",
                y=-0.35,
                yref="paper",
                xanchor="left",
                yanchor="bottom",
                align="left"
            )
        ] if source_text else []
    )
    
    # Determine the output filename from the input JSON path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Save the figure as a PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    json_file_path = sys.argv[1]
    create_chart_from_json(json_file_path)