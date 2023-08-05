import datetime

import collections

from fec_dbsync.models import *


collections_journey_name_config = 'collectionsJourneyName'

db_entry_list = ['loan_account_number', 'acid', 'current_balance', 'lms_schm_code', 'cif_id', 'prin_dmd_os',
                 'int_dmd_os',
                 'past_due_flag', 'charge_off_flag', 'disb_date', 'Acct_status', 'payoff_date', 'pms_schm_id',
                 'pms_schm_desc',
                 'dpd_cntr', 'dpd_ason_date', 'inst_start_date', 'maturity_date', 'debt_group']

batch_size = 10000

MODELS_DICT = {
    GeneralAccount: {
        'table_name': 'custom.robo_gam_view',
        'row_dict': collections.OrderedDict([
            ('LOAN_ACCT_NUM', 'row[0]'),
            ('ACID', 'row[1]'),
            ('CURRENT_BAL', 'row[2]'),
            ('LMS_SCHM_CODE', 'row[3]'),
            ('CIF_ID', 'row[4]'),
            ('PRIN_DMD_OS', 'row[5]'),
            ('INT_DMD_OS', 'row[6]'),
            ('PAST_DUE_FLG', 'row[7]'),
            ('CHRGE_OFF_FLG', 'row[8]'),
            ('DISB_DATE', 'row[9]'),
            ('ACCT_STATUS', 'row[10]'),
            ('PAYOFF_DATE', 'row[11]'),
            ('PMS_SCHM_ID', 'row[12]'),
            ('PMS_SCHM_DESC', 'row[13]'),
            ('DPD_CNTR', 'row[14]'),
            ('DPD_ASON_DATE', 'row[15]'),
            ('INST_START_DATE', 'row[16]'),
            ('MATURITY_DATE', 'row[17]'),
            ('DEBT_GROUP', 'row[18]'),
            ('GAC_LAST_CHANGE_TIME', 'row[19]'),
            ('GAC_CREATION_TIME', 'row[20]'),
            ('GAM_LAST_CHANGE_TIME', 'row[21]'),
            ('GAM_CREATION_TIME', 'row[22]')
        ])
    },
    RoboRepayUplView: {
        'table_name': 'custom.robo_repayupl_view',
        'row_dict': collections.OrderedDict([
            ('SRL_NUM', 'row[0]'),
            ('FILE_NAME', 'row[1]'),
            ('UPLOAD_DATE', 'row[2]'),
            ('REF_NUM', 'row[3]'),
            ('LOAN_ACCT_NUM', 'row[4]'),
            ('CUSTOMER_NAME', 'row[5]'),
            ('DESCRIPTION', 'row[6]'),
            ('PAID_DATE', 'row[7]'),
            ('ACCT_CURRENCY', 'row[8]'),
            ('PAID_AMT', 'row[9]'),
            ('CUSTOMER_BANK_ACCOUNT', 'row[10]'),
            ('CHEQUE_ID', 'row[11]'),
            ('FAIL_FLG', 'row[12]'),
            ('FAIL_REASON', 'row[13]'),
            ('LCHG_TIME', 'row[14]'),
            ('LCHG_USER_ID', 'row[15]'),
            ('RCRE_USER_ID', 'row[16]'),
            ('RCRE_TIME', 'row[17]'),
            ('BANK_ID', 'row[18]'),
        ])
    },
    RoboIdtView: {
        'table_name': 'custom.robo_ldt_view',
        'row_dict': collections.OrderedDict([
            ('LOAN_ACCT_NUM', 'row[0]'),
            ('SHDL_NUM', 'row[1]'),
            ('DMD_FLOW_ID', 'row[2]'),
            ('ACID', 'row[3]'),
            ('DMD_EFF_DATE', 'row[4]'),
            ('DMD_SRL_NUM', 'row[5]'),
            ('DMD_OVDU_DATE', 'row[6]'),
            ('DMD_AMT', 'row[7]'),
            ('TOT_ADJ_AMT', 'row[8]'),
            ('LAST_ADJ_DATE', 'row[9]'),
            ('WAIVED_AMT', 'row[10]'),
            ('LAST_WAIVER_ADJ_DATE', 'row[11]'),
            ('LATEFEE_STATUS_FLG', 'row[12]'),
            ('GAM_CREATION_TIME', 'row[13]'),
            ('GAM_LAST_CHANGE_TIME', 'row[14]'),
            ('LDT_CREATION_TIME', 'row[15]'),
            ('LDT_LAST_CHANGE_TIME', 'row[16]'),
        ])
    },
    RoboClelarshView: {
        'table_name': 'custom.robo_clelarsh_view',
        'row_dict': collections.OrderedDict([
            ('ACID', 'row[0]'),
            ('LOAN_ACCT_NUM', 'row[1]'),
            ('PRIN_CMP', 'row[2]'),
            ('INT_CMP', 'row[3]'),
            ('CHRG_CMP', 'row[4]'),
            ('TOTAL_FLOW', 'row[5]'),
            ('REP_SHDL_DATE', 'row[6]'),
            ('SHDL_NUM', 'row[7]'),
            ('BANK_ID', 'row[8]'),
            ('RCRE_USER_ID', 'row[9]'),
            ('RCRE_TIME', 'row[10]'),
            ('LCHG_USER_ID', 'row[11]'),
            ('LCHG_TIME', 'row[12]'),
            ('STATUS_FLG', 'row[13]'),
            ('SRL_NUM', 'row[14]')
        ])
    },
    RoboChatView: {
        'table_name': 'custom.robo_chat_view',
        'row_dict': collections.OrderedDict([
            ('ACID', 'row[0]'),
            ('LOAN_ACCT_NUM', 'row[1]'),
            ('CHARGE_TYPE', 'row[2]'),
            ('SYS_CALC_CHRGE_AMT', 'row[3]'),
            ('USER_CALC_CHRGE_AMT', 'row[4]'),
            ('CHRGE_AMT_COLLECTED', 'row[5]'),
            ('CHRGE_WAIVED', 'row[6]'),
            ('CHARGE_OUTSTANDING', 'row[7]'),
            ('GAM_CREATION_TIME', 'row[8]'),
            ('GAM_LAST_CHANGE_TIME', 'row[9]'),
            ('CHAT_CREATION_TIME', 'row[10]'),
            ('CHAT_LAST_CHANGE_TIME', 'row[11]')

        ])
    },
    RoboEitView: {
        'table_name': 'custom.robo_eit_view',
        'row_dict': collections.OrderedDict([
            ('LOAN_ACCT_NUM', 'row[0]'),
            ('ACID', 'row[1]'),
            ('ACCRUED_UPTO_DATE_CR', 'row[2]'),
            ('ACCRUED_UPTO_DATE_DR', 'row[3]'),
            ('LAST_ACCRUAL_RUN_DATE_CR', 'row[4]'),
            ('LAST_ACCRUAL_RUN_DATE_DR', 'row[5]'),
            ('NRML_ACCRUED_AMOUNT_CR', 'row[6]'),
            ('NRML_ACCRUED_AMOUNT_DR', 'row[7]'),
            ('BOOKED_UPTO_DATE_CR', 'row[8]'),
            ('BOOKED_UPTO_DATE_DR', 'row[9]'),
            ('LAST_BOOK_RUN_DATE_CR', 'row[10]'),
            ('LAST_BOOK_RUN_DATE_DR', 'row[11]'),
            ('BOOK_FOR_REV_DATE_CR', 'row[12]'),
            ('BOOK_FOR_REV_DATE_DR', 'row[13]'),
            ('NRML_BOOKED_AMOUNT_CR', 'row[14]'),
            ('NRML_BOOKED_AMOUNT_DR', 'row[15]'),
            ('INTEREST_CALC_UPTO_DATE_CR', 'row[16]'),
            ('INTEREST_CALC_UPTO_DATE_DR', 'row[17]'),
            ('NRML_INTEREST_AMOUNT_CR', 'row[18]'),
            ('NRML_INTEREST_AMOUNT_DR', 'row[19]'),
            ('LAST_INTEREST_RUN_DATE_CR', 'row[20]'),
            ('LAST_INTEREST_RUN_DATE_DR', 'row[21]'),
            ('NEXT_INT_RUN_DATE_DR', 'row[22]'),
            ('NRML_INT_SUSPENSE_AMT_DR', 'row[23]'),
            ('PENAL_ACCRUED_AMOUNT_DR', 'row[24]'),
            ('PENAL_BOOKED_AMOUNT_DR', 'row[25]'),
            ('PENAL_INTEREST_AMOUNT_DR', 'row[26]'),
            ('PENAL_INT_SUSPENSE_AMT_DR', 'row[27]'),
            ('ACCOUNT_PEGGED_FLG', 'row[28]'),
            ('GAM_CREATION_TIME', 'row[29]'),
            ('GAM_LAST_CHANGE_TIME', 'row[30]'),
            ('EIT_CREATION_TIME', 'row[31]'),
            ('EIT_LAST_CHANGE_TIME', 'row[32]')
        ])
    },
    RoboLrsView: {
        'table_name': 'custom.robo_lrs_view',
        'row_dict': collections.OrderedDict([
            ('LOAN_ACCT_NUM', 'row[0]'),
            ('ACID', 'row[1]'),
            ('FLOW_ID', 'row[2]'),
            ('NUM_OF_FLOWS', 'row[3]'),
            ('FLOW_AMT', 'row[4]'),
            ('NUM_OF_DMDS', 'row[5]'),
            ('NEXT_DMD_DATE', 'row[6]'),
            ('NEXT_INT_DMD_DATE', 'row[7]'),
            ('CURRENT_INT_REC_FLG', 'row[8]'),
            ('GAM_CREATION_TIME', 'row[9]'),
            ('GAM_LAST_CHANGE_TIME', 'row[10]'),
            ('LRS_CREATION_TIME', 'row[11]'),
            ('LRS_LAST_CHANGE_TIME', 'row[12]')
        ])
    },
    RoboLdaView: {
        'table_name': 'custom.ROBO_LDA_VIEW',
        'row_dict': collections.OrderedDict([
            ('LOAN_ACCT_NUM', 'row[0]'),
            ('ACID', 'row[1]'),
            ('SHDL_NUM', 'row[2]'),
            ('DMD_FLOW_ID', 'row[3]'),
            ('DMD_DATE', 'row[4]'),
            ('DMD_SRL_NUM', 'row[5]'),
            ('SRL_NUM', 'row[6]'),
            ('DEL_FLG', 'row[7]'),
            ('ADJ_DATE', 'row[8]'),
            ('ADJ_AMT', 'row[9]'),
            ('LCHG_USER_ID', 'row[10]'),
            ('LCHG_TIME', 'row[11]'),
            ('RCRE_USER_ID', 'row[12]'),
            ('RCRE_TIME', 'row[13]'),
            ('OFLOW_ADJ_FLG', 'row[14]'),
            ('TRAN_DATE', 'row[15]'),
            ('TRAN_ID', 'row[16]'),
            ('PART_TRAN_SRL_NUM', 'row[17]'),
            ('TS_CNT', 'row[18]'),
            ('BANK_ID', 'row[19]'),
            ('WAIVER_SRL_NUM', 'row[20]'),
            ('WAIVER_RECORD', 'row[21]')
        ])
    },
    RoboCxlView: {
        'table_name': 'custom.ROBO_CXL_VIEW',
        'row_dict': collections.OrderedDict([
            ('LOAN_ACCT_NUM', 'row[0]'),
            ('CXL_SRL_NUM', 'row[1]'),
            ('ENTITY_CRE_FLG', 'row[2]'),
            ('DEL_FLG', 'row[3]'),
            ('COMP_B2KID', 'row[4]'),
            ('COMP_B2KID_TYPE', 'row[5]'),
            ('SRL_NUM', 'row[6]'),
            ('CHRG_TRAN_ID', 'row[7]'),
            ('CHRG_PART_TRAN_SRL_NUM', 'row[8]'),
            ('CHRG_TRAN_DATE', 'row[9]'),
            ('PARENT_TRAN_ID', 'row[10]'),
            ('PARENT_TRAN_SRL_NUM', 'row[11]'),
            ('PARENT_TRAN_DATE', 'row[12]'),
            ('EVENT_TYPE', 'row[13]'),
            ('EVENT_ID', 'row[14]'),
            ('SERVICE_SOL_ID', 'row[15]'),
            ('SYSTEM_CALC_AMT', 'row[16]'),
            ('ACTUAL_AMT_COLL', 'row[17]'),
            ('COLL_CRNCY_CODE', 'row[18]'),
            ('TRAN_PARTICULAR', 'row[19]'),
            ('TRAN_RMKS', 'row[20]'),
            ('REVERSAL_FLG', 'row[21]'),
            ('START_DATE', 'row[22]'),
            ('END_DATE', 'row[23]'),
            ('TARGET_ACID', 'row[24]'),
            ('CUST_ID', 'row[25]'),
            ('CHRG_BORNE_BY_IND', 'row[26]'),
            ('PART_TRAN_TYPE', 'row[27]'),
            ('PTRAN_BUS_TYPE', 'row[28]'),
            ('CHRG_ACID', 'row[29]'),
            ('RATE_CODE1', 'row[30]'),
            ('RATE_CODE2', 'row[31]'),
            ('RATE_1', 'row[32]'),
            ('RATE_2', 'row[33]'),
            ('MODIFY_FLG', 'row[34]'),
            ('LCHG_USER_ID', 'row[35]'),
            ('LCHG_TIME', 'row[36]'),
            ('RCRE_USER_ID', 'row[37]'),
            ('RCRE_TIME', 'row[38]'),
            ('CONSOL_DEBIT_PTRAN_FLG', 'row[39]'),
            ('TS_CNT', 'row[40]'),
            ('CHRG_RPT_CODE', 'row[41]'),
            ('AMT_WITHOUT_DISCOUNT', 'row[42]'),
            ('REC_NOT_EFFECTIVE', 'row[43]'),
            ('CHANNEL_ID', 'row[44]'),
            ('AMT_AFTER_FIRST_LVL_DISC', 'row[45]'),
            ('RECORD_TYPE', 'row[46]'),
            ('CONSOLIDATED_TRAN_SRL_NUM', 'row[47]'),
            ('CHRG_GL_DATE', 'row[48]'),
            ('PARENT_GL_DATE', 'row[49]'),
            ('BANK_ID', 'row[50]'),
            ('AMT_BEFORE_ADDTNL_DISC', 'row[51]'),
            ('CHRG_DEBIT_PART_TRAN_SRL_NUM', 'row[52]'),
            ('DEFAULT_CHRG_CALC_FLG', 'row[53]'),
            ('REL_PRICING_REF_NUM', 'row[54]'),
            ('GL_SEGMENT_STRING', 'row[55]'),
            ('REF_CXL_SRL_NUM', 'row[56]'),
            ('PARENT_CXL_SRL_NUM', 'row[57]'),
            ('PART_CHRG_COLL_FLG', 'row[58]'),
            ('PENDING_CHRG_AMT', 'row[59]'),
            ('WAIVER_REASON_CODE', 'row[60]'),
            ('WAIVER_REMARKS', 'row[61]'),
            ('CHRG_REVERSAL_REASON_CODE', 'row[62]')
        ])
    },
    RoboLtdView: {
        'table_name': 'custom.ROBO_LTD_VIEW',
        'row_dict': collections.OrderedDict([
            ('LOAN_ACCT_NUM',  'row[0]'),
            ('TRAN_DATE',  'row[1]'),
            ('TRAN_ID',  'row[2]'),
            ('PART_TRAN_SRL_NUM',  'row[3]'),
            ('SHDL_NUM',  'row[4]'),
            ('FLOW_ID',  'row[5]'),
            ('ENTITY_CRE_FLG',  'row[6]'),
            ('DEL_FLG',  'row[7]'),
            ('ACID',  'row[8]'),
            ('VALUE_DATE',  'row[9]'),
            ('FLOW_AMT',  'row[10]'),
            ('REVERSAL_FLG',  'row[11]'),
            ('REVERSED_FLG',  'row[12]'),
            ('DMD_OFFSET_FLG',  'row[13]'),
            ('LCHG_USER_ID',  'row[14]'),
            ('LCHG_TIME',  'row[15]'),
            ('RCRE_USER_ID',  'row[16]'),
            ('RCRE_TIME',  'row[17]'),
            ('DMD_DATE',  'row[18]'),
            ('LAST_TRAN_FLG',  'row[19]'),
            ('LOAN_INT_ACID',  'row[20]'),
            ('REVERSAL_REF_ID',  'row[21]'),
            ('TYPE_OF_DMDS',  'row[22]'),
            ('DMD_SRL_NUM',  'row[23]'),
            ('ORIGIN_OF_TRAN',  'row[24]'),
            ('OFLOW_ADJ_FLG',  'row[25]'),
            ('TS_CNT',  'row[26]'),
            ('PRINCIPAL_AMT',  'row[27]'),
            ('INTEREST_AMT',  'row[28]'),
            ('BANKCHARGE_AMT',  'row[29]'),
            ('OTHERCHARGE_AMT',  'row[30]'),
            ('DMD_SATISFY_FLG',  'row[31]'),
            ('INT_BENEFIT_FLG',  'row[32]'),
            ('ADVANCE_PAYMENT_FLG',  'row[33]'),
            ('TRAN_VALUE_DATE',  'row[34]'),
            ('INT_BENEFIT_DATE',  'row[35]'),
            ('RAISE_DMD_FLG',  'row[36]'),
            ('RAISE_DMD_FOR_AMT',  'row[37]'),
            ('DEFERRED_INT_AMT',  'row[38]'),
            ('DEMAND_IND',  'row[39]'),
            ('PREPAYMENT_TYPE',  'row[40]'),
            ('INT_COLL_ON_PREPAYMENT_FLG',  'row[41]'),
            ('TRANSFER_TYPE',  'row[42]'),
            ('TOP_DISB_FLG',  'row[43]'),
            ('GL_DATE',  'row[44]'),
            ('BANK_ID',  'row[45]'),
            ('NORMAL_INTEREST_AMT',  'row[46]'),
            ('PENAL_INTEREST_AMT',  'row[47]'),
            ('OVERDUE_INTEREST_AMT',  'row[48]'),
            ('INTEREST_OVERDUE_AMT',  'row[49]'),
            ('HOLIDAY_INTEREST_AMT',  'row[50]'),
            ('NORMAL_PRINCIPAL_AMT',  'row[51]'),
            ('PRINCIPAL_OVERDUE_AMT',  'row[52]'),
            ('PLANNED_PREPAY_AMT',  'row[53]'),
            ('WAIVER_RECORD',  'row[54]'),
            ('ACCRUED_PENAL_INT_AMT',  'row[55]'),
            ('DEFERRED_INT_DMD_AMT',  'row[56]'),
            ('EMICAP_DEFERRED_INT',  'row[57]'),
            ('COMP_INT_AMT',  'row[58]'),
            ('PEN_ON_INT_AMT',  'row[59]'),
            ('PEN_ON_PRIN_AMT',  'row[60]'),
            ('INT_REFUND_PREPYMNT_FLG',  'row[61]'),
            ('MARGIN_MNY_AMT',  'row[62]'),
            ('RETENTION_AMT',  'row[63]'),
            ('BUILDER_PROFIT_AMT',  'row[64]'),
            ('ADJUST_FROM_SEC_DEP_FLG',  'row[65]')
        ])
    },
}

