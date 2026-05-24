import sys
import json
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Derive output filename from JSON path
    if json_path.endswith('.json'):
        output_filename = json_path[:-5] + '.png'
    else:
        output_filename = json_path + '.png'

    # Read data from JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    # Extract data and settings from the JSON structure
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    # Prepare data for Plotly Pie chart
    values = [item['value'] for item in chart_data]
    
    # Create formatted labels for the legend, mimicking the original chart
    # The format is: Category Name followed by the value underlined on a new line.
    legend_labels = [f"{item['category']}<br><u>{item['value']}%</u>" for item in chart_data]
    
    # Use original category names for clean hover text
    hover_labels = [item['category'] for item in chart_data]

    # Create the Pie chart trace
    pie_trace = go.Pie(
        labels=legend_labels,
        values=values,
        marker=dict(colors=colors),
        sort=False,  # Preserve the original order of data
        direction='clockwise',
        textinfo='none',  # No text labels on the pie slices themselves
        hoverinfo='text',
        hovertext=[f'<b>{hover_labels[i]}</b><br>Value: {values[i]}%' for i in range(len(values))],
        showlegend=True
    )

    fig = go.Figure(data=[pie_trace])

    # Update layout
    fig.update_layout(
        title=dict(
            text=texts.get('title'),
            x=0.5,
            xanchor='center'
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        legend=dict(
            x=1.0,
            y=0.5,
            xanchor='left',
            yanchor='middle',
            traceorder='normal',
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=50, r=200, t=80, b=50), # Add right margin to prevent legend clipping
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    # Save the figure to a PNG file
    try:
        fig.write_image(output_filename, scale=2)
        print(f"Chart saved to {output_filename}")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()