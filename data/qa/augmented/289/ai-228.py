import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Generates a chart from a JSON configuration file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]
    base_filename = pathlib.Path(json_path).stem

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: Could not read or parse the JSON file at {json_path}. Details: {e}")
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    if not chart_data or not colors:
        print("Error: JSON file must contain 'chart_data' and 'colors'.")
        sys.exit(1)

    # Prepare data for plotting
    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the figure
    fig = go.Figure()

    # Add the bar trace
    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker_color=colors[0],
        text=[str(v) for v in values],
        textposition='outside',
        cliponaxis=False
    ))

    # Update layout to match the source image aesthetic
    fig.update_layout(
        font_family="Arial",
        plot_bgcolor='white',
        showlegend=False,
        xaxis=dict(
            title=texts.get('x_axis_title'),
            showgrid=True,
            gridcolor='#EAEAEA',
            griddash='dot',
            gridwidth=1,
            zeroline=False,
            ticks='outside',
            tickcolor='lightgrey',
            showline=False
        ),
        yaxis=dict(
            title=texts.get('y_axis_title'),
            autorange='reversed',  # Display categories from top to bottom
            showgrid=False,
            ticks='',  # Hide y-axis tick marks
            showline=True,
            linecolor='black',
            linewidth=1
        ),
        margin=dict(l=200, r=60, t=30, b=80)  # Adjust margins
    )

    # Add source text as an annotation
    source_text = texts.get('source')
    if source_text:
        fig.add_annotation(
            text=source_text,
            xref="paper", yref="paper",
            x=0.98, y=-0.15,
            showarrow=False,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12, color="#666666")
        )

    # Generate and save the image file
    output_path = f"{base_filename}.png"
    try:
        fig.write_image(output_path, scale=2)
        print(f"Chart successfully generated and saved to {output_path}")
    except Exception as e:
        print(f"Error writing image file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()