import streamlit as st
import pandas as pd

def calculate_duration_multiplier(duration):
    """Calculate the multiplier based on deal duration."""
    duration_multipliers = {
        3: 0.20,  # 20% increase
        4: 0.30,  # 30% increase
        5: 0.50,  # 50% increase
    }
    return duration_multipliers.get(duration, 0.0)

def calculate_commission(deal_size, deal_duration, yearly_target, yearly_bonus):
    """Calculate commission based on input parameters."""
    # Calculate base rate
    base_rate = yearly_bonus / yearly_target
    
    # Get duration multiplier
    duration_multiplier = calculate_duration_multiplier(deal_duration)
    
    # Calculate final commission
    commission = deal_size * base_rate * duration_multiplier
    
    return {
        'base_rate': base_rate,
        'duration_multiplier': duration_multiplier,
        'commission': commission
    }

# Set page config
st.set_page_config(
    page_title="Commission Calculator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Add custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .result-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("💰 Commission Calculator")
st.write("Calculate your commission based on deal parameters and targets.")

# Create two columns for input fields
col1, col2 = st.columns(2)

with col1:
    st.subheader("Deal Information")
    deal_size = st.number_input(
        "Deal Size (GBP)",
        min_value=0,
        value=100000,
        step=1000,
        help="Enter the total deal value in GBP"
    )
    
    deal_duration = st.selectbox(
        "Deal Duration (Years)",
        options=[1, 2, 3, 4, 5],
        index=2,
        help="Select the duration of the deal in years"
    )

with col2:
    st.subheader("Target Information")
    yearly_target = st.number_input(
        "Yearly Target (GBP)",
        min_value=0,
        value=1000000,
        step=10000,
        help="Enter your yearly target in GBP"
    )
    
    yearly_bonus = st.number_input(
        "Yearly Bonus (GBP)",
        min_value=0,
        value=100000,
        step=1000,
        help="Enter your yearly bonus in GBP"
    )

# Calculate button
if st.button("Calculate Commission", type="primary"):
    if yearly_target == 0:
        st.error("Yearly target cannot be zero!")
    else:
        result = calculate_commission(deal_size, deal_duration, yearly_target, yearly_bonus)
        
        # Display results in a nice format
        st.markdown("### Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Base Rate",
                f"{result['base_rate']:.2%}"
            )
        
        with col2:
            st.metric(
                "Duration Multiplier",
                f"{result['duration_multiplier']:.2%}"
            )
        
        with col3:
            st.metric(
                "Commission",
                f"£{result['commission']:,.2f}"
            )
        
        # Show calculation breakdown
        st.markdown("### Calculation Breakdown")
        st.markdown(f"""
        ```
        Commission = Deal Size × Base Rate × Duration Multiplier
        Commission = £{deal_size:,} × {result['base_rate']:.2%} × {result['duration_multiplier']:.2%}
        Commission = £{result['commission']:,.2f}
        ```
        """)