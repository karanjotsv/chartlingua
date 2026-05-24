import sys
import json
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Derive output filename from the input JSON path
    try:
        filename_base = json_path.rsplit('.', 1)[0]
    except IndexError:
        print("Error: Invalid JSON file path format.")
        sys.exit(1)

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    # Extract data from the JSON structure
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    # Prepare data for Plotly
    labels = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    # Create the pie chart trace
    pie_trace = go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
        hoverinfo='label+percent',
        textinfo='percent',
        textposition='auto',
        textfont=dict(family="Arial", size=14, color='black'),
        sort=False,  # Preserve the order from the JSON file
        direction='counterclockwise'
    )

    fig = go.Figure(data=[pie_trace])

    # Update layout
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(family="Arial", size=24, color='black')
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(family="Arial")
        ),
        font=dict(family="Arial", size=12, color='black'),
        paper_bgcolor='#E6E6FA',
        plot_bgcolor='#E6E6FA',
        margin=dict(l=40, r=40, t=120, b=120),
        showlegend=True
    )

    # Generate the output image
    output_filename = f"{filename_base}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()