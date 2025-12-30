# Quick Start Guide - HealthSec Maturity Score Calculator v2.0

## 🚀 Running the Application

The application is **currently running** at:
- **Local**: http://localhost:8501

To restart the server in the future:
```bash
cd "/Users/James/Desktop/HealthSec/HealthSec Maturity Scorecard/healthsec_maturity_scorecard"
streamlit run maturity_app.py
```

## 🎯 New Features (v2.0)

### 1. Question Pack Selector
- Choose from 3 pre-built assessments:
  - **Quick Assessment** (10 questions) - 5-minute evaluation
  - **Standard Assessment** (20 questions) - Comprehensive review
  - **HIPAA Compliance Focus** (15 questions) - Regulatory-focused

### 2. Smart Answer System
- **Yes** ✅ - Control is implemented (full points)
- **No** ❌ - Gap identified (added to Top Risks)
- **N/A** ⊘ - Question doesn't apply (excluded from score)
- **Not Answered** ⚪ - Default state

### 3. Weighted Scoring
- Questions worth 1-10 points based on impact
- Score reflects real-world risk priorities
- Shows both percentage (0-100) and weighted points

### 4. Top Risks Dashboard
- Automatically identifies your biggest gaps
- Prioritized by CRITICAL > HIGH > MEDIUM > LOW
- Includes specific recommendations for each gap
- Maps to compliance frameworks (HIPAA, FDA, NIST, GxP)

### 5. Downloadable Reports
- Click "Download Markdown Report" at the bottom
- Includes executive summary, risks, and action plan
- Ready for board presentations or compliance docs

## 📝 For CISOs & Consultants

### Adding Custom Question Packs
1. Create a new YAML file in `question_packs/`
2. Follow the structure from existing packs
3. No Python coding required!
4. Example structure:

```yaml
name: "Your Custom Assessment"
description: "Description here"
version: "1.0"
domains:
  - name: "Security Domain"
    questions:
      - id: "custom_01"
        text: "Your question here?"
        weight: 8
        risk_if_no: "HIGH"
        recommendation: "What to do if answer is No"
        compliance_refs:
          hipaa: ["164.308(a)(1)"]
          nist_csf: ["PR.AC-1"]
```

### Customizing Weights
- Edit the `weight` field (1-10) in any question
- Higher weight = more impact on final score
- Rebalance domains as needed for your industry

### Use Cases
- **Self-Assessment**: Internal security posture evaluation
- **Vendor Risk**: Due diligence questionnaires
- **Compliance Prep**: Pre-audit readiness checks
- **Gap Analysis**: Identify specific control weaknesses
- **Progress Tracking**: Re-run quarterly to measure improvement

## 🔧 Technical Details

### Dependencies
- Python 3.8+
- streamlit==1.29.0
- pandas==2.1.4
- plotly==5.18.0
- pyyaml==6.0.1

### File Structure
```
healthsec_maturity_scorecard/
├── maturity_app.py          # Main application
├── requirements.txt         # Python dependencies
├── README.md               # Full documentation
├── LICENSE                 # MIT license
├── .gitignore             # Git exclusions
├── UPGRADE_NOTES.md       # Version 2.0 changes
├── QUICKSTART.md          # This file
└── question_packs/        # Assessment definitions
    ├── quick_10.yaml
    ├── standard_20.yaml
    └── hipaa_15.yaml
```

### Deployment Options
- **Local**: Already running on your machine
- **Streamlit Cloud**: Free hosting, one-click deploy
- **AWS/Azure**: Docker container or EC2/App Service
- **On-Premises**: Behind corporate firewall

## 📊 Sample Workflow

1. **Select Assessment Type** - Choose pack in sidebar
2. **Answer Questions** - Use radio buttons for Yes/No/N/A
3. **Review Score** - Watch real-time updates to maturity score
4. **Analyze Risks** - Review Top Priority Risks section
5. **Download Report** - Generate Markdown for documentation
6. **Take Action** - Follow 30/60/90-day remediation plan
7. **Re-Assess** - Run quarterly to track improvement

## 🤝 Contributing

This is an **open source project** - contributions welcome!

### Ways to Contribute:
1. **Add Question Packs** - Create industry-specific assessments
2. **Improve Recommendations** - Enhance remediation guidance
3. **Add Compliance Refs** - Map to additional frameworks
4. **Fix Bugs** - Report issues on GitHub
5. **Documentation** - Improve guides and examples

### Submitting Question Packs:
1. Fork the repository
2. Add your YAML file to `question_packs/`
3. Test locally with `streamlit run maturity_app.py`
4. Submit pull request with description
5. Maintainers will review and merge

## 📞 Support

- **GitHub Issues**: Report bugs or request features
- **Email**: info@healthsecalliance.com
- **Documentation**: See README.md for full details

## 📄 License

MIT License - Free for commercial and personal use

---

**Built with ❤️ by the HealthSec Alliance**  
Securing the Future of Healthcare Data

**Version**: 2.0.0 | **Date**: December 30, 2025

