import gradio as gr
import re

def audit_recruiter(sender_email, email_body):
    risk_score = 0
    flags = []
    
    # Normalize text
    body_lower = email_body.lower()
    sender_lower = sender_email.lower()

    # --- TIER 3 "BODY SHOP" INDICATORS (High Risk) ---
    
    # The "Lock-In" Clause
    if "right to represent" in body_lower or "rtr" in body_lower:
        risk_score += 25
        flags.append("🚨 **RTR Demand:** Immediate request for 'Right to Represent' suggests they do not own the client relationship.")

    # The "Urgency" Trap
    if "urgent requirement" in body_lower or "immediate interview" in body_lower:
        risk_score += 15
        flags.append("⚠️ **False Urgency:** High-pressure tactics are common in low-tier harvesting.")

    # The "Identity" Flags
    if "iselin" in body_lower and "nj" in body_lower:
        risk_score += 20
        flags.append("📍 **The 'Iselin' Hub:** Address associated with high-volume offshore recruitment farms.")
    
    if "whatsapp" in body_lower:
        risk_score += 10
        flags.append("🚩 **Unprofessional Channel:** Requesting WhatsApp communication is a common scam indicator.")

    # --- KEYWORD MISMATCH (The "Shotgun" Approach) ---
    # Detects if they are pitching a low-level role to a high-level profile
    low_level_keywords = ["qa analyst", "tester", "entry level", "junior", "c++", "java developer"]
    for word in low_level_keywords:
        if word in body_lower:
            risk_score += 5
            flags.append(f"📉 **Role Mismatch:** Recruiter is blasting '{word}' roles via script (Resume Farming).")
            break # Only count once

    # --- SENDER DOMAIN ANALYSIS ---
    generic_domains = ["gmail.com", "yahoo.com", "hotmail.com"]
    if any(domain in sender_lower for domain in generic_domains):
        risk_score += 20
        flags.append("📧 **Generic Domain:** Professional recruiters rarely use public Gmail/Yahoo addresses.")

    # --- VERDICT LOGIC ---
    if risk_score >= 40:
        verdict = "🔴 TIER 3: HIGH RISK / SPAM"
        action = "DELETE IMMEDIATELY. Do not reply. Do not sign RTR."
        box_color = "red"
    elif risk_score >= 20:
        verdict = "🟠 TIER 2: CAUTION / VOLUME RECRUITER"
        action = "Proceed with caution. Verify client relationship before sending resume."
        box_color = "orange"
    else:
        verdict = "🟢 TIER 1: LIKELY LEGITIMATE"
        action = "Appears to be a standard or retained search engagement."
        box_color = "green"

    # --- REPORT GENERATION ---
    report = f"""
    ## Audit Verdict: <span style='color:{box_color}'>{verdict}</span>
    **Risk Score:** {risk_score}/100
    
    ### 🛡️ Recommended Action:
    **{action}**
    
    ### 🔍 Forensic Findings:
    """
    if not flags:
        report += "\n- No obvious risk vectors detected."
    else:
        for f in flags:
            report += f"\n- {f}"
            
    return report

# --- UI LAYOUT ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🐍 V.I.P.E.R. Audit Engine
    ### Vendor Integrity & Personnel Email Reconnaissance
    **Cata Risk Lab** | Sovereign AI & Data Privacy
    """)
    
    with gr.Row():
        with gr.Column():
            sender_input = gr.Textbox(label="Sender Email Address", placeholder="recruiter@company.com")
            body_input = gr.Textbox(label="Email Content", placeholder="Paste the job inquiry here...", lines=10)
            btn = gr.Button("🔍 Run Forensic Scan", variant="primary")
        
        with gr.Column():
            output_box = gr.Markdown(label="Forensic Report")
            
    gr.Markdown("---")
    gr.Markdown("*Disclaimer: This tool uses heuristic pattern matching to identify common markers of low-integrity recruitment. It is for educational and privacy-protection purposes only.*")

    btn.click(fn=audit_recruiter, inputs=[sender_input, body_input], outputs=output_box)

if __name__ == "__main__":
    demo.launch()
