#!/usr/bin/env python3
"""Extract key financial metrics from Brazilian B2B SaaS Excel files."""

import pandas as pd
import numpy as np
import sys
import json

def find_date_columns(df, year='2025'):
    """Find columns containing year data (format: YYYYMM)."""
    cols = []
    for i, val in enumerate(df.iloc[3, :].tolist()):
        try:
            if str(val).startswith(year):
                cols.append(i)
        except:
            pass
    return cols

def extract_ytd_value(df, row_idx, col_indices):
    """Sum values across columns for YTD."""
    values = df.iloc[row_idx, col_indices].values
    return np.nansum([v for v in values if pd.notna(v) and isinstance(v, (int, float))])

def find_row_by_text(df, search_text, col=3):
    """Find row index containing search text."""
    for i in range(df.shape[0]):
        val = df.iloc[i, col]
        if pd.notna(val) and search_text.upper() in str(val).upper():
            return i
    return None

def extract_financials(filepath, year='2025'):
    """Extract key financial metrics from Excel file."""
    xlsx = pd.ExcelFile(filepath)
    
    # Load main financials sheet
    sheet_name = None
    for name in xlsx.sheet_names:
        if 'financials_mensal' in name.lower() or 'financials' in name.lower():
            sheet_name = name
            break
    
    if not sheet_name:
        sheet_name = xlsx.sheet_names[0]
    
    df = pd.read_excel(xlsx, sheet_name=sheet_name, header=None)
    cols = find_date_columns(df, year)
    
    if not cols:
        return {"error": f"No {year} columns found"}
    
    # Find key rows
    metrics = {
        'revenue_row': find_row_by_text(df, 'RECEITA BRUTA'),
        'recurring_row': find_row_by_text(df, 'RECORRENTE'),
        'deductions_row': find_row_by_text(df, 'DEDUÇÕES'),
        'personnel_cogs_row': find_row_by_text(df, 'C | TRABALHISTAS') or find_row_by_text(df, 'TRABALHISTA'),
        'general_cogs_row': find_row_by_text(df, 'C | GERAIS'),
        'personnel_opex_row': find_row_by_text(df, 'D | TRABALHISTAS'),
        'commercial_row': find_row_by_text(df, 'D | COMERCIAIS') or find_row_by_text(df, 'COMERCIAIS'),
        'ga_row': find_row_by_text(df, 'D | GERAIS E ADMINISTRATIVAS') or find_row_by_text(df, 'G&A'),
        'ebitda_row': find_row_by_text(df, 'EBITDA'),
    }
    
    # Extract YTD values
    months_ytd = len(cols)
    results = {
        'months_ytd': months_ytd,
        'annualization_factor': 12 / months_ytd,
    }
    
    for key, row in metrics.items():
        if row is not None:
            ytd = extract_ytd_value(df, row, cols)
            results[key.replace('_row', '_ytd')] = ytd
            results[key.replace('_row', '_annual')] = ytd * (12 / months_ytd)
    
    # Try to get KPIs from KPI sheet
    for kpi_sheet in ['KPI_Real', 'KPIs']:
        if kpi_sheet in xlsx.sheet_names:
            df_kpi = pd.read_excel(xlsx, sheet_name=kpi_sheet, header=None)
            kpi_cols = find_date_columns(df_kpi, year)
            if kpi_cols:
                latest_col = kpi_cols[-1]
                
                # Find customer count
                for i in range(df_kpi.shape[0]):
                    val = df_kpi.iloc[i, 2] if df_kpi.shape[1] > 2 else None
                    if pd.notna(val) and 'TOTAL CLIENTES' in str(val).upper():
                        results['customers'] = df_kpi.iloc[i, latest_col]
                    elif pd.notna(val) and val == 'ARPU':
                        results['arpu'] = df_kpi.iloc[i, latest_col]
                    elif pd.notna(val) and 'CHURN' in str(val).upper() and '%' in str(val):
                        results['churn_rate'] = df_kpi.iloc[i, latest_col]
                    elif pd.notna(val) and 'MRR' == str(val).strip():
                        results['mrr'] = df_kpi.iloc[i, latest_col]
                
                # Find headcount
                for i in range(df_kpi.shape[0]):
                    val = df_kpi.iloc[i, 2] if df_kpi.shape[1] > 2 else None
                    if pd.notna(val) and ('TOTAL HC' in str(val).upper() or val == 'HC'):
                        hc = df_kpi.iloc[i, latest_col]
                        if pd.notna(hc) and hc > 0:
                            results['headcount'] = int(hc)
            break
    
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_financials.py <excel_file> [year]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    year = sys.argv[2] if len(sys.argv) > 2 else '2025'
    
    results = extract_financials(filepath, year)
    print(json.dumps(results, indent=2, default=str))
