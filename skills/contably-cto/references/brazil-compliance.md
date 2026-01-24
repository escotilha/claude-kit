# Brazil Accounting Compliance Reference

## SPED (Sistema Público de Escrituração Digital)

The digital bookkeeping system collecting all financial, accounting, tax, and labor information.

### SPED Modules

| Module | Purpose | Frequency | Deadline |
|--------|---------|-----------|----------|
| **ECD** | Digital Accounting Bookkeeping | Annual | Last business day of May |
| **ECF** | Fiscal Bookkeeping (IRPJ/CSLL) | Annual | Last business day of July |
| **EFD-ICMS/IPI** | State tax records | Monthly | Varies by state |
| **EFD-Contribuições** | PIS/COFINS records | Monthly | 10th business day |
| **EFD-Reinf** | Withholding taxes | Monthly | 15th of following month |

### Electronic Invoice Types

| Type | Scope | Authority | Format |
|------|-------|-----------|--------|
| **NF-e** | Goods/products | State (SEFAZ) | XML with digital signature |
| **NFS-e** | Services | Municipal (3,500+ cities) | XML, varies by municipality |
| **CT-e** | Cargo transport | State | XML |
| **NFC-e** | Consumer sales | State | XML |
| **MDF-e** | Transport manifest | State | XML |
| **NFCom** | Telecom (new Nov 2025) | National | XML |

### Integration Architecture Implications

1. **State-level APIs**: Each of 27 states has SEFAZ with different endpoints
2. **Municipal fragmentation**: NFS-e requires integration with thousands of municipal systems
3. **Digital certificates**: A1/A3 certificates required for all document signing
4. **5-year retention**: All XML documents must be stored with audit trail

## eSocial

Unified labor and payroll reporting system.

### Key Events

| Event Code | Description | Timing |
|------------|-------------|--------|
| S-1000 | Employer info | Initial + changes |
| S-1200 | Payroll | Monthly |
| S-1210 | Payment info | Monthly |
| S-2200 | Employee admission | Before start date |
| S-2299 | Termination | Up to 10 days after |
| S-2230 | Leave/absence | Per occurrence |

### Architecture Requirements

- Real-time event submission capability
- Government certificate authentication
- Event sequencing and dependency management
- Rollback/correction workflows (S-3000 series)

## Tax Rates Quick Reference

### Federal Taxes (on revenue)
- **PIS**: 1.65% (non-cumulative) or 0.65% (cumulative)
- **COFINS**: 7.6% (non-cumulative) or 3% (cumulative)
- **IRPJ**: 15% + 10% surtax on profits > R$20k/month
- **CSLL**: 9%

### State Tax
- **ICMS**: 7-25% depending on state and product

### Municipal Tax
- **ISS**: 2-5% on services

### Payroll Contributions
- **INSS (employer)**: 20% + RAT (1-3%)
- **FGTS**: 8%
- **System S**: ~5.8% (varies by sector)

## 2026 Tax Reform (Constitutional Amendment 132/2023)

### New Taxes Replacing Current System

| Old Taxes | New Tax | Rate (estimated) |
|-----------|---------|------------------|
| ICMS, ISS | IBS (state/municipal) | ~17.7% |
| PIS, COFINS, IPI | CBS (federal) | ~8.8% |

### Transition Timeline
- 2026-2027: Testing phase, parallel systems
- 2027-2032: Gradual transition
- 2033: Full implementation

### Architecture Implications
- Must support dual tax calculation engines
- Destination-based taxation (vs current origin-based for ICMS)
- Unified national invoice format expected

## Simples Nacional

Simplified tax regime for small businesses (up to R$4.8M annual revenue).

### DAS (Single Payment Document)
- Monthly unified payment
- Rates: 4% to 33% depending on activity and revenue tier
- Reported via PGDAS-D monthly

### Integration Needs
- Simples calculation engine
- DAS generation
- PGDAS-D submission

## Key Deadlines Calendar

| Obligation | Deadline |
|------------|----------|
| eSocial events | Varies by event type |
| DCTFWeb | 15th of following month |
| EFD-Contribuições | 10th business day |
| EFD-ICMS/IPI | Varies by state |
| DIRF | February (annual) |
| RAIS | March (annual) |
| ECD | May (annual) |
| ECF | July (annual) |

## API Integration Points

### SEFAZ Web Services
- **Production**: `https://nfe.sefaz[UF].gov.br/`
- **Homologation**: Separate endpoints per state
- **Operations**: Authorization, cancellation, event registration, status query

### Banking (Open Finance Brazil)
- Account info APIs
- Payment initiation
- PIX instant payments

### RFB (Federal Revenue)
- e-CAC portal authentication
- Certificate-based services
