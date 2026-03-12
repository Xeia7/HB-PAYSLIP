from fpdf import FPDF # fpdf2 still uses this import name

# ... (inside your button logic) ...

# 1. Initialize PDF
pdf = FPDF()
pdf.add_page()

# 2. Add a Unicode-friendly font (Built-in fonts like Helvetica don't always support ₱)
# We can use 'Arial' or 'helvetica' but replace the ₱ symbol with 'PHP' 
# or use a system font. To keep it simple and safe:
pdf.set_font("helvetica", 'B', 20)
pdf.cell(190, 15, "PAYMENT RECEIPT", ln=True, align='C')

# ... (rest of your layout) ...

# Use 'PHP' instead of the ₱ symbol to avoid encoding crashes
pdf.set_font("helvetica", size=12)
pdf.cell(140, 10, "Total Batch Funds")
pdf.cell(50, 10, f"PHP {total_money:,.2f}", ln=True, align='R')

# ... (and for the final payout) ...
pdf.set_font("helvetica", 'B', 14)
pdf.cell(140, 12, "NET SALARY", border=1, fill=True)
pdf.cell(50, 12, f"PHP {salary:,.2f}", border=1, fill=True, ln=True, align='R')

# 3. The New Output Method for fpdf2
pdf_output = pdf.output() # In fpdf2, output() returns bytes by default

st.download_button(
    label="Click here to download PDF",
    data=pdf_output,
    file_name=f"HB_Receipt_{batch_name}.pdf",
    mime="application/pdf"
)
