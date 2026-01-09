# Excel Model Structure Reference

## Sheet 1: Executive Summary

### Company Overview Table (Rows 6-16)
| Row | Metric | Cell B | Format |
|-----|--------|--------|--------|
| 7 | Annual Revenue | Input (blue) | #,##0 |
| 8 | Recurring Revenue % | Input | 0.0% |
| 9 | EBITDA | Input | #,##0 |
| 10 | EBITDA Margin | =B9/B7 | 0.0% |
| 11 | Total Employees | Input | #,##0 |
| 12 | Customers | Input | #,##0 |
| 13 | Monthly ARPU | Input | #,##0 |
| 14 | ARR | Input | #,##0 |
| 15 | Churn Rate | Input | 0.0% |

### Cost Structure Table (Rows 20-26)
| Cost Category | Annual (R$) | % of Revenue | AI Opportunity |
|--------------|-------------|--------------|----------------|
| Personnel - COGS | Input | =B/Revenue | Text |
| General COGS | Input | =B/Revenue | Text |
| Personnel - OpEx | Input | =B/Revenue | Text |
| Commercial | Input | =B/Revenue | Text |
| G&A | Input | =B/Revenue | Text |

### Scenario Summary Table (Rows 30-36)
Links to Scenarios sheet calculations:
- Annual Savings: =Scenarios!B21, =Scenarios!B39, =Scenarios!B57
- Implementation Cost: =Scenarios!B22, =Scenarios!B40, =Scenarios!B58
- Net Year 1 Impact: =Scenarios!B23, =Scenarios!B41, =Scenarios!B59
- Payback (months): =Scenarios!B24, =Scenarios!B42, =Scenarios!B60
- 3-Year NPV: =Scenarios!B27, =Scenarios!B45, =Scenarios!B63
- New EBITDA Margin: =Scenarios!B26, =Scenarios!B44, =Scenarios!B62

## Sheet 2: Scenarios

### Assumptions Section (Rows 5-9)
- B5: Base Annual Revenue (input, blue)
- B6: Current EBITDA (input, blue)
- B7: =B6/B5 (Current EBITDA Margin)
- B8: Discount Rate (input, default 0.12)
- B9: Analysis Period (input, default 3)

### Scenario Table Structure (repeat for each scenario)
| Col A | Col B | Col C | Col D | Col E |
|-------|-------|-------|-------|-------|
| Category | Current Cost | Reduction % | Savings | Impl Cost |
| Customer Support | Input | Input % | =B×C | Input |
| Sales Process | Input | Input % | =B×C | Input |
| Marketing | Input | Input % | =B×C | Input |
| Finance/Admin | Input | Input % | =B×C | Input |
| Infrastructure | Input | Input % | =B×C | Input |
| **TOTAL** | | | =SUM(D) | =SUM(E) |

### KPI Calculations (after each scenario table)
```
Annual Savings      = =D_TOTAL
Implementation Cost = =E_TOTAL  
Net Year 1 Impact   = =Savings - Impl_Cost
Payback (months)    = =IF(Savings>0, Impl_Cost/Savings*12, 0)
New EBITDA          = =B6 + Savings
New EBITDA Margin   = =(B6 + Savings) / B5
3-Year NPV          = =-Impl + Savings/(1+B8) + Savings/(1+B8)^2 + Savings/(1+B8)^3
```

## Sheet 3: Implementation Roadmap

### Phase Tables
| Initiative | Department | Expected Savings | Cost | Complexity |
|-----------|------------|------------------|------|------------|
| Text | Text | #,##0 | #,##0 | Low/Med/High |

### Phase Totals
- =SUM(Savings column)
- =SUM(Cost column)

### Grand Total Row
- Total Savings: =Phase1 + Phase2 + Phase3
- Total Costs: =Phase1 + Phase2 + Phase3
- Net Benefit: =Total_Savings - Total_Costs

## Sheet 4: AI Use Cases

| Use Case | Current Process | AI Solution | Tool/Platform | FTE Impact | Annual Savings |
|----------|----------------|-------------|---------------|------------|----------------|
| Text | Text | Text | Text | Number | #,##0 |

## Styling Standards

### Colors
- Blue font (0,0,255): All input values
- Black font: All formulas
- Header fill (2F5496): White bold text
- Light blue (D6E3F8): Conservative scenario
- Light green (C6EFCE): Moderate scenario  
- Light yellow (FFF2CC): Aggressive scenario

### Number Formats
- Currency: #,##0 (no decimals for R$)
- Percentages: 0.0%
- Payback: 0.0 (months)
- FTE: 0.0

### Column Widths
- A (labels): 30-35
- B (values): 16-18
- C (percentages): 12-14
- D (savings): 16
- E (implementation): 18-20
