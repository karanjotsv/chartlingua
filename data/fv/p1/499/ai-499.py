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
        print(f"Usage: python {pathlib.Path(__file__).name} <path_to_json_file>")
        sys.exit(1)

    json_path_str = sys.argv[1]
    json_path = pathlib.Path(json_path_str)

    # Check if the JSON file exists
    if not json_path.is_file():
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    # Read JSON data from file
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Extract data and texts from the config
    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']
    legend_labels = texts['legend_labels']

    fig = go.Figure()

    # Get all categories for the y-axis, preserving order from the JSON
    y_categories = [item['brand'] for item in chart_data]

    # Create a separate trace for each product type to ensure a correct legend
    for i, product_type in enumerate(legend_labels):
        x_values = []
        # Create a sparse list of values for the current product type
        for item in chart_data:
            if item['type'] == product_type:
                x_values.append(item['value'])
            else:
                x_values.append(None) # Use None for other categories to create gaps

        fig.add_trace(go.Bar(
            name=product_type,
            y=y_categories,
            x=x_values,
            orientation='h',
            marker=dict(
                color=colors[i],
                line=dict(color='black', width=1) # Border for the bars and legend markers
            )
        ))

    # Update layout to match the original chart's appearance
    fig.update_layout(
        barmode='stack', # 'stack' works correctly with None values to show single bars
        xaxis_title=texts['x_axis_title'],
        yaxis_title=texts['y_axis_title'],
        font=dict(family="Arial", size=12, color="black"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=150, r=40, t=30, b=60),
        yaxis=dict(
            autorange="reversed", # Reverses the order to match the image (top to bottom)
            showgrid=False,
            linecolor='black',
            linewidth=1.5,
            showline=True,
            mirror=True,
            ticks='outside'
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor='black',
            linewidth=1.5,
            showline=True,
            mirror=True,
            ticks='outside'
        ),
        legend=dict(
            x=0.98,
            y=0.02,
            xanchor='right',
            yanchor='bottom',
            bgcolor='rgba(255,255,255,0)', # Transparent background
            traceorder='normal'
        ),
        showlegend=True
    )

    # Define the output filename based on the input JSON filename
    output_filename = f"{json_path.stem}.png"

    # Save the chart as a PNG image
    fig.write_image(output_filename, scale=2)

    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()