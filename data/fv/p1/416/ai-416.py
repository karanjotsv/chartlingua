import sys
import json
import plotly.graph_objects as go
import os

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Ensure the JSON file exists
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)

    # Derive output filename from JSON path
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_name}.png"

    # Read and parse the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract data from the JSON structure
    chart_data = data['chart_data']
    texts = data['texts']
    colors = data['colors']
    y_axis_ticks = data['y_axis_ticks']

    # Prepare data for Plotly
    x_values = [item['x'] for item in chart_data]
    y_values = [item['y'] for item in chart_data]
    
    # Use general number formatting for text to handle integers and floats cleanly
    text_labels = [f'{y:.2g}' for y in y_values]

    # Create the figure
    fig = go.Figure()

    # Add the bar trace
    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values,
        marker_color=colors[0],
        marker_line=dict(color='white', width=1),
        text=text_labels,
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black'),
        cliponaxis=False # Prevent text from being clipped at the top
    ))

    # Update layout
    fig.update_layout(
        title=dict(
            text=texts['title'],
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(family='Arial', size=16)
        ),
        xaxis=dict(
            title=texts['x_axis_title'],
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            showgrid=True,
            gridcolor='#D3D3D3'
        ),
        yaxis=dict(
            title=texts['y_axis_title'],
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            tickvals=y_axis_ticks,
            ticktext=[f'{t:.2g}' for t in y_axis_ticks],
            range=[0, max(y_axis_ticks) * 1.1],
            showgrid=True,
            gridcolor='#D3D3D3'
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=90, r=30, t=80, b=180) # Increased bottom margin for long source
    )

    # Add source annotation at the bottom
    fig.add_annotation(
        text=texts['source'],
        align='left',
        showarrow=False,
        xref='paper', yref='paper',
        x=0, y=-0.35, # Adjust y position to fit below x-axis title
        xanchor='left', yanchor='top',
        font=dict(family='Arial', size=10)
    )

    # Write the image file
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()