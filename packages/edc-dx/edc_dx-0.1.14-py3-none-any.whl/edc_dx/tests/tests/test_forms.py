from django import forms
from django.test import TestCase
from edc_crf.crf_form_validator_mixins import CrfFormValidatorMixin

from edc_dx import get_diagnosis_labels
from edc_dx.form_validators import DiagnosisFormValidatorMixin

from ..test_case_mixin import TestCaseMixin


class DiagnosisFormValidator(CrfFormValidatorMixin, DiagnosisFormValidatorMixin):
    def clean(self):
        self.get_diagnoses()
        for prefix, label in get_diagnosis_labels():
            self.applicable_if_not_diagnosed(
                prefix=prefix,
                field_applicable=f"{prefix}_test",
                label=label,
            )

    def get_consent_for_period_or_raise(self):
        pass


class MyModel:
    @classmethod
    def related_visit_model_attr(cls):
        return "subject_visit"


class TestDiagnosisFormValidator(TestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_identifier = self.enroll()
        self.create_visits(self.subject_identifier)

    def test_ok(self):
        data = dict(subject_visit=self.subject_visit_followup)
        form_validator = DiagnosisFormValidator(cleaned_data=data, model=MyModel)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn(
            "Please complete Clinical Review: Baseline",
            str(form_validator._errors.get("__all__")),
        )

    def test_ok2(self):

        data = dict(subject_visit=self.subject_visit_followup)
        form_validator = DiagnosisFormValidator(cleaned_data=data, model=MyModel)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn(
            "Please complete Clinical Review: Baseline",
            str(form_validator._errors.get("__all__")),
        )
