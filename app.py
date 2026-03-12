import streamlit as st
from fpdf import FPDF
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="HB Salary Pro",
    page_icon="💰",
    layout="centered"
)

# --- Custom CSS for Aesthetics ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
    .salary-card {
        padding: 25px;
        border-radius: 15px;
        background: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #efefef;
        margin: 20px 0;
    }
    .metric-label {
        color: #6c757d;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        color: #1d3557;
        font-size: 36px;
        font-weight: 800;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("Help & Settings")
    st.markdown("""
    **How to use:**
    1. Enter the total batch funds from EastWest.
    2. Enter the total records in that batch.
    3. Enter the records you personally finished.
    """)
    if st.button("Reset Calculator"):
        st.rerun()

# --- App Header ---
st.title("💰 HB Salary Calculator")
st.markdown("Generate professional receipts for your batch work.")
st.divider()

# --- Input Section ---
col1, col2 = st.columns(2)

with col1:
    total_money = st.number_input("Total EastWest Funds (₱)", min_value=0.0, format="%.2f", help="The total amount received for the whole batch.")
    total_records = st.number_input("Total Batch Records", min_value=1, step=1)

with col2:
    records_done = st.number_input("Your Records Completed", min_value=0, step=1)
    batch_name = st.text_input("Batch Name (Lodo)", placeholder="e.g. Batch 105-A")

# --- Logic & Results ---
if total_records > 0:
    rate_per_record = total_money / total_records
    salary = rate_per_record * records_done

    # Aesthetic Result Card
    st.markdown(f"""
        <div class="salary-card">
            <div class="metric-label">Your Estimated Payout</div>
            <div class="metric-value">₱{salary:,.2f}</div>
            <div style="color: #2a9d8f; font-size: 13px; font-weight: 600;">
                Rate per record: ₱{rate_per_record:.4f}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # --- PDF Receipt Section ---
    st.subheader("📄 Generate Official Receipt")
    user_name = st.text_input("Full Name for Receipt")
    
    if st.button("Prepare PDF Receipt"):
        if not user_name or not batch_name:
            st.error("Missing Information: Please enter your Name and Batch Name.")
        else:
            # Generate PDF using fpdf2
            pdf = FPDF()
            pdf.add_page()
            
            # Header
            pdf.set_font("helvetica", 'B', 20)
            pdf.set_text_color(29, 53, 87)
            pdf.cell(190, 20, "PAYMENT RECEIPT", ln=True, align='C')
            
            # Date & Info
            pdf.set_font("helvetica", size=10)
            pdf.set_text_color(120)
            pdf.cell(190, 10, f"Issued on: {datetime.date.today().strftime('%B %d, %Y')}", ln=True, align='C')
            pdf.ln(10)
            
            # User Info Row
            pdf.set_font("helvetica", 'B', 11)
            pdf.set_text_color(0)
            pdf.cell(95, 10, f"Recipient: {user_name.upper()}")
            pdf.cell(95, 10, f"Batch ID: {batch_name}", ln=True, align='R')
            
            # Draw a line
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, 65, 200, 65)
            pdf.ln(15)
            
            # Breakdown Table
            pdf.set_font("helvetica", size=11)
            pdf.cell(140, 10, "Total Batch Funds (EastWest)")
            pdf.cell(50, 10, f"PHP {total_money:,.2f}", ln=True, align='R')
            
            pdf.cell(140, 10, "Total Records in Batch")
            pdf.cell(50, 10, f"{total_records:,}", ln=True, align='R')
            
            pdf.cell(140, 10, "Your Completed Records")
            pdf.cell(50, 10, f"{records_done:,}", ln=True, align='R')
            
            pdf.ln(10)
            
            # Final Total Box
            pdf.set_font("helvetica", 'B', 14)
            pdf.set_fill_color(245, 247, 250)
            pdf.cell(140, 15, " TOTAL PAYOUT", border='TB', fill=True)
            pdf.cell(50, 15, f"PHP {salary:,.2f} ", border='TB', fill=True, ln=True, align='R')

            # Footer Note
            pdf.set_y(-30)
            pdf.set_font("helvetica", 'I', 8)
            pdf.set_text_color(150)
            pdf.cell(190, 10, "This is an auto-generated breakdown for records tracking purposes.", align='C')

            # Output as bytes for Streamlit
            pdf_bytes = pdf.output()
            
            st.success("PDF Generated Successfully!")
            st.download_button(
                label="📥 Download PDF Receipt",
                data=pdf_bytes,
                file_name=f"Receipt_{batch_name}_{user_name.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
