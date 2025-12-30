import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yaml
from pathlib import Path
from datetime import datetime
import json

# Page Configuration
st.set_page_config(
    page_title="HealthSec Maturity Score Calculator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Mode Aesthetic (Black/Red/White)
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stApp {
        background-color: #0E1117;
    }
    h1, h2, h3 {
        color: #FF4B4B;
        font-weight: 700;
    }
    .score-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #FF4B4B;
        text-align: center;
        margin: 20px 0;
    }
    .score-number {
        font-size: 72px;
        font-weight: 900;
        color: #FF4B4B;
        margin: 10px 0;
    }
    .score-label {
        font-size: 24px;
        color: #FFFFFF;
        font-weight: 600;
    }
    .recommendation-box {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin: 20px 0;
    }
    .risk-item {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #FF6B35;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)


# Load Question Packs
@st.cache_data
def load_question_packs():
    """Load all YAML question packs from the question_packs directory"""
    packs = {}
    pack_dir = Path("question_packs")
    
    if not pack_dir.exists():
        st.error("Question packs directory not found!")
        return packs
    
    for yaml_file in pack_dir.glob("*.yaml"):
        try:
            with open(yaml_file, 'r') as f:
                pack_data = yaml.safe_load(f)
                packs[yaml_file.stem] = pack_data
        except Exception as e:
            st.error(f"Error loading {yaml_file.name}: {e}")
    
    return packs


def calculate_weighted_score(responses, pack_data):
    """Calculate weighted score and identify top risks"""
    total_weight = 0
    earned_weight = 0
    top_risks = []
    domain_scores = {}
    domain_weights = {}
    
    # Check if this is a Trust Stack framework pack
    is_trust_stack = pack_data.get('trust_stack_framework', False)
    
    for domain in pack_data['domains']:
        domain_name = domain['name']
        domain_scores[domain_name] = 0
        domain_weights[domain_name] = 0
        
        for question in domain['questions']:
            q_id = question['id']
            weight = question['weight']
            response = responses.get(q_id, 'unanswered')
            
            if response != 'n/a':  # Only count if not N/A
                domain_weights[domain_name] += weight
                total_weight += weight
                
                if response == 'yes':
                    domain_scores[domain_name] += weight
                    earned_weight += weight
                elif response == 'no':
                    # Track this as a risk
                    top_risks.append({
                        'question': question['text'],
                        'domain': domain_name,
                        'trust_stack': question.get('trust_stack', domain_name),
                        'weight': weight,
                        'risk_level': question.get('risk_if_no', 'MEDIUM'),
                        'recommendation': question.get('recommendation', 'Address this control gap'),
                        'compliance_refs': question.get('compliance_refs', {})
                    })
    
    # Calculate percentage score
    score = (earned_weight / total_weight * 100) if total_weight > 0 else 0
    
    # Calculate domain percentages
    domain_percentages = {}
    for domain_name in domain_scores:
        if domain_weights[domain_name] > 0:
            domain_percentages[domain_name] = (domain_scores[domain_name] / domain_weights[domain_name]) * 100
        else:
            domain_percentages[domain_name] = 0
    
    # Sort risks by weight and risk level
    risk_priority = {'CRITICAL': 3, 'HIGH': 2, 'MEDIUM': 1, 'LOW': 0}
    top_risks.sort(key=lambda x: (risk_priority.get(x['risk_level'], 0), x['weight']), reverse=True)
    
    return score, domain_percentages, top_risks[:10], earned_weight, total_weight, is_trust_stack


def generate_markdown_report(pack_name, pack_data, responses, score, domain_percentages, top_risks):
    """Generate a downloadable Markdown report"""
    report = f"""# HealthSec Maturity Assessment Report

**Assessment Date:** {datetime.now().strftime('%B %d, %Y')}  
**Assessment Type:** {pack_data['name']}  
**Version:** {pack_data['version']}

---

## Executive Summary

### Overall Maturity Score: {score:.1f}/100

"""
    
    # Risk Level
    if score < 50:
        risk_level = "**CRITICAL RISK** 🔴"
        summary = "Your organization is at significant risk of data breaches, ransomware attacks, and regulatory non-compliance. Immediate action is required."
    elif score < 70:
        risk_level = "**HIGH RISK** 🟠"
        summary = "Your security posture has gaps that could lead to compliance violations or security incidents. Priority improvements needed."
    elif score < 85:
        risk_level = "**MODERATE RISK** 🟡"
        summary = "Your organization demonstrates good security practices with room for improvement in key areas."
    else:
        risk_level = "**ROBUST POSTURE** 🟢"
        summary = "Your organization demonstrates strong cybersecurity maturity and is well-positioned to maintain compliance."
    
    report += f"**Risk Level:** {risk_level}\n\n{summary}\n\n"
    
    # Domain Breakdown
    report += "## Domain Breakdown\n\n"
    for domain, percentage in domain_percentages.items():
        bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
        report += f"- **{domain}:** {percentage:.1f}% [{bar}]\n"
    
    # Top Risks
    report += f"\n## Top {len(top_risks)} Priority Risks\n\n"
    for i, risk in enumerate(top_risks, 1):
        report += f"### {i}. {risk['risk_level']} Risk - {risk['domain']}\n\n"
        report += f"**Control Gap:** {risk['question']}\n\n"
        report += f"**Recommendation:** {risk['recommendation']}\n\n"
        
        if risk['compliance_refs']:
            report += "**Compliance References:**\n"
            for framework, refs in risk['compliance_refs'].items():
                report += f"- {framework.upper()}: {', '.join(refs)}\n"
        report += "\n---\n\n"
    
    # Recommendations
    report += "## Recommended Action Plan\n\n"
    report += "### Immediate (30 Days)\n"
    critical_risks = [r for r in top_risks if r['risk_level'] == 'CRITICAL']
    if critical_risks:
        for risk in critical_risks[:3]:
            report += f"- [ ] {risk['recommendation']}\n"
    else:
        report += "- No critical gaps identified\n"
    
    report += "\n### Short-term (60 Days)\n"
    high_risks = [r for r in top_risks if r['risk_level'] == 'HIGH']
    if high_risks:
        for risk in high_risks[:3]:
            report += f"- [ ] {risk['recommendation']}\n"
    else:
        report += "- Continue monitoring current controls\n"
    
    report += "\n### Long-term (90+ Days)\n"
    report += "- Conduct follow-up assessment to measure improvement\n"
    report += "- Review and update security policies\n"
    report += "- Schedule security awareness training\n"
    report += "- Implement continuous compliance monitoring\n"
    
    report += "\n---\n\n"
    report += "*Report generated by HealthSec Maturity Score Calculator*  \n"
    report += "*Open Source Project by HealthSec Alliance*\n"
    
    return report


# Header
st.markdown("<h1 style='text-align: center;'>🏥 HealthSec Maturity Score Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #CCCCCC;'>Quantify Your Cybersecurity Risk & Compliance Posture</p>", unsafe_allow_html=True)
st.markdown("---")

# Load question packs
question_packs = load_question_packs()

if not question_packs:
    st.error("No question packs found! Please ensure YAML files exist in the question_packs directory.")
    st.stop()

# Sidebar - Pack Selection
st.sidebar.title("📋 Assessment Configuration")

pack_names = {key: data['name'] for key, data in question_packs.items()}
selected_pack_key = st.sidebar.selectbox(
    "Select Assessment Type:",
    options=list(pack_names.keys()),
    format_func=lambda x: pack_names[x]
)

selected_pack = question_packs[selected_pack_key]

st.sidebar.markdown(f"**Description:** {selected_pack['description']}")
st.sidebar.markdown("---")

# Question Collection
st.sidebar.markdown("### Answer the following questions:")
st.sidebar.markdown("*Use N/A if the question doesn't apply to your organization*")

responses = {}

for domain in selected_pack['domains']:
    st.sidebar.markdown(f"### {domain['name']}")
    
    for question in domain['questions']:
        q_id = question['id']
        q_text = question['text']
        weight = question.get('weight', 5)
        
        # Use radio buttons for 3-state answers (default to N/A for optional questions)
        response = st.sidebar.radio(
            f"{q_text}",
            options=['n/a', 'yes', 'no'],
            format_func=lambda x: {'yes': '✅ Yes', 'no': '❌ No', 'n/a': '⊘ N/A (Optional)'}[x],
            key=q_id,
            index=0,  # Default to N/A
            horizontal=False
        )
        
        responses[q_id] = response
        
    st.sidebar.markdown("---")

# Calculate scores
score, domain_percentages, top_risks, earned_weight, total_weight, is_trust_stack = calculate_weighted_score(responses, selected_pack)

# Determine Risk Level
if score < 50:
    risk_level = "CRITICAL RISK"
    risk_color = "#FF0000"
elif score < 70:
    risk_level = "HIGH RISK"
    risk_color = "#FF6B35"
elif score < 85:
    risk_level = "MODERATE RISK"
    risk_color = "#FFB84D"
else:
    risk_level = "ROBUST POSTURE"
    risk_color = "#4CAF50"

# Count answered questions (excluding N/A)
applicable_questions = sum(1 for r in responses.values() if r != 'n/a')
answered_questions = sum(1 for r in responses.values() if r in ['yes', 'no'])
total_questions = len([q for d in selected_pack['domains'] for q in d['questions']])

# Main Content Area
if applicable_questions > 0:
    st.info(f"📊 **{applicable_questions}** questions are applicable to your organization | **{total_questions - applicable_questions}** marked as N/A")

col1, col2 = st.columns([1, 1])

with col1:
    # Score Card
    st.markdown(f"""
        <div class="score-card">
            <div class="score-label">YOUR HEALTHSEC MATURITY SCORE</div>
            <div class="score-number">{score:.1f}/100</div>
            <div style="font-size: 28px; color: {risk_color}; font-weight: 700; margin-top: 10px;">
                {risk_level}
            </div>
            <div style="font-size: 14px; color: #888888; margin-top: 15px;">
                Weighted Score: {earned_weight:.0f}/{total_weight:.0f} points
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Domain Breakdown
    st.markdown("### 📊 Domain Breakdown")
    for domain_name, percentage in domain_percentages.items():
        st.markdown(f"**{domain_name}:** {percentage:.1f}%")
        st.progress(percentage / 100)

with col2:
    # Radar Chart
    if is_trust_stack:
        st.markdown("### 🎯 Trust Stack Framework")
    else:
        st.markdown("### 🎯 Security Posture Radar")
    
    categories = list(domain_percentages.keys())
    values = list(domain_percentages.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(255, 75, 75, 0.3)',
        line=dict(color='#FF4B4B', width=2),
        name='Your Score'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='#1a1a1a',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#444444',
                tickfont=dict(color='#FFFFFF')
            ),
            angularaxis=dict(
                gridcolor='#444444',
                tickfont=dict(color='#FFFFFF', size=12)
            )
        ),
        showlegend=False,
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font=dict(color='#FFFFFF'),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Top Risks Section
st.markdown("---")
st.markdown("## 🚨 Top Priority Risks")

if not top_risks:
    st.success("✅ Excellent! No control gaps identified in your current responses.")
else:
    st.markdown(f"*Showing top {min(5, len(top_risks))} risks based on weight and severity*")
    
    for i, risk in enumerate(top_risks[:5], 1):
        risk_emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}
        
        st.markdown(f"""
            <div class="risk-item">
                <h4>{risk_emoji.get(risk['risk_level'], '⚪')} {i}. {risk['risk_level']} - {risk['domain']}</h4>
                <p style="font-size: 14px; color: #CCCCCC;"><strong>Control Gap:</strong> {risk['question']}</p>
                <p style="font-size: 14px; color: #CCCCCC;"><strong>Recommendation:</strong> {risk['recommendation']}</p>
            </div>
        """, unsafe_allow_html=True)

# Recommendations Section
st.markdown("---")
st.markdown("## 💡 Recommendations & Next Steps")

if score < 50:
    st.markdown(f"""
        <div class="recommendation-box">
            <h3 style="color: #FF4B4B;">⚠️ CRITICAL VULNERABILITY DETECTED</h3>
            <p style="font-size: 16px; line-height: 1.6;">
                Your organization is at <strong>significant risk</strong> of data breaches, ransomware attacks, and 
                regulatory non-compliance. Immediate action is required.
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                <strong>Recommended Actions:</strong>
            </p>
            <ul style="font-size: 15px; line-height: 1.8;">
                <li>Address all CRITICAL risks in the next 30 days</li>
                <li>Deploy <strong>Zero Trust Architecture</strong> immediately for OT devices</li>
                <li>Implement an <strong>immutable audit ledger</strong> for data integrity</li>
                <li>Conduct a <strong>comprehensive HIPAA/FDA compliance audit</strong></li>
                <li>Contact the <strong>HealthSec Alliance</strong> for emergency remediation</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
elif score < 70:
    st.markdown(f"""
        <div class="recommendation-box">
            <h3 style="color: #FF6B35;">⚡ HIGH RISK - Improvements Needed</h3>
            <p style="font-size: 16px; line-height: 1.6;">
                Your security posture has gaps that could lead to compliance violations or security incidents.
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                <strong>Priority Focus Areas:</strong>
            </p>
            <ul style="font-size: 15px; line-height: 1.8;">
                <li>Address CRITICAL and HIGH priority risks within 60 days</li>
                <li>Schedule a security posture review with the HealthSec Alliance</li>
                <li>Implement missing controls from your weakest domains</li>
                <li>Consider a comprehensive penetration test</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
elif score < 85:
    st.markdown(f"""
        <div class="recommendation-box">
            <h3 style="color: #FFB84D;">📈 MODERATE RISK - Continue Improving</h3>
            <p style="font-size: 16px; line-height: 1.6;">
                Your organization demonstrates good security practices. Focus on closing remaining gaps.
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                <strong>Next Steps:</strong>
            </p>
            <ul style="font-size: 15px; line-height: 1.8;">
                <li>Address remaining HIGH priority risks</li>
                <li>Strengthen domains scoring below 70%</li>
                <li>Implement continuous monitoring and improvement</li>
                <li>Consider advanced security capabilities (SOAR, EDR, etc.)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div class="recommendation-box">
            <h3 style="color: #4CAF50;">✅ ROBUST SECURITY POSTURE</h3>
            <p style="font-size: 16px; line-height: 1.6;">
                Congratulations! Your organization demonstrates strong cybersecurity maturity. You are well-positioned 
                to maintain compliance and protect patient data.
            </p>
            <p style="font-size: 16px; line-height: 1.6;">
                <strong>Next Steps:</strong>
            </p>
            <ul style="font-size: 15px; line-height: 1.8;">
                <li>Continue monitoring and improving your security controls</li>
                <li>Consider joining the <strong>HealthSec Alliance</strong> as a trusted partner</li>
                <li>Share your best practices with the healthcare community</li>
                <li>Stay updated on emerging threats and AI governance frameworks</li>
                <li>Conduct regular re-assessments (quarterly recommended)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Download Report
st.markdown("---")
st.markdown("## 📥 Download Your Assessment Report")

# Report available if at least some questions answered (not just all N/A)
if answered_questions > 0:
    report_md = generate_markdown_report(
        selected_pack_key,
        selected_pack,
        responses,
        score,
        domain_percentages,
        top_risks
    )
    
    st.download_button(
        label="📄 Download Markdown Report",
        data=report_md,
        file_name=f"healthsec_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )
    
    st.info("💡 **Tip:** This report can be used for board presentations, compliance documentation, and remediation planning.")
else:
    st.warning("⚠️ Answer at least one applicable question (Yes/No) to download your assessment report.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #888888; padding: 20px;'>
        <p><strong>HealthSec Alliance</strong> | Securing the Future of Healthcare Data</p>
        <p>Contact us at <a href='mailto:info@healthsecalliance.com' style='color: #FF4B4B;'>info@healthsecalliance.com</a> | Visit our website at <a href='https://healthsecalliance.com' style='color: #FF4B4B;'>healthsecalliance.com</a></p>
        <p style='font-size: 12px; margin-top: 10px;'>v2.0.0 | MIT License</p>
    </div>
""", unsafe_allow_html=True)