CHANNEL_DICT = {
    'FT': 'VPBANK',
    'TT': 'VPBANK',
    'PY': 'PAYOO',
    'MS': 'MAYOO',
    'VI': 'VIETTEL',
    'BI': 'BIDV',
    'AG': 'AGRIBANK',
    'NP': 'NAPAS'
}

WORKFLOW_REPORT_URL_DICT ={
    'customer_journey_tracking': 'customer_journey_tracking',
    'reject_loan_application': 'rejected_loan_application',
    'customer_portfolio': 'customer_portfolio',
    'disbursement_status_tracking': 'disbursement_status_tracking',
    'product_performance_report': 'product_performance_report',
    'customer_service_tracking': 'customer_service_tracking',
    'loan_portfolio_snapshot': 'loan_portfolio_snapshot',
    'loan_health_check': 'loan_health_check',
    'credit_card_fi': 'credit_card_fi'
}

MIS_REPORT_METHODS ={
    'customer_journey_tracking': 'mis_customer_journey_tracking_report',
    'reject_loan_application': 'mis_reject_loan_application_report',
    'api_status_tracking': 'mis_api_status_tracking_report',
    'customer_portfolio': 'mis_customer_portfolio_report',
    'disbursement_status_tracking': 'mis_disbursement_status_tracking_report',
    'robo_sales': 'mis_robo_sales_report',
    'loan_snapshot_active': 'mis_loan_snapshot_active_report',
    'product_performance': 'mis_product_performance_report',
    'loan_status_tracking': 'mis_loan_status_tracking_report',
    'customer_service_tracking': 'mis_customer_service_tracking_report',
    'loan_portfolio_snapshot': 'mis_loan_portfolio_snapshot_report',
    'loan_health_check': 'mis_loan_health_check',
    'credit_card_fi': 'mis_credit_card_fi'
}

MIS_SHARED_PATH = "/opt/mis_files/" + str(datetime.date.today()) + "/"

PROCESSING_FEE = 12000
INDEM = "INDEM"
PIDEM = "PIDEM"
PRDEM = "PRDEM"