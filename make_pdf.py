from reportlab.pdfgen import canvas

def create_toxic_pdf():
    c = canvas.Canvas("toxic_contract.pdf")
    c.drawString(100, 800, "CONFIDENTIAL SERVICE AGREEMENT")
    c.drawString(100, 780, "BETWEEN:")
    c.drawString(100, 760, "Party A: VIPS Consulting Group")
    c.drawString(100, 740, "AND")
    c.drawString(100, 720, "Party B: FTX Trading Ltd (Sam Bankman-Fried)") 
    
    c.drawString(100, 680, "1. INDEMNITY")
    c.drawString(100, 660, "Party B agrees to hold Party A harmless for all financial losses.")
    c.drawString(100, 640, "2. PAYMENT")
    c.drawString(100, 620, "All payments shall be made in FTT Tokens.")
    
    c.save()
    print("SUCCESS: 'toxic_contract.pdf' created.")

if __name__ == "__main__":

    create_toxic_pdf()
