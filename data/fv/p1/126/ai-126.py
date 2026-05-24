import sys
import json
import plotly.graph_objects as go
import os

def main():
    """
    Main function to generate a pie chart from a JSON file.
    """
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Ensure the input file is a .json file
    if not json_path.endswith('.json'):
        print("Error: Input file must be a .json file.")
        sys.exit(1)

    # Read data from JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{json_path}' contains invalid JSON.")
        sys.exit(1)


    # Extract data from the loaded JSON
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    # Prepare data for Plotly
    labels = [item['label'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the pie chart trace
    pie_trace = go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='#FFFFFF', width=2)
        ),
        textinfo='percent',
        texttemplate='%{value}%',
        hoverinfo='label+percent',
        sort=False,  # Preserve the original order from the JSON
        direction='clockwise',
        textfont=dict(size=14)
    )

    # Create the figure
    fig = go.Figure(data=[pie_trace])

    # Update layout
    title_text = texts.get('title')

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        legend=dict(
            x=0.01,
            y=0.98,
            xanchor='left',
            yanchor='top',
            traceorder='normal' # Follows the order of data provided
        ),
        margin=dict(l=150, r=40, t=100, b=40)
    )
    
    # Update text position and font for slices
    fig.update_traces(
        insidetextorientation='radial',
        textposition='inside'
    )

    # Define output filename
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Save the figure as a PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    main()