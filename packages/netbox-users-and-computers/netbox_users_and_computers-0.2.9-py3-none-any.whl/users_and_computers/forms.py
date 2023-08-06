from netbox.forms import NetBoxModelForm
from pyrsistent import v
from .models import Aduser, RiskRelation, RiskAssignment
from utilities.forms import (
    BootstrapMixin, DynamicModelChoiceField)
from django import forms


class RiskForm(NetBoxModelForm):
    class Meta:
        model = Aduser
        fields = ('name',
                  'sAMAccountName',
                  'status',
                  'firstname',
                  'lastname', 'ad_guid', 'ad_description', 'position', 'department', 'comment',
                  'vpnIPaddress',
                  'description',
                  'comments')


class RiskRelationForm(NetBoxModelForm):
    class Meta:
        model = RiskRelation
        fields = ('name', 'description')


class RiskAssignmentForm(BootstrapMixin, forms.ModelForm):
    risk = DynamicModelChoiceField(
        queryset=Aduser.objects.all()
    )
    relation = DynamicModelChoiceField(
        queryset=RiskRelation.objects.all()
    )

    class Meta:
        model = RiskAssignment
        fields = (
            'risk', 'relation',
        )
