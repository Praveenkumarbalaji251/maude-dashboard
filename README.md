# MAUDE Harm-Device-Manufacturer Dashboard

This project provides an interactive dashboard for analyzing FDA MAUDE adverse event data, focusing on patient harm, device brand, and manufacturer, month-wise.

## Features
- Month-wise filtering and analysis of harm-brand-manufacturer counts
- Interactive charts and tables for top harms and devices
- Full patient problem count visualization (scrollable)
- Built with Streamlit for easy local and cloud deployment

## Project Structure
```
WHYHOW.ai/
├── maude_dashboard_monthly.py         # Main Streamlit dashboard script
├── aggregate_harm_brand_manufacturer_all_months.py  # Script to generate monthly Excel files
├── aggregate_harm_brand_manufacturer_aug2024.py     # Script for August 2024 aggregation
├── harm_brand_manufacturer_aug_2024.xlsx            # Example monthly data file
├── harm_brand_manufacturer_sep_2024.xlsx            # ...other monthly data files
├── patient_problem_counts.xlsx                      # Patient problem counts (for second chart)
├── maude_AUG2024_JULY2025.csv                      # Raw MAUDE data (large file, not for cloud)
├── requirements.txt                                 # Python dependencies
└── README.md                                        # Project documentation
```

## Setup
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd WHYHOW.ai
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the dashboard locally:
   ```bash
   streamlit run maude_dashboard_monthly.py
   ```

## Deployment
To deploy on Streamlit Community Cloud:
- Push this code to a public GitHub repository.
- Ensure `maude_dashboard_monthly.py` and at least sample data files are present.
- Large files (like the raw CSV) may need to be hosted elsewhere or replaced with samples.
- Follow Streamlit Cloud instructions to deploy.

## Requirements
- Python 3.8+
- pandas
- streamlit
- altair

## Notes
- The file `maude_AUG2024_JULY2025.csv` is very large and is NOT tracked in git or hosted on GitHub. Keep it in your local project directory for full functionality.
- For full functionality, keep all monthly Excel files and `patient_problem_counts.xlsx` in the project root.
- The dashboard is designed for local analysis of large datasets; cloud deployment may require data size adjustments.

## License
MIT
