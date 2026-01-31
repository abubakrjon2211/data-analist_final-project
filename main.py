import streamlit as st
import plotly.express as px
import db

st.set_page_config(page_title="Auto Market Analytics", layout="wide")

def main():
    """Main function to render the dashboard."""
    st.title("Auto Market Analytics: Dushanbe (PostgreSQL)")
    st.markdown("**Student:** Rustamov Abubakr")
    
    try:
        df = db.get_all_cars()
        stats = db.get_brand_stats()
    except Exception as e:
        st.error(f"Database error: {e}")
        return

    st.sidebar.header("Filters")
    
    all_brands = sorted(df['brand_name'].unique())
    selected_brands = st.sidebar.multiselect(
        "Select Brands", 
        all_brands, 
        default=all_brands[:3] if len(all_brands) > 3 else all_brands
    )

    min_p, max_p = int(df['price'].min()), int(df['price'].max())
    price_range = st.sidebar.slider("Price Range (TJS)", min_p, max_p, (min_p, max_p))

    if not selected_brands:
        st.warning("Please select at least one brand.")
        return

    filtered_df = df[
        (df['brand_name'].isin(selected_brands)) &
        (df['price'] >= price_range[0]) &
        (df['price'] <= price_range[1])
    ]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Ads", len(filtered_df))
    if not filtered_df.empty:
        col2.metric("Avg Price", f"{int(filtered_df['price'].mean()):,} TJS".replace(",", " "))
        col3.metric("Min Price", f"{filtered_df['price'].min():,} TJS".replace(",", " "))

    st.subheader("Brand Distribution")
    count_by_brand = filtered_df['brand_name'].value_counts().reset_index()
    count_by_brand.columns = ['Brand', 'Count']
    fig1 = px.bar(count_by_brand, x='Brand', y='Count', color='Brand', text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Price vs Year")
        fig2 = px.scatter(
            filtered_df, 
            x='year', 
            y='price', 
            color='brand_name',
            hover_data=['model_name', 'title']
        )
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.subheader("Price Distribution")
        fig3 = px.box(filtered_df, x='brand_name', y='price', color='brand_name')
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Market Leaders (Top 10)")
    st.dataframe(stats.head(10), use_container_width=True)

    with st.expander("Raw Data View"):
        st.dataframe(filtered_df)

if __name__ == "__main__":
    main()