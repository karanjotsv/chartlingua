import sys
import json
import os
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Check if the file exists
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    # Extract data from the JSON structure
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    # Prepare data for Plotly pie chart
    labels = [f"{item['category']} ({item['value']}%)" for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the pie chart trace
    pie_trace = go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
        sort=False,  # Preserve the order from the JSON data
        direction='clockwise',
        textinfo='none',
        hoverinfo='skip'
    )

    # Create the figure
    fig = go.Figure(data=[pie_trace])

    # Update layout for a clean and accurate look
    fig.update_layout(
        title=dict(
            text=texts.get('title'),
            x=0.05,
            xanchor='left',
            font=dict(
                family="Arial",
                size=20,
                color='black'
            )
        ),
        font=dict(family="Arial"),
        showlegend=True,
        legend=dict(
            font=dict(size=12)
        ),
        margin=dict(l=20, r=40, t=80, b=20),
        width=800,
        height=600
    )

    # Determine the output filename from the input JSON path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Save the figure as a PNG image
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart successfully saved to '{output_filename}'")
    except Exception as e:
        print(f"An error occurred while saving the image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()