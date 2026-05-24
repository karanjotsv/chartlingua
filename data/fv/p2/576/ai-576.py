import sys
import json
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_filepath = sys.argv[1]

    # Derive the output filename from the JSON file path
    try:
        output_filename_base = json_filepath.rsplit('.', 1)[0]
    except IndexError:
        print("Error: Invalid JSON file path provided.")
        sys.exit(1)

    # Read data from the JSON file
    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            chart_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_filepath}")
        sys.exit(1)

    # Extract data and texts from the JSON structure
    data_series = chart_data['chart_data']
    texts = chart_data['texts']
    colors = chart_data['colors']

    labels = [item['label'] for item in data_series]
    values = [item['value'] for item in data_series]

    # Create the figure
    fig = go.Figure()

    # Add the pie chart trace
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=1)
        ),
        textinfo='percent',
        textposition='outside',
        textfont=dict(size=14, family="Arial"),
        hoverinfo='label+percent',
        sort=False,  # Preserve the order from the JSON file
        direction='clockwise'
    ))

    # Update layout and styling
    fig.update_layout(
        title=dict(
            text=texts.get('title', ''),
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=22, family="Arial")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(family="Arial")
        ),
        font=dict(family="Arial"),
        paper_bgcolor='#F0F0FF',
        margin=dict(t=100, b=100, l=40, r=40)
    )

    # Generate the output image file path
    output_image_path = f"{output_filename_base}.png"

    # Save the figure as a PNG image
    try:
        fig.write_image(output_image_path, scale=2)
        print(f"Chart saved to {output_image_path}")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()