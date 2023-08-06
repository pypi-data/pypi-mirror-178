'''
# `okta_policy_rule_profile_enrollment`

Refer to the Terraform Registory for docs: [`okta_policy_rule_profile_enrollment`](https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf
import constructs


class PolicyRuleProfileEnrollment(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleProfileEnrollment.PolicyRuleProfileEnrollment",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment okta_policy_rule_profile_enrollment}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        policy_id: builtins.str,
        unknown_user_action: builtins.str,
        access: typing.Optional[builtins.str] = None,
        email_verification: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        inline_hook_id: typing.Optional[builtins.str] = None,
        profile_attributes: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["PolicyRuleProfileEnrollmentProfileAttributes", typing.Dict[str, typing.Any]]]]] = None,
        target_group_id: typing.Optional[builtins.str] = None,
        ui_schema_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment okta_policy_rule_profile_enrollment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param policy_id: ID of the policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#policy_id PolicyRuleProfileEnrollment#policy_id}
        :param unknown_user_action: Which action should be taken if this User is new. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#unknown_user_action PolicyRuleProfileEnrollment#unknown_user_action}
        :param access: Allow or deny access based on the rule conditions: ALLOW or DENY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#access PolicyRuleProfileEnrollment#access}
        :param email_verification: Indicates whether email verification should occur before access is granted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#email_verification PolicyRuleProfileEnrollment#email_verification}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#id PolicyRuleProfileEnrollment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inline_hook_id: ID of a Registration Inline Hook. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#inline_hook_id PolicyRuleProfileEnrollment#inline_hook_id}
        :param profile_attributes: profile_attributes block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#profile_attributes PolicyRuleProfileEnrollment#profile_attributes}
        :param target_group_id: The ID of a Group that this User should be added to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#target_group_id PolicyRuleProfileEnrollment#target_group_id}
        :param ui_schema_id: Value created by the backend. If present all policy updates must include this attribute/value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#ui_schema_id PolicyRuleProfileEnrollment#ui_schema_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id_: builtins.str,
                *,
                policy_id: builtins.str,
                unknown_user_action: builtins.str,
                access: typing.Optional[builtins.str] = None,
                email_verification: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                id: typing.Optional[builtins.str] = None,
                inline_hook_id: typing.Optional[builtins.str] = None,
                profile_attributes: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[PolicyRuleProfileEnrollmentProfileAttributes, typing.Dict[str, typing.Any]]]]] = None,
                target_group_id: typing.Optional[builtins.str] = None,
                ui_schema_id: typing.Optional[builtins.str] = None,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PolicyRuleProfileEnrollmentConfig(
            policy_id=policy_id,
            unknown_user_action=unknown_user_action,
            access=access,
            email_verification=email_verification,
            id=id,
            inline_hook_id=inline_hook_id,
            profile_attributes=profile_attributes,
            target_group_id=target_group_id,
            ui_schema_id=ui_schema_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putProfileAttributes")
    def put_profile_attributes(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["PolicyRuleProfileEnrollmentProfileAttributes", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[PolicyRuleProfileEnrollmentProfileAttributes, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProfileAttributes", [value]))

    @jsii.member(jsii_name="resetAccess")
    def reset_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccess", []))

    @jsii.member(jsii_name="resetEmailVerification")
    def reset_email_verification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailVerification", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInlineHookId")
    def reset_inline_hook_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInlineHookId", []))

    @jsii.member(jsii_name="resetProfileAttributes")
    def reset_profile_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProfileAttributes", []))

    @jsii.member(jsii_name="resetTargetGroupId")
    def reset_target_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetGroupId", []))

    @jsii.member(jsii_name="resetUiSchemaId")
    def reset_ui_schema_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUiSchemaId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="profileAttributes")
    def profile_attributes(self) -> "PolicyRuleProfileEnrollmentProfileAttributesList":
        return typing.cast("PolicyRuleProfileEnrollmentProfileAttributesList", jsii.get(self, "profileAttributes"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="accessInput")
    def access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessInput"))

    @builtins.property
    @jsii.member(jsii_name="emailVerificationInput")
    def email_verification_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "emailVerificationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inlineHookIdInput")
    def inline_hook_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inlineHookIdInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="profileAttributesInput")
    def profile_attributes_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["PolicyRuleProfileEnrollmentProfileAttributes"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["PolicyRuleProfileEnrollmentProfileAttributes"]]], jsii.get(self, "profileAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupIdInput")
    def target_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="uiSchemaIdInput")
    def ui_schema_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uiSchemaIdInput"))

    @builtins.property
    @jsii.member(jsii_name="unknownUserActionInput")
    def unknown_user_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unknownUserActionInput"))

    @builtins.property
    @jsii.member(jsii_name="access")
    def access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "access"))

    @access.setter
    def access(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "access", value)

    @builtins.property
    @jsii.member(jsii_name="emailVerification")
    def email_verification(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "emailVerification"))

    @email_verification.setter
    def email_verification(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailVerification", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="inlineHookId")
    def inline_hook_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inlineHookId"))

    @inline_hook_id.setter
    def inline_hook_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inlineHookId", value)

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value)

    @builtins.property
    @jsii.member(jsii_name="targetGroupId")
    def target_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetGroupId"))

    @target_group_id.setter
    def target_group_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="uiSchemaId")
    def ui_schema_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uiSchemaId"))

    @ui_schema_id.setter
    def ui_schema_id(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uiSchemaId", value)

    @builtins.property
    @jsii.member(jsii_name="unknownUserAction")
    def unknown_user_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unknownUserAction"))

    @unknown_user_action.setter
    def unknown_user_action(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unknownUserAction", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleProfileEnrollment.PolicyRuleProfileEnrollmentConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "policy_id": "policyId",
        "unknown_user_action": "unknownUserAction",
        "access": "access",
        "email_verification": "emailVerification",
        "id": "id",
        "inline_hook_id": "inlineHookId",
        "profile_attributes": "profileAttributes",
        "target_group_id": "targetGroupId",
        "ui_schema_id": "uiSchemaId",
    },
)
class PolicyRuleProfileEnrollmentConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
        policy_id: builtins.str,
        unknown_user_action: builtins.str,
        access: typing.Optional[builtins.str] = None,
        email_verification: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        inline_hook_id: typing.Optional[builtins.str] = None,
        profile_attributes: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["PolicyRuleProfileEnrollmentProfileAttributes", typing.Dict[str, typing.Any]]]]] = None,
        target_group_id: typing.Optional[builtins.str] = None,
        ui_schema_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param policy_id: ID of the policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#policy_id PolicyRuleProfileEnrollment#policy_id}
        :param unknown_user_action: Which action should be taken if this User is new. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#unknown_user_action PolicyRuleProfileEnrollment#unknown_user_action}
        :param access: Allow or deny access based on the rule conditions: ALLOW or DENY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#access PolicyRuleProfileEnrollment#access}
        :param email_verification: Indicates whether email verification should occur before access is granted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#email_verification PolicyRuleProfileEnrollment#email_verification}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#id PolicyRuleProfileEnrollment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inline_hook_id: ID of a Registration Inline Hook. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#inline_hook_id PolicyRuleProfileEnrollment#inline_hook_id}
        :param profile_attributes: profile_attributes block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#profile_attributes PolicyRuleProfileEnrollment#profile_attributes}
        :param target_group_id: The ID of a Group that this User should be added to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#target_group_id PolicyRuleProfileEnrollment#target_group_id}
        :param ui_schema_id: Value created by the backend. If present all policy updates must include this attribute/value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#ui_schema_id PolicyRuleProfileEnrollment#ui_schema_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            def stub(
                *,
                connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
                count: typing.Optional[jsii.Number] = None,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                for_each: typing.Optional[cdktf.ITerraformIterator] = None,
                lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
                provider: typing.Optional[cdktf.TerraformProvider] = None,
                provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
                policy_id: builtins.str,
                unknown_user_action: builtins.str,
                access: typing.Optional[builtins.str] = None,
                email_verification: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                id: typing.Optional[builtins.str] = None,
                inline_hook_id: typing.Optional[builtins.str] = None,
                profile_attributes: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[PolicyRuleProfileEnrollmentProfileAttributes, typing.Dict[str, typing.Any]]]]] = None,
                target_group_id: typing.Optional[builtins.str] = None,
                ui_schema_id: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument unknown_user_action", value=unknown_user_action, expected_type=type_hints["unknown_user_action"])
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument email_verification", value=email_verification, expected_type=type_hints["email_verification"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inline_hook_id", value=inline_hook_id, expected_type=type_hints["inline_hook_id"])
            check_type(argname="argument profile_attributes", value=profile_attributes, expected_type=type_hints["profile_attributes"])
            check_type(argname="argument target_group_id", value=target_group_id, expected_type=type_hints["target_group_id"])
            check_type(argname="argument ui_schema_id", value=ui_schema_id, expected_type=type_hints["ui_schema_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "policy_id": policy_id,
            "unknown_user_action": unknown_user_action,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if access is not None:
            self._values["access"] = access
        if email_verification is not None:
            self._values["email_verification"] = email_verification
        if id is not None:
            self._values["id"] = id
        if inline_hook_id is not None:
            self._values["inline_hook_id"] = inline_hook_id
        if profile_attributes is not None:
            self._values["profile_attributes"] = profile_attributes
        if target_group_id is not None:
            self._values["target_group_id"] = target_group_id
        if ui_schema_id is not None:
            self._values["ui_schema_id"] = ui_schema_id

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[cdktf.SSHProvisionerConnection, cdktf.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[cdktf.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[cdktf.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[cdktf.FileProvisioner, cdktf.LocalExecProvisioner, cdktf.RemoteExecProvisioner]]], result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''ID of the policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#policy_id PolicyRuleProfileEnrollment#policy_id}
        '''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def unknown_user_action(self) -> builtins.str:
        '''Which action should be taken if this User is new.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#unknown_user_action PolicyRuleProfileEnrollment#unknown_user_action}
        '''
        result = self._values.get("unknown_user_action")
        assert result is not None, "Required property 'unknown_user_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access(self) -> typing.Optional[builtins.str]:
        '''Allow or deny access based on the rule conditions: ALLOW or DENY.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#access PolicyRuleProfileEnrollment#access}
        '''
        result = self._values.get("access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_verification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Indicates whether email verification should occur before access is granted.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#email_verification PolicyRuleProfileEnrollment#email_verification}
        '''
        result = self._values.get("email_verification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#id PolicyRuleProfileEnrollment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_hook_id(self) -> typing.Optional[builtins.str]:
        '''ID of a Registration Inline Hook.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#inline_hook_id PolicyRuleProfileEnrollment#inline_hook_id}
        '''
        result = self._values.get("inline_hook_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile_attributes(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["PolicyRuleProfileEnrollmentProfileAttributes"]]]:
        '''profile_attributes block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#profile_attributes PolicyRuleProfileEnrollment#profile_attributes}
        '''
        result = self._values.get("profile_attributes")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["PolicyRuleProfileEnrollmentProfileAttributes"]]], result)

    @builtins.property
    def target_group_id(self) -> typing.Optional[builtins.str]:
        '''The ID of a Group that this User should be added to.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#target_group_id PolicyRuleProfileEnrollment#target_group_id}
        '''
        result = self._values.get("target_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ui_schema_id(self) -> typing.Optional[builtins.str]:
        '''Value created by the backend. If present all policy updates must include this attribute/value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#ui_schema_id PolicyRuleProfileEnrollment#ui_schema_id}
        '''
        result = self._values.get("ui_schema_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleProfileEnrollmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyRuleProfileEnrollment.PolicyRuleProfileEnrollmentProfileAttributes",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "name": "name", "required": "required"},
)
class PolicyRuleProfileEnrollmentProfileAttributes:
    def __init__(
        self,
        *,
        label: builtins.str,
        name: builtins.str,
        required: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param label: A display-friendly label for this property. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#label PolicyRuleProfileEnrollment#label}
        :param name: The name of a User Profile property. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#name PolicyRuleProfileEnrollment#name}
        :param required: Indicates if this property is required for enrollment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#required PolicyRuleProfileEnrollment#required}
        '''
        if __debug__:
            def stub(
                *,
                label: builtins.str,
                name: builtins.str,
                required: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
        self._values: typing.Dict[str, typing.Any] = {
            "label": label,
            "name": name,
        }
        if required is not None:
            self._values["required"] = required

    @builtins.property
    def label(self) -> builtins.str:
        '''A display-friendly label for this property.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#label PolicyRuleProfileEnrollment#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of a User Profile property.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#name PolicyRuleProfileEnrollment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Indicates if this property is required for enrollment.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/policy_rule_profile_enrollment#required PolicyRuleProfileEnrollment#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyRuleProfileEnrollmentProfileAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyRuleProfileEnrollmentProfileAttributesList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleProfileEnrollment.PolicyRuleProfileEnrollmentProfileAttributesList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                wraps_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PolicyRuleProfileEnrollmentProfileAttributesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PolicyRuleProfileEnrollmentProfileAttributesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        if __debug__:
            def stub(value: cdktf.IInterpolatingParent) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            def stub(value: builtins.bool) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[PolicyRuleProfileEnrollmentProfileAttributes]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[PolicyRuleProfileEnrollmentProfileAttributes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[PolicyRuleProfileEnrollmentProfileAttributes]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[PolicyRuleProfileEnrollmentProfileAttributes]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class PolicyRuleProfileEnrollmentProfileAttributesOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyRuleProfileEnrollment.PolicyRuleProfileEnrollmentProfileAttributesOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
                complex_object_index: jsii.Number,
                complex_object_is_from_set: builtins.bool,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "required"))

    @required.setter
    def required(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[PolicyRuleProfileEnrollmentProfileAttributes, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[PolicyRuleProfileEnrollmentProfileAttributes, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[PolicyRuleProfileEnrollmentProfileAttributes, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[PolicyRuleProfileEnrollmentProfileAttributes, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "PolicyRuleProfileEnrollment",
    "PolicyRuleProfileEnrollmentConfig",
    "PolicyRuleProfileEnrollmentProfileAttributes",
    "PolicyRuleProfileEnrollmentProfileAttributesList",
    "PolicyRuleProfileEnrollmentProfileAttributesOutputReference",
]

publication.publish()
