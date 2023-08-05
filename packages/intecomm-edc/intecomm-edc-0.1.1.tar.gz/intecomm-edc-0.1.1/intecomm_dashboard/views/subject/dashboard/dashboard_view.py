from edc_subject_dashboard.views import SubjectDashboardView


class DashboardView(SubjectDashboardView):

    consent_model = "intecomm_consent.subjectconsent"
    navbar_selected_item = "consented_subject"
    visit_model = "intecomm_subject.subjectvisit"
    history_button_label = "Audit"
