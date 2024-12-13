import streamlit as st
import pandas as pd
import plotly.express as px


# File Uploader
# uploaded_file = st.file_uploader("Upload your flight dataset (XLSX)", type="xlsx")


# Function to load the processed data
@st.cache_data
def load_data(filepath="data/Flight_datasets.xlsx"):
    """
    Loads the processed dataset.

    Args:
        filepath (str): Path to the processed dataset.

    Returns:
        pd.DataFrame: Loaded data.
    """
    try:
        df = pd.read_excel(filepath)
        return df
    except FileNotFoundError:
        st.error("Processed dataset not found. Please run the processing script first.")
        return pd.DataFrame()


# Main function to run the Streamlit app
def main():
    # Load the Excel file
    # df = pd.read_excel(uploaded_file)

    # App Title
    st.title("Flight Dashboard")
    st.write("This dashboard displays the flight data insights and allows stakeholders to filter and search the records.")

    # Load the processed data
    df = load_data()
    if df.empty:
        st.warning("No data to display. Please ensure the dataset is processed and available.")
        return
    
    # Display Dataset Preview
    st.write("Dataset Preview:")
    st.dataframe(df)

    # Sidebar Title
    st.sidebar.title("Flight Data Insights")

    # Filter by Airline, Source City and Destination City
    airline_filter = st.sidebar.selectbox("Select Airline",  ["All"] + list(df["Airline"].unique()))
    source_city = st.sidebar.selectbox("Select Source City",  ["All"] + list(df["Source"].unique()))
    destination_city = st.sidebar.selectbox("Select Destination City",  ["All"] + list(df["Destination"].unique()))

    filtered_data = df[
        ((df["Airline"] == airline_filter) | (airline_filter == "All")) &
        ((df["Source"] == source_city) | (source_city == "All")) &
        ((df["Destination"] == destination_city) | (destination_city == "All"))
        ]
    # filtered_data = df[(df["Airline"] == airline_filter) & (df["Source"] == source_city) & (df["Destination"] == destination_city)]

    # Price By Airline table
    st.subheader(f"Flights by Airline: {airline_filter}, from {source_city} to {destination_city}")
    st.dataframe(filtered_data)

    # route_data = df[(df["Source"] == source_city) & (df["Destination"] == destination_city)]
    # st.subheader(f"Flights from {source_city} to {destination_city}")
    # st.dataframe(route_data)

    # Price by Distribution (Boxplot for all airlines)
    st.subheader("Price Distribution by Airline")
    fig_price_dist = px.box(df,
                            x="Airline",
                            y="Price",
                            color="Airline",
                            title="Price Distribution by Airline")
    st.plotly_chart(fig_price_dist)

    # Price Trends by Destination (Enhanced)
    st.subheader("Price Trends by Destination")

    # Aggregating data by month for better readability
    df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'])
    df['Month'] = df['Date_of_Journey'].dt.to_period('M').astype(str)  # Convert Period to string

    # Group data by Month and Destination
    monthly_price = df.groupby(['Month', 'Destination'])['Price'].mean().reset_index()

    # Plotting the line chart with enhanced features
    fig_price_trends = px.line(monthly_price,
                               x='Month',
                               y='Price',
                               color='Destination',
                               title='Price Trends by Destination',
                               labels={'Month': 'Month', 'Price': 'Average Price'},
                               line_shape='linear',  # Makes the lines smooth
                               markers=True,  # Adds markers to the lines for better visibility
                               template="plotly_dark")  # Optional: Use a dark template for a cleaner look

    # Make sure the x-axis labels are readable
    fig_price_trends.update_xaxes(tickangle=45, tickmode='array')

    # Display the plot
    st.plotly_chart(fig_price_trends)

    # Average Price by Total Stops
    st.subheader("Average Price by Total Stops")
    avg_price_stops = filtered_data.groupby("Total_Stops")["Price"].mean().reset_index()
    fig_avg_price = px.bar(avg_price_stops,
                           x="Total_Stops",
                           y="Price",
                           color="Total_Stops",
                           title="Average Price by Total Stops")
    st.plotly_chart(fig_avg_price)

    # Distribution of Source Cities
    st.subheader("Distribution of Flights by Source")
    fig_source_dist = px.pie(filtered_data,
                             names="Source",
                             title="Flight Distribution by Source City")
    st.plotly_chart(fig_source_dist)

    # Price by Source City (Bar Chart)
    st.subheader("Price by Source City")
    price_by_source = df.groupby("Source")["Price"].mean().reset_index()
    fig_price_by_source = px.bar(price_by_source,
                                 x="Source",
                                 y="Price",
                                 color="Source",
                                 title="Average Price by Source City")
    st.plotly_chart(fig_price_by_source)

    # Price by Airline and Total Stops (Bar Chart)
    st.subheader("Price by Airline and Total Stops")
    price_by_airline_stops = df.groupby(['Airline', 'Total_Stops'])['Price'].mean().reset_index()
    fig_price_airline_stops = px.bar(price_by_airline_stops,
                                     x="Airline",
                                     y="Price",
                                     color="Total_Stops",
                                     title="Price by Airline and Total Stops",
                                     barmode='group')
    st.plotly_chart(fig_price_airline_stops)

    # Price Distribution by Time of Day (Boxplot)
    st.subheader("Price Distribution by Time of Day")
    df['Dep_Time'] = pd.to_datetime(df['Dep_Time'])
    df['Hour_of_Day'] = df['Dep_Time'].dt.hour
    fig_price_time = px.box(df,
                            x="Hour_of_Day",
                            y="Price",
                            title="Price Distribution by Time of Day")
    st.plotly_chart(fig_price_time)

    # Flights by Route (Pie Chart)
    st.subheader("Flights by Route")
    fig_route_dist = px.pie(df,
                            names="Route",
                            title="Flight Distribution by Route")
    st.plotly_chart(fig_route_dist)

    # Duration vs Price
    st.subheader("Duration vs Price")
    fig_duration_price = px.scatter(filtered_data,
                                    x="Duration",
                                    y="Price",
                                    color="Airline",
                                    title="Duration vs Price by Airline",
                                    hover_data=["Source", "Destination"])
    st.plotly_chart(fig_duration_price)

    # Footer Note
    st.sidebar.markdown("This dashboard provides insights into flight data.")


# Entry point for the Streamlit app
if __name__ == "__main__":
    main()
