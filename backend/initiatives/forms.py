from django import forms

from .models import (
    Status, StatusInitiativeHear, StatusInitiativeEditing, StatusInitiativeProgress, StatusInitiativeFinished, StatusInitiativeDone, StatusInitiativeRejected
)

import logging

logger = logging.getLogger(__name__)


class InlineForceSaveNew(forms.ModelForm):
    def has_changed(self):
        '''
        Force save inline form if fields if equals than default
        '''
        if not self.instance.pk:
            return True
        else:
            return super().has_changed()

class HearStatusInlineForm(InlineForceSaveNew):
    class Meta:
        model = StatusInitiativeHear
        fields = ['email_content']

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance', None)
        if instance:
            pass
        else:
            default_email = Status.objects.get(name='Slišimo').default_email
            initial['email_content'] = default_email

        kwargs['initial'] = initial
        super().__init__(
            *args, **kwargs
        )


class EditingStatusInlineForm(InlineForceSaveNew):
    class Meta:
        model = StatusInitiativeEditing
        fields = ['email_content']

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance', None)
        if instance:
            pass
        else:
            default_email = Status.objects.get(name='Urejamo').default_email
            initial['email_content'] = default_email

        kwargs['initial'] = initial
        super().__init__(
            *args, **kwargs
        )


class ProgressStatusInlineForm(InlineForceSaveNew):
    class Meta:
        model = StatusInitiativeProgress
        fields = ['email_content']

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance', None)
        if instance:
            pass
        else:
            default_email = Status.objects.get(name='V izvajanju').default_email
            initial['email_content'] = default_email

        kwargs['initial'] = initial
        super().__init__(
            *args, **kwargs
        )


class DoneStatusInlineForm(InlineForceSaveNew):
    class Meta:
        model = StatusInitiativeDone
        fields = ['email_content']

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance', None)
        if instance:
            pass
        else:
            default_email = Status.objects.get(name='Izvedeno').default_email
            initial['email_content'] = default_email

        kwargs['initial'] = initial
        super().__init__(
            *args, **kwargs
        )


class FinishedStatusInlineForm(InlineForceSaveNew):
    class Meta:
        model = StatusInitiativeFinished
        fields = ['email_content']

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance', None)
        if instance:
            pass
        else:
            default_email = Status.objects.get(name='Zaključeno').default_email
            initial['email_content'] = default_email

        kwargs['initial'] = initial
        super().__init__(
            *args, **kwargs
        )


class RejectedStatusInlineForm(InlineForceSaveNew):
    class Meta:
        model = StatusInitiativeRejected
        fields = ['email_content']

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance', None)
        logger.debug('instance')
        if instance:
            pass
        else:
            status = Status.objects.get(name='Zavrnjeno')
            initial['email_content'] = status.default_email
            logger.debug(status.default_email)
            initial['status_id'] = status.id

        kwargs['initial'] = initial
        super().__init__(
            *args, **kwargs
        )
