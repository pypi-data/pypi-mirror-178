import logging

from django import forms
from django.conf import settings

from . import conf
from .manager import manager


def _get_handlers1():
    yield "", "Handler"
    yield "0", "Any Handler"
    if conf.SMART_LOG_ONLINE:
        yield conf.ONLINE_LOGGER_NAME, "Smart Handler"
    for x in manager.handlers.names:
        if x != conf.ONLINE_LOGGER_NAME:
            yield x, x


def _get_handlers2():
    for x in manager.handlers.names:
        if x != conf.ONLINE_LOGGER_NAME:
            yield x, x
    if conf.SMART_LOG_ONLINE:
        yield conf.ONLINE_LOGGER_NAME, "Smart Handler"


class FilterLogForm(forms.Form):
    logger = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Filter by logger name", "class": "search"}
        ),
    )
    level = forms.ChoiceField(label="", required=False, choices=[])

    @property
    def media(self):
        extra = "" if settings.DEBUG else ".min"
        js = ["smart_logging/online%s.js" % extra]
        return forms.Media(js=js)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["level"].choices = (["", "Level"],) + tuple(
            logging._levelToName.items()
        )


class ConfigForm(FilterLogForm):
    handler = forms.ChoiceField(label="", required=False, choices=[])
    propagate = forms.ChoiceField(
        label="",
        required=False,
        choices=[
            ("", "Propagate"),
            ("-1", "Propagate to parent"),
            ("0", "Do not propagate"),
        ],
    )

    @property
    def media(self):
        extra = "" if settings.DEBUG else ".min"
        js = ["smart_logging/config%s.js" % extra]
        return forms.Media(js=js)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["handler"].choices = _get_handlers1()


class LoggerConfigForm(forms.Form):
    logger = forms.CharField(max_length=1000, disabled=True, widget=forms.HiddenInput)
    handlers = forms.MultipleChoiceField(
        choices=(), required=False, widget=forms.CheckboxSelectMultiple
    )
    level = forms.TypedChoiceField(choices=logging._levelToName.items(), coerce=int)
    propagate = forms.BooleanField(required=False)
    online = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["handlers"].choices = _get_handlers2()

    def save(self):
        if self.changed_data:
            logger = logging.getLogger(self.cleaned_data["logger"])
            return manager.configure_logger(logger, **self.cleaned_data)
        return []


class LoggerConfigFormSet(forms.BaseFormSet):
    def save(self):
        return {form.cleaned_data["logger"]: form.save() for form in self.forms}


LoggerConfigFormSet = forms.formset_factory(
    LoggerConfigForm, formset=LoggerConfigFormSet, extra=0
)
