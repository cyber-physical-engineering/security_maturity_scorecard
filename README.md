# 🏥 HealthSec Maturity Score Calculator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io)

An open-source cybersecurity maturity assessment tool designed specifically for healthcare organizations, life sciences companies, and the broader health ecosystem.

**Developed by Big Data Plumbing (https://github.com/bigdataplumbing) to help organizations assess their security posture against critical healthcare compliance frameworks.

---

## 🎯 Purpose

The HealthSec Maturity Score Calculator helps Hospital CIOs, IT Directors, and OT Managers evaluate their organization's cybersecurity posture across three critical domains:

- **Device Security**: OT devices, firmware integrity, MFA, and device tracking
- **Data Integrity**: Encryption, audit logging, backup strategies
- **AI Governance**: Human oversight, model drift monitoring, FDA/HIPAA compliance

## ⚡ Features

### Core Capabilities
- ✅ **Multiple Question Packs**: Choose from Quick (10Q), Standard (20Q), or HIPAA Focus (15Q)
- 📊 **Weighted Scoring System**: Questions weighted by impact (1-10 points)
- 📈 **Visual Analytics**: Interactive radar chart showing strengths across domains
- 🎯 **Top Risks Dashboard**: Automatically identifies and prioritizes your biggest gaps
- 💡 **Actionable Recommendations**: Specific remediation steps for each control gap
- 📥 **Downloadable Reports**: Generate Markdown reports for board presentations
- 🎨 **Dark Mode Interface**: Professional black/red/white aesthetic
- 🌐 **Browser-Based**: No installation required for end users
- 🔓 **100% Open Source**: Free to use, modify, and contribute

### Advanced Features (v2.0+)
- **3-State Answers**: Yes/No/N/A support with smart scoring
- **Compliance Mapping**: Built-in references to HIPAA, NIST CSF, FDA, GxP
- **Plugin Architecture**: Add custom question packs via YAML (no coding required)
- **Risk Prioritization**: CRITICAL/HIGH/MEDIUM/LOW classification
- **Extensible Framework**: Ready for benchmarking and historical tracking

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone this repository:**

```bash
git clone https://github.com/bigdataplumbing/healthsec-maturity-scorecard.git
cd healthsec-maturity-scorecard
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run maturity_app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

---

## 📊 How It Works

### Scoring System

- Each "Yes" answer = 10 points
- Total Score = Sum of all answers (0-100)
- Domain Scores = Calculated separately for each category

### Risk Levels

| Score Range | Risk Level | Interpretation |
|-------------|------------|----------------|
| 0-49 | **CRITICAL RISK** | Immediate remediation required |
| 50-69 | **HIGH RISK** | Significant improvements needed |
| 70-84 | **MODERATE RISK** | Good posture with room for improvement |
| 85-100 | **ROBUST POSTURE** | Strong security maturity |

---

## 🏗️ Technical Architecture

- **Frontend**: Streamlit (Python web framework)
- **Data Handling**: Pandas
- **Visualization**: Plotly (interactive radar charts)
- **Deployment**: Can be deployed to Streamlit Cloud, AWS, Azure, or on-premises

---

## 🎨 Customization

### Adding Questions

Edit the `questions` dictionary in `maturity_app.py`:

```python
questions = {
    "Your Domain": [
        "Your question here?",
        "Another question?"
    ]
}
```

### Adjusting Scoring Weights

Modify the scoring logic to weight certain domains more heavily:

```python
# Example: Double weight for Data Integrity
if "Data Integrity" in domain:
    domain_score += 20  # Instead of 10
```

### Changing Colors

Update the CSS section at the top of `maturity_app.py` to match your brand:

```python
st.markdown("""
    <style>
    h1, h2, h3 {
        color: #YOUR_COLOR;  # Change primary color
    }
    </style>
""", unsafe_allow_html=True)
```

---

## 🔒 Compliance & Standards

This tool is designed to align with:

- **HIPAA** (Health Insurance Portability and Accountability Act)
- **GxP** (Good Practice Quality Guidelines)
- **FDA** Cybersecurity Guidelines for Medical Devices
- **NIST Cybersecurity Framework**
- **Zero Trust Architecture** principles

---

## 📈 Use Cases

1. **Self-Assessment**: Organizations can evaluate their current security posture
2. **Gap Analysis**: Identify specific areas needing improvement
3. **Board Reporting**: Generate visual reports for executive stakeholders
4. **Vendor Assessment**: Evaluate security maturity of healthcare partners
5. **Sales Tool**: Demonstrate the value of security solutions to prospects
6. **Compliance Prep**: Prepare for HIPAA, FDA, and GxP audits

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Contribution Ideas

- Add more questions for deeper assessments
- Create different questionnaire versions (quick, standard, comprehensive)
- Add export functionality (PDF reports)
- Implement multi-language support
- Create benchmarking features
- Add historical tracking

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 About HealthSec Alliance

The HealthSec Alliance is dedicated to securing healthcare data, ensuring trust in AI systems, and maintaining compliance across the health ecosystem. We provide open-source tools, frameworks, and education to help organizations protect patient data and maintain regulatory compliance.

**GitHub Organization**: [bigdataplumbing](https://github.com/bigdataplumbing)

---

## 📞 Support & Contact

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/bigdataplumbing/healthsec-maturity-scorecard/issues)
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/bigdataplumbing/healthsec-maturity-scorecard/discussions)
- **Email**: info@healthsecalliance.com

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Visualization powered by [Plotly](https://plotly.com)
- Inspired by healthcare security frameworks from NIST, FDA, and HIPAA

---

**Star ⭐ this repo if you find it helpful!**

**Version**: 2.0.0  
**Last Updated**: December 30, 2025

