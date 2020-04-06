from django.urls import path

from .views import (
    IndexView, PipelineSummaryListView, PipelineSummaryPDFView,
    PipelineSummaryExcelView, JobToPipelineAnalysisListView,
    JobsSummaryListView, JobsSummaryPDFView, JobsSummaryExcelView,
    JobToPipelineAnalysisPDFView, JobToPipelineAnalysisExcelView,
    CommissionsEarnedSummaryListView, CommissionsEarnedSummaryPDFView,
    CommissionsEarnedSummaryExcelView, MonthlyInvoicesSummaryListView,
    MonthlyInvoicesSummaryPDFView, MonthlyInvoicesSummaryExcelView,
    SuccessfulJobsListView, SuccessfulJobsPDFView, InterviewsReportListView,
    InterviewsReportPDFView, InterviewsExcelView)

app_name = 'reports'
urlpatterns = [
    path(
        'pdf/pipeline-summary/',
        PipelineSummaryPDFView.as_view(),
        name='pdf_pipeline_summary'),
    path(
        'excel/pipeline-summary/',
        PipelineSummaryExcelView.as_view(),
        name='excel_pipeline_summary'),
    path(
        'pipeline-summary/',
        PipelineSummaryListView.as_view(),
        name='pipeline_summary'),

    path(
        'successful-jobs/',
        SuccessfulJobsListView.as_view(),
        name='successful_jobs'),
    path(
        'pdf/successful-jobs/',
        SuccessfulJobsPDFView.as_view(),
        name='pdf_successful_jobs'),

    path(
        'pdf/jobs-summary/',
        JobsSummaryPDFView.as_view(),
        name='pdf_jobs_summary'),
    path(
        'excel/jobs-summary/',
        JobsSummaryExcelView.as_view(),
        name='excel_jobs_summary'),
    path(
        'jobs-summary/',
        JobsSummaryListView.as_view(),
        name='jobs_summary'),

    path(
        'pdf/job-to-pipeline-analysis/',
        JobToPipelineAnalysisPDFView.as_view(),
        name='pdf_job_to_pipeline_analysis'),
    path(
        'excel/job-to-pipeline-analysis/',
        JobToPipelineAnalysisExcelView.as_view(),
        name='excel_job_to_pipeline_analysis'),
    path(
        'job-to-pipeline-analysis/',
        JobToPipelineAnalysisListView.as_view(),
        name='job_to_pipeline_analysis'),

    path(
        'pdf/commissions-earned-summary/',
        CommissionsEarnedSummaryPDFView.as_view(),
        name='pdf_commissions_earned_summary'),
    path(
        'excel/commissions-earned-summary/',
        CommissionsEarnedSummaryExcelView.as_view(),
        name='excel_commissions_earned_summary'),
    path(
        'commissions-earned-summary/',
        CommissionsEarnedSummaryListView.as_view(),
        name='commissions_earned_summary'),

    path(
        'pdf/monthly-invoices-summary/',
        MonthlyInvoicesSummaryPDFView.as_view(),
        name='pdf_monthly_invoices_summary'),
    path(
        'excel/monthly-invoices-summary/',
        MonthlyInvoicesSummaryExcelView.as_view(),
        name='excel_monthly_invoices_summary'),
    path(
        'monthly-invoices-summary/',
        MonthlyInvoicesSummaryListView.as_view(),
        name='monthly_invoices_summary'),


    path(
        'pdf/interviews/',
        InterviewsReportPDFView.as_view(),
        name='pdf_interviews'),
    path(
        'excel/interviews/',
        InterviewsExcelView.as_view(),
        name='excel_interviews'),
    path(
        'interviews/',
        InterviewsReportListView.as_view(),
        name='interviews'),

    path('', IndexView.as_view(), name='index'),
]
