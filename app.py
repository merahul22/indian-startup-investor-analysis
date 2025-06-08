import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout='wide', page_title='StartUp Analysis')

# Load and clean data
df = pd.read_csv('startup_cleaned.csv')
df['investors'] = df['investors'].fillna('Unknown')
df['investors'] = df['investors'].str.split(',').apply(lambda x: [i.strip() for i in x])
df_exploded = df.explode('investors')  # Each row now has one investor

def load_overall_analysis():
    st.title('Overall Startup Funding Analysis')

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=['date'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # Cards Section
    total = round(df['amount'].sum())
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total Funding', f"{total} Cr")
    with col2:
        st.metric('Max Funding', f"{max_funding} Cr")
    with col3:
        st.metric('Avg Funding', f"{round(avg_funding)} Cr")
    with col4:
        st.metric('Funded Startups', num_startups)

    # MoM Chart
    st.header('Month-on-Month (MoM) Analysis')
    temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index(name='value')

    temp_df['date_label'] = pd.to_datetime(temp_df[['year', 'month']].assign(day=1))
    temp_df['x_axis'] = temp_df['date_label'].dt.strftime('%b %Y')

    # MoM chart inside smaller column layout
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(temp_df['x_axis'], temp_df['value'], marker='o', color='darkblue')
        ax.set_xlabel('Month-Year')
        ax.set_ylabel('Amount' if option == 'Total Funding' else 'Count')
        ax.set_title(f"MoM {option}")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

    # Sector Analysis
    st.header("Sector Analysis")
    sector_data = df['vertical'].value_counts().head(10)


    col3, col4 = st.columns(2)
    with col3:
        fig2, ax2 = plt.subplots()
        ax2.pie(sector_data, labels=sector_data.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title(f"Top 10 Sectors by Funding count")
        st.pyplot(fig2)

    # Type of Funding Pie Chart
    st.header("Type of Funding")
    funding_series = df['round'].value_counts().head(10)
    col5, col6 = st.columns(2)
    with col5:
        fig3, ax3 = plt.subplots()
        ax3.pie(funding_series, labels=funding_series.index, autopct='%1.1f%%', startangle=90)
        ax3.set_title("Top Funding Types")
        st.pyplot(fig3)

    # City-wise Funding
    st.header("City-wise Funding")
    city_series = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
    col7, col8 = st.columns(2)
    with col7:
        fig4, ax4 = plt.subplots()
        ax4.bar(city_series.index, city_series.values, color='teal')
        ax4.set_ylabel("Amount")
        ax4.set_title("Top Cities by Funding Amount")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig4)

    # Top Startups Year-wise
    st.header("Top Startups by Year")
    year_list = sorted(df['year'].dropna().unique())
    selected_year = st.selectbox("Select Year", year_list)
    top_startups = df[df['year'] == selected_year].groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_startups)

    # Top Investors
    st.header("Top Investors")
    top_investors = df_exploded['investors'].value_counts().head(10)
    st.bar_chart(top_investors)

    # Funding Heatmap
    st.header("Funding Heatmap (Year vs Month)")
    heatmap_data = df.pivot_table(index='month', columns='year', values='amount', aggfunc='sum').fillna(0)
    st.dataframe(heatmap_data.style.background_gradient(cmap='YlGnBu'))


