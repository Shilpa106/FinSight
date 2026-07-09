from enum import Enum


class DocumentType(str, Enum):
    UNKNOWN = "unknown"
    ANNUAL_REPORT = "annual_report"
    LOAN_AGREEMENT = "loan_agreement"
    FUND_REPORT = "fund_report"
    INVESTMENT_MEMO = "investment_memo"
    COMPLIANCE_DOCUMENT = "compliance_document"
    KYC_DOCUMENT = "kyc_document"