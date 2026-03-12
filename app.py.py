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
    }
    .salary-card {
        padding: 20px;
        border-radius: 15px;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .metric-label {
        color: #6c757d;
        font-size: 14px;
    }
    .metric-value {
        color: #1d3557;
        font-size: 32px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")
    st.info("Ensure your 'Total Records' matches the batch sheet exactly for accuracy.")
    if st.button("Reset Calculator"):
        st.rerun()

# --- App Header ---
st.title("💰 HB Salary Calculator")
st.markdown("Calculate your earnings and generate professional receipts instantly.")
st.divider()

# --- Input Section (2 Columns) ---
col1, col2 = st.columns(2)

with col1:
    total_money = st.number_input("Total EastWest Funds (₱)", min_value=0.0, format="%.2f")
    total_records = st.number_input("Total Batch Records", min_value=1, step=1)

with col2:
    records_done = st.number_input("Your Records Completed", min_value=0, step=1)
    batch_name = st.text_input("Batch Name (Lodo)", placeholder="e.g. Batch 42-A")

# --- Logic & Results ---
if total_records > 0:
    rate_per_record = total_money / total_records
    salary = rate_per_record * records_done

    # Aesthetic Result Card
    st.markdown(f"""
        <div class="salary-card">
            <div class="metric-label">Estimated Payout</div>
            <div class="metric-value">₱{salary:,.2f}</div>
            <div style="color: #2a9d8f; font-size: 12px;">Rate per record: ₱{rate_per_record:.4f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # --- PDF Receipt Section ---
    st.subheader("📄 Generate Official Receipt")
    user_name = st.text_input("Full Name for Receipt")
    
    if st.button("Prepare PDF"):
        if not user_name or not batch_name:
            st.warning("Please enter your Name and Batch Name to generate the PDF.")
        else:
            # Generate PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Simple, clean design for PDF
            pdf.set_font("Helvetica", 'B', 20)
            pdf.set_text_color(29, 53, 87)
            pdf.cell(190, 15, "PAYMENT RECEIPT", ln=True, align='C')
            
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(100)
            pdf.cell(190, 10, f"Generated on: {datetime.date.today()}", ln=True, align='C')
            pdf.ln(10)
            
            pdf.set_font("Helvetica", 'B', 12)
            pdf.set_text_color(0)
            pdf.cell(95, 10, f"Recipient: {user_name}")
            pdf.cell(95, 10, f"Batch: {batch_name}", ln=True, align='R')
            pdf.line(10, 55, 200, 55)
            pdf.ln(15)
            
            pdf.set_font("Helvetica", size=12)
            pdf.cell(140, 10, "Total Batch Funds")
            pdf.cell(50, 10, f"₱{total_money:,.2f}", ln=True, align='R')
            
            pdf.cell(140, 10, "Total Records in Batch")
            pdf.cell(50, 10, f"{total_records}", ln=True, align='R')
            
            pdf.cell(140, 10, "Your Contribution (Records)")
            pdf.cell(50, 10, f"{records_done}", ln=True, align='R')
            
            pdf.ln(10)
            pdf.set_font("Helvetica", 'B', 14)
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(140, 12, "NET SALARY", border=1, fill=True)
            pdf.cell(50, 12, f"₱{salary:,.2f}", border=1, fill=True, ln=True, align='R')

            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="Click here to download PDF",
                data=pdf_output,
                file_name=f"HB_Receipt_{batch_name}.pdf",
                mime="application/pdf"
            )