def load_investor_analysis(investor):
    st.header(investor)

    # Filter rows for selected investor
    investor_df = df_exploded[df_exploded['investors'] == investor]

    # Recent 5 investments
    last5_df = investor_df[['date', 'startup', 'vertical', 'city', 'round', 'amount']].sort_values(
        by='date', ascending=False).head()
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Biggest Investments')
        big_series = investor_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(big_series.index, big_series.values, color='skyblue')
        ax.set_ylabel("Amount (in Crores)")
        ax.set_title("Top Startups by Investment")
        st.pyplot(fig)

    with col2:
        st.subheader('Sectors Invested In')
        sector_series = investor_df.groupby('vertical')['amount'].sum()
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        ax1.pie(sector_series, labels=sector_series.index, autopct="%0.1f%%", startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader('Cities Invested In')
        city_series = investor_df.groupby('city')['amount'].sum()
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        ax2.pie(city_series, labels=city_series.index, autopct="%0.1f%%", startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)

    with col4:
        st.subheader('Investment Stages')
        stage_series = investor_df.groupby('round')['amount'].sum()
        fig4, ax4 = plt.subplots(figsize=(5, 3))
        ax4.pie(stage_series, labels=stage_series.index, autopct="%0.1f%%", startangle=90)
        ax4.axis('equal')
        st.pyplot(fig4)

    st.subheader("Year-over-Year Investment by " + investor)
    investor_df['year'] = pd.to_datetime(investor_df['date']).dt.year
    yoy_series = investor_df.groupby('year')['amount'].sum()

    fig3, ax3 = plt.subplots(figsize=(4, 2))
    ax3.plot(yoy_series.index, yoy_series.values, marker='o', linestyle='-', color='green')
    ax3.set_title("YoY Investment Trend")
    ax3.set_xlabel("Year")
    ax3.set_ylabel("Total Investment Amount")
    st.pyplot(fig3)

    st.subheader("Similar Investors (Same City)")

    # Get cities where investor invested
    investor_cities = investor_df['city'].unique()

    # Filter rows for those cities (excluding selected investor)
    similar_df = df_exploded[(df_exploded['city'].isin(investor_cities)) & (df_exploded['investors'] != investor)]

    if not similar_df.empty:
        similar_investors = similar_df['investors'].value_counts().head().reset_index()
        similar_investors.columns = ['Investor', 'Investment Count']
        st.write(f"Investors who also invested in {', '.join(investor_cities)}:")
        st.dataframe(similar_investors)
    else:
        st.info("No similar investors found in the same city.")


# Sidebar UI
st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'StartUp', 'Investor'])

if option == 'Overall Analysis':
    st.title("Overall Startup Funding Analysis")
    btn0=st.sidebar.button('Show Overall Analysis')
    # st.write("This section is under construction."
    if btn0:
        load_overall_analysis()


elif option == 'StartUp':
    startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title("Startup Analysis")
    if btn1:
        st.subheader(startup)
        startup_df = df[df['startup'] == startup]
        first_row = startup_df.iloc[0]
        st.markdown(f"""
               - **Name:** {startup}
               - **Founders:** {first_row.get('founders', 'Unknown')}
               - **Industry:** {first_row.get('vertical', 'Unknown')}
               - **Subindustry:** {first_row.get('subvertical', 'N/A')}
               - **Location:** {first_row.get('city', 'Unknown')}
               - **Funding Rounds:** {startup_df['round'].nunique()}
               - **Stage:** {first_row.get('stage', first_row.get('round', 'Unknown'))}
               - **Investors:** {', '.join(set([inv.strip() for lst in startup_df['investors'] for inv in lst if isinstance(lst, list)]))}
               - **First Funding Date:** {startup_df['date'].min()}
               - **Latest Funding Date:** {startup_df['date'].max()}
               """)
        st.subheader("💰 All Funding Rounds")
        st.dataframe(startup_df[['date', 'amount', 'round', 'investors']].sort_values(by='date', ascending=False))

        st.subheader("🧭 Similar Companies (Same Industry & City)")
        similar_df = df[
            (df['vertical'] == first_row['vertical']) &
            (df['city'] == first_row['city']) &
            (df['startup'] != startup)
            ]
        if not similar_df.empty:
            st.dataframe(similar_df[['startup', 'vertical', 'city', 'amount']].drop_duplicates().head(5))
        else:
            st.info("No similar companies found.")

else:
    # Investor option
    unique_investors = sorted(df_exploded['investors'].dropna().unique().tolist())
    selected_investor = st.sidebar.selectbox('Select Investor', unique_investors)
    btn2 = st.sidebar.button('Find Investor Details')
    st.title("Investor Funding Analysis")
    if btn2:
        load_investor_analysis(selected_investor)
