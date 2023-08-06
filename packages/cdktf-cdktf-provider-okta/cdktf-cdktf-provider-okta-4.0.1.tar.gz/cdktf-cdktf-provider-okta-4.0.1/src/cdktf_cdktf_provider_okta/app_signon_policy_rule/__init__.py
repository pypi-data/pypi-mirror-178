'''
# `okta_app_signon_policy_rule`

Refer to the Terraform Registory for docs: [`okta_app_signon_policy_rule`](https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule).
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


class AppSignonPolicyRule(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSignonPolicyRule.AppSignonPolicyRule",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule okta_app_signon_policy_rule}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        policy_id: builtins.str,
        access: typing.Optional[builtins.str] = None,
        constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_expression: typing.Optional[builtins.str] = None,
        device_is_managed: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        device_is_registered: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        factor_mode: typing.Optional[builtins.str] = None,
        groups_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        inactivity_period: typing.Optional[builtins.str] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        platform_include: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AppSignonPolicyRulePlatformInclude", typing.Dict[str, typing.Any]]]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        re_authentication_frequency: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        users_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_types_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_types_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule okta_app_signon_policy_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#name AppSignonPolicyRule#name}
        :param policy_id: ID of the policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#policy_id AppSignonPolicyRule#policy_id}
        :param access: Allow or deny access based on the rule conditions: ALLOW or DENY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#access AppSignonPolicyRule#access}
        :param constraints: An array that contains nested Authenticator Constraint objects that are organized by the Authenticator class. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#constraints AppSignonPolicyRule#constraints}
        :param custom_expression: This is an optional advanced setting. If the expression is formatted incorrectly or conflicts with conditions set above, the rule may not match any users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#custom_expression AppSignonPolicyRule#custom_expression}
        :param device_is_managed: If the device is managed. A device is managed if it's managed by a device management system. When managed is passed, registered must also be included and must be set to true. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_managed AppSignonPolicyRule#device_is_managed}
        :param device_is_registered: If the device is registered. A device is registered if the User enrolls with Okta Verify that is installed on the device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_registered AppSignonPolicyRule#device_is_registered}
        :param factor_mode: The number of factors required to satisfy this assurance level. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#factor_mode AppSignonPolicyRule#factor_mode}
        :param groups_excluded: List of group IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_excluded AppSignonPolicyRule#groups_excluded}
        :param groups_included: List of group IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_included AppSignonPolicyRule#groups_included}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#id AppSignonPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inactivity_period: The inactivity duration after which the end user must re-authenticate. Use the ISO 8601 Period format for recurring time intervals. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#inactivity_period AppSignonPolicyRule#inactivity_period}
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_connection AppSignonPolicyRule#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_excludes AppSignonPolicyRule#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_includes AppSignonPolicyRule#network_includes}
        :param platform_include: platform_include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#platform_include AppSignonPolicyRule#platform_include}
        :param priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#priority AppSignonPolicyRule#priority}.
        :param re_authentication_frequency: The duration after which the end user must re-authenticate, regardless of user activity. Use the ISO 8601 Period format for recurring time intervals. PT0S - Every sign-in attempt, PT43800H - Once per session Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#re_authentication_frequency AppSignonPolicyRule#re_authentication_frequency}
        :param status: Status of the rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#status AppSignonPolicyRule#status}
        :param type: The Verification Method type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#type AppSignonPolicyRule#type}
        :param users_excluded: Set of User IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_excluded AppSignonPolicyRule#users_excluded}
        :param users_included: Set of User IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_included AppSignonPolicyRule#users_included}
        :param user_types_excluded: Set of User Type IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_excluded AppSignonPolicyRule#user_types_excluded}
        :param user_types_included: Set of User Type IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_included AppSignonPolicyRule#user_types_included}
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
                name: builtins.str,
                policy_id: builtins.str,
                access: typing.Optional[builtins.str] = None,
                constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
                custom_expression: typing.Optional[builtins.str] = None,
                device_is_managed: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                device_is_registered: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                factor_mode: typing.Optional[builtins.str] = None,
                groups_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
                groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
                id: typing.Optional[builtins.str] = None,
                inactivity_period: typing.Optional[builtins.str] = None,
                network_connection: typing.Optional[builtins.str] = None,
                network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
                network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
                platform_include: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[AppSignonPolicyRulePlatformInclude, typing.Dict[str, typing.Any]]]]] = None,
                priority: typing.Optional[jsii.Number] = None,
                re_authentication_frequency: typing.Optional[builtins.str] = None,
                status: typing.Optional[builtins.str] = None,
                type: typing.Optional[builtins.str] = None,
                users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
                users_included: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_types_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_types_included: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        config = AppSignonPolicyRuleConfig(
            name=name,
            policy_id=policy_id,
            access=access,
            constraints=constraints,
            custom_expression=custom_expression,
            device_is_managed=device_is_managed,
            device_is_registered=device_is_registered,
            factor_mode=factor_mode,
            groups_excluded=groups_excluded,
            groups_included=groups_included,
            id=id,
            inactivity_period=inactivity_period,
            network_connection=network_connection,
            network_excludes=network_excludes,
            network_includes=network_includes,
            platform_include=platform_include,
            priority=priority,
            re_authentication_frequency=re_authentication_frequency,
            status=status,
            type=type,
            users_excluded=users_excluded,
            users_included=users_included,
            user_types_excluded=user_types_excluded,
            user_types_included=user_types_included,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPlatformInclude")
    def put_platform_include(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AppSignonPolicyRulePlatformInclude", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[AppSignonPolicyRulePlatformInclude, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlatformInclude", [value]))

    @jsii.member(jsii_name="resetAccess")
    def reset_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccess", []))

    @jsii.member(jsii_name="resetConstraints")
    def reset_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConstraints", []))

    @jsii.member(jsii_name="resetCustomExpression")
    def reset_custom_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomExpression", []))

    @jsii.member(jsii_name="resetDeviceIsManaged")
    def reset_device_is_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceIsManaged", []))

    @jsii.member(jsii_name="resetDeviceIsRegistered")
    def reset_device_is_registered(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceIsRegistered", []))

    @jsii.member(jsii_name="resetFactorMode")
    def reset_factor_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFactorMode", []))

    @jsii.member(jsii_name="resetGroupsExcluded")
    def reset_groups_excluded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsExcluded", []))

    @jsii.member(jsii_name="resetGroupsIncluded")
    def reset_groups_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupsIncluded", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInactivityPeriod")
    def reset_inactivity_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInactivityPeriod", []))

    @jsii.member(jsii_name="resetNetworkConnection")
    def reset_network_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkConnection", []))

    @jsii.member(jsii_name="resetNetworkExcludes")
    def reset_network_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkExcludes", []))

    @jsii.member(jsii_name="resetNetworkIncludes")
    def reset_network_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkIncludes", []))

    @jsii.member(jsii_name="resetPlatformInclude")
    def reset_platform_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformInclude", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetReAuthenticationFrequency")
    def reset_re_authentication_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReAuthenticationFrequency", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUsersExcluded")
    def reset_users_excluded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsersExcluded", []))

    @jsii.member(jsii_name="resetUsersIncluded")
    def reset_users_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsersIncluded", []))

    @jsii.member(jsii_name="resetUserTypesExcluded")
    def reset_user_types_excluded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTypesExcluded", []))

    @jsii.member(jsii_name="resetUserTypesIncluded")
    def reset_user_types_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserTypesIncluded", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="platformInclude")
    def platform_include(self) -> "AppSignonPolicyRulePlatformIncludeList":
        return typing.cast("AppSignonPolicyRulePlatformIncludeList", jsii.get(self, "platformInclude"))

    @builtins.property
    @jsii.member(jsii_name="accessInput")
    def access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessInput"))

    @builtins.property
    @jsii.member(jsii_name="constraintsInput")
    def constraints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "constraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="customExpressionInput")
    def custom_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceIsManagedInput")
    def device_is_managed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "deviceIsManagedInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceIsRegisteredInput")
    def device_is_registered_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "deviceIsRegisteredInput"))

    @builtins.property
    @jsii.member(jsii_name="factorModeInput")
    def factor_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "factorModeInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsExcludedInput")
    def groups_excluded_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsExcludedInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsIncludedInput")
    def groups_included_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsIncludedInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inactivityPeriodInput")
    def inactivity_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inactivityPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkConnectionInput")
    def network_connection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="networkExcludesInput")
    def network_excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkExcludesInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIncludesInput")
    def network_includes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkIncludesInput"))

    @builtins.property
    @jsii.member(jsii_name="platformIncludeInput")
    def platform_include_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["AppSignonPolicyRulePlatformInclude"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["AppSignonPolicyRulePlatformInclude"]]], jsii.get(self, "platformIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="reAuthenticationFrequencyInput")
    def re_authentication_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reAuthenticationFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="usersExcludedInput")
    def users_excluded_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersExcludedInput"))

    @builtins.property
    @jsii.member(jsii_name="usersIncludedInput")
    def users_included_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usersIncludedInput"))

    @builtins.property
    @jsii.member(jsii_name="userTypesExcludedInput")
    def user_types_excluded_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userTypesExcludedInput"))

    @builtins.property
    @jsii.member(jsii_name="userTypesIncludedInput")
    def user_types_included_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userTypesIncludedInput"))

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
    @jsii.member(jsii_name="constraints")
    def constraints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "constraints"))

    @constraints.setter
    def constraints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraints", value)

    @builtins.property
    @jsii.member(jsii_name="customExpression")
    def custom_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customExpression"))

    @custom_expression.setter
    def custom_expression(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customExpression", value)

    @builtins.property
    @jsii.member(jsii_name="deviceIsManaged")
    def device_is_managed(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "deviceIsManaged"))

    @device_is_managed.setter
    def device_is_managed(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceIsManaged", value)

    @builtins.property
    @jsii.member(jsii_name="deviceIsRegistered")
    def device_is_registered(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "deviceIsRegistered"))

    @device_is_registered.setter
    def device_is_registered(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceIsRegistered", value)

    @builtins.property
    @jsii.member(jsii_name="factorMode")
    def factor_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "factorMode"))

    @factor_mode.setter
    def factor_mode(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "factorMode", value)

    @builtins.property
    @jsii.member(jsii_name="groupsExcluded")
    def groups_excluded(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsExcluded"))

    @groups_excluded.setter
    def groups_excluded(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsExcluded", value)

    @builtins.property
    @jsii.member(jsii_name="groupsIncluded")
    def groups_included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupsIncluded"))

    @groups_included.setter
    def groups_included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupsIncluded", value)

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
    @jsii.member(jsii_name="inactivityPeriod")
    def inactivity_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inactivityPeriod"))

    @inactivity_period.setter
    def inactivity_period(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inactivityPeriod", value)

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
    @jsii.member(jsii_name="networkConnection")
    def network_connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkConnection"))

    @network_connection.setter
    def network_connection(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConnection", value)

    @builtins.property
    @jsii.member(jsii_name="networkExcludes")
    def network_excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkExcludes"))

    @network_excludes.setter
    def network_excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkExcludes", value)

    @builtins.property
    @jsii.member(jsii_name="networkIncludes")
    def network_includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkIncludes"))

    @network_includes.setter
    def network_includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIncludes", value)

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
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="reAuthenticationFrequency")
    def re_authentication_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reAuthenticationFrequency"))

    @re_authentication_frequency.setter
    def re_authentication_frequency(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reAuthenticationFrequency", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="usersExcluded")
    def users_excluded(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "usersExcluded"))

    @users_excluded.setter
    def users_excluded(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usersExcluded", value)

    @builtins.property
    @jsii.member(jsii_name="usersIncluded")
    def users_included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "usersIncluded"))

    @users_included.setter
    def users_included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usersIncluded", value)

    @builtins.property
    @jsii.member(jsii_name="userTypesExcluded")
    def user_types_excluded(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userTypesExcluded"))

    @user_types_excluded.setter
    def user_types_excluded(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTypesExcluded", value)

    @builtins.property
    @jsii.member(jsii_name="userTypesIncluded")
    def user_types_included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userTypesIncluded"))

    @user_types_included.setter
    def user_types_included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTypesIncluded", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appSignonPolicyRule.AppSignonPolicyRuleConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "policy_id": "policyId",
        "access": "access",
        "constraints": "constraints",
        "custom_expression": "customExpression",
        "device_is_managed": "deviceIsManaged",
        "device_is_registered": "deviceIsRegistered",
        "factor_mode": "factorMode",
        "groups_excluded": "groupsExcluded",
        "groups_included": "groupsIncluded",
        "id": "id",
        "inactivity_period": "inactivityPeriod",
        "network_connection": "networkConnection",
        "network_excludes": "networkExcludes",
        "network_includes": "networkIncludes",
        "platform_include": "platformInclude",
        "priority": "priority",
        "re_authentication_frequency": "reAuthenticationFrequency",
        "status": "status",
        "type": "type",
        "users_excluded": "usersExcluded",
        "users_included": "usersIncluded",
        "user_types_excluded": "userTypesExcluded",
        "user_types_included": "userTypesIncluded",
    },
)
class AppSignonPolicyRuleConfig(cdktf.TerraformMetaArguments):
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
        name: builtins.str,
        policy_id: builtins.str,
        access: typing.Optional[builtins.str] = None,
        constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_expression: typing.Optional[builtins.str] = None,
        device_is_managed: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        device_is_registered: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        factor_mode: typing.Optional[builtins.str] = None,
        groups_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        inactivity_period: typing.Optional[builtins.str] = None,
        network_connection: typing.Optional[builtins.str] = None,
        network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        platform_include: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["AppSignonPolicyRulePlatformInclude", typing.Dict[str, typing.Any]]]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        re_authentication_frequency: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        users_included: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_types_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_types_included: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Policy Rule Name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#name AppSignonPolicyRule#name}
        :param policy_id: ID of the policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#policy_id AppSignonPolicyRule#policy_id}
        :param access: Allow or deny access based on the rule conditions: ALLOW or DENY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#access AppSignonPolicyRule#access}
        :param constraints: An array that contains nested Authenticator Constraint objects that are organized by the Authenticator class. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#constraints AppSignonPolicyRule#constraints}
        :param custom_expression: This is an optional advanced setting. If the expression is formatted incorrectly or conflicts with conditions set above, the rule may not match any users. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#custom_expression AppSignonPolicyRule#custom_expression}
        :param device_is_managed: If the device is managed. A device is managed if it's managed by a device management system. When managed is passed, registered must also be included and must be set to true. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_managed AppSignonPolicyRule#device_is_managed}
        :param device_is_registered: If the device is registered. A device is registered if the User enrolls with Okta Verify that is installed on the device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_registered AppSignonPolicyRule#device_is_registered}
        :param factor_mode: The number of factors required to satisfy this assurance level. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#factor_mode AppSignonPolicyRule#factor_mode}
        :param groups_excluded: List of group IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_excluded AppSignonPolicyRule#groups_excluded}
        :param groups_included: List of group IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_included AppSignonPolicyRule#groups_included}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#id AppSignonPolicyRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inactivity_period: The inactivity duration after which the end user must re-authenticate. Use the ISO 8601 Period format for recurring time intervals. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#inactivity_period AppSignonPolicyRule#inactivity_period}
        :param network_connection: Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_connection AppSignonPolicyRule#network_connection}
        :param network_excludes: The zones to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_excludes AppSignonPolicyRule#network_excludes}
        :param network_includes: The zones to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_includes AppSignonPolicyRule#network_includes}
        :param platform_include: platform_include block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#platform_include AppSignonPolicyRule#platform_include}
        :param priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#priority AppSignonPolicyRule#priority}.
        :param re_authentication_frequency: The duration after which the end user must re-authenticate, regardless of user activity. Use the ISO 8601 Period format for recurring time intervals. PT0S - Every sign-in attempt, PT43800H - Once per session Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#re_authentication_frequency AppSignonPolicyRule#re_authentication_frequency}
        :param status: Status of the rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#status AppSignonPolicyRule#status}
        :param type: The Verification Method type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#type AppSignonPolicyRule#type}
        :param users_excluded: Set of User IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_excluded AppSignonPolicyRule#users_excluded}
        :param users_included: Set of User IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_included AppSignonPolicyRule#users_included}
        :param user_types_excluded: Set of User Type IDs to exclude. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_excluded AppSignonPolicyRule#user_types_excluded}
        :param user_types_included: Set of User Type IDs to include. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_included AppSignonPolicyRule#user_types_included}
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
                name: builtins.str,
                policy_id: builtins.str,
                access: typing.Optional[builtins.str] = None,
                constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
                custom_expression: typing.Optional[builtins.str] = None,
                device_is_managed: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                device_is_registered: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                factor_mode: typing.Optional[builtins.str] = None,
                groups_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
                groups_included: typing.Optional[typing.Sequence[builtins.str]] = None,
                id: typing.Optional[builtins.str] = None,
                inactivity_period: typing.Optional[builtins.str] = None,
                network_connection: typing.Optional[builtins.str] = None,
                network_excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
                network_includes: typing.Optional[typing.Sequence[builtins.str]] = None,
                platform_include: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[AppSignonPolicyRulePlatformInclude, typing.Dict[str, typing.Any]]]]] = None,
                priority: typing.Optional[jsii.Number] = None,
                re_authentication_frequency: typing.Optional[builtins.str] = None,
                status: typing.Optional[builtins.str] = None,
                type: typing.Optional[builtins.str] = None,
                users_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
                users_included: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_types_excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
                user_types_included: typing.Optional[typing.Sequence[builtins.str]] = None,
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
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
            check_type(argname="argument custom_expression", value=custom_expression, expected_type=type_hints["custom_expression"])
            check_type(argname="argument device_is_managed", value=device_is_managed, expected_type=type_hints["device_is_managed"])
            check_type(argname="argument device_is_registered", value=device_is_registered, expected_type=type_hints["device_is_registered"])
            check_type(argname="argument factor_mode", value=factor_mode, expected_type=type_hints["factor_mode"])
            check_type(argname="argument groups_excluded", value=groups_excluded, expected_type=type_hints["groups_excluded"])
            check_type(argname="argument groups_included", value=groups_included, expected_type=type_hints["groups_included"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inactivity_period", value=inactivity_period, expected_type=type_hints["inactivity_period"])
            check_type(argname="argument network_connection", value=network_connection, expected_type=type_hints["network_connection"])
            check_type(argname="argument network_excludes", value=network_excludes, expected_type=type_hints["network_excludes"])
            check_type(argname="argument network_includes", value=network_includes, expected_type=type_hints["network_includes"])
            check_type(argname="argument platform_include", value=platform_include, expected_type=type_hints["platform_include"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument re_authentication_frequency", value=re_authentication_frequency, expected_type=type_hints["re_authentication_frequency"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument users_excluded", value=users_excluded, expected_type=type_hints["users_excluded"])
            check_type(argname="argument users_included", value=users_included, expected_type=type_hints["users_included"])
            check_type(argname="argument user_types_excluded", value=user_types_excluded, expected_type=type_hints["user_types_excluded"])
            check_type(argname="argument user_types_included", value=user_types_included, expected_type=type_hints["user_types_included"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "policy_id": policy_id,
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
        if constraints is not None:
            self._values["constraints"] = constraints
        if custom_expression is not None:
            self._values["custom_expression"] = custom_expression
        if device_is_managed is not None:
            self._values["device_is_managed"] = device_is_managed
        if device_is_registered is not None:
            self._values["device_is_registered"] = device_is_registered
        if factor_mode is not None:
            self._values["factor_mode"] = factor_mode
        if groups_excluded is not None:
            self._values["groups_excluded"] = groups_excluded
        if groups_included is not None:
            self._values["groups_included"] = groups_included
        if id is not None:
            self._values["id"] = id
        if inactivity_period is not None:
            self._values["inactivity_period"] = inactivity_period
        if network_connection is not None:
            self._values["network_connection"] = network_connection
        if network_excludes is not None:
            self._values["network_excludes"] = network_excludes
        if network_includes is not None:
            self._values["network_includes"] = network_includes
        if platform_include is not None:
            self._values["platform_include"] = platform_include
        if priority is not None:
            self._values["priority"] = priority
        if re_authentication_frequency is not None:
            self._values["re_authentication_frequency"] = re_authentication_frequency
        if status is not None:
            self._values["status"] = status
        if type is not None:
            self._values["type"] = type
        if users_excluded is not None:
            self._values["users_excluded"] = users_excluded
        if users_included is not None:
            self._values["users_included"] = users_included
        if user_types_excluded is not None:
            self._values["user_types_excluded"] = user_types_excluded
        if user_types_included is not None:
            self._values["user_types_included"] = user_types_included

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
    def name(self) -> builtins.str:
        '''Policy Rule Name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#name AppSignonPolicyRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''ID of the policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#policy_id AppSignonPolicyRule#policy_id}
        '''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access(self) -> typing.Optional[builtins.str]:
        '''Allow or deny access based on the rule conditions: ALLOW or DENY.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#access AppSignonPolicyRule#access}
        '''
        result = self._values.get("access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def constraints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array that contains nested Authenticator Constraint objects that are organized by the Authenticator class.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#constraints AppSignonPolicyRule#constraints}
        '''
        result = self._values.get("constraints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def custom_expression(self) -> typing.Optional[builtins.str]:
        '''This is an optional advanced setting.

        If the expression is formatted incorrectly or conflicts with conditions set above, the rule may not match any users.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#custom_expression AppSignonPolicyRule#custom_expression}
        '''
        result = self._values.get("custom_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_is_managed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''If the device is managed.

        A device is managed if it's managed by a device management system. When managed is passed, registered must also be included and must be set to true.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_managed AppSignonPolicyRule#device_is_managed}
        '''
        result = self._values.get("device_is_managed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def device_is_registered(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''If the device is registered.

        A device is registered if the User enrolls with Okta Verify that is installed on the device.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#device_is_registered AppSignonPolicyRule#device_is_registered}
        '''
        result = self._values.get("device_is_registered")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def factor_mode(self) -> typing.Optional[builtins.str]:
        '''The number of factors required to satisfy this assurance level.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#factor_mode AppSignonPolicyRule#factor_mode}
        '''
        result = self._values.get("factor_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups_excluded(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of group IDs to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_excluded AppSignonPolicyRule#groups_excluded}
        '''
        result = self._values.get("groups_excluded")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def groups_included(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of group IDs to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#groups_included AppSignonPolicyRule#groups_included}
        '''
        result = self._values.get("groups_included")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#id AppSignonPolicyRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inactivity_period(self) -> typing.Optional[builtins.str]:
        '''The inactivity duration after which the end user must re-authenticate.

        Use the ISO 8601 Period format for recurring time intervals.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#inactivity_period AppSignonPolicyRule#inactivity_period}
        '''
        result = self._values.get("inactivity_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_connection(self) -> typing.Optional[builtins.str]:
        '''Network selection mode: ANYWHERE, ZONE, ON_NETWORK, or OFF_NETWORK.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_connection AppSignonPolicyRule#network_connection}
        '''
        result = self._values.get("network_connection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_excludes AppSignonPolicyRule#network_excludes}
        '''
        result = self._values.get("network_excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The zones to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#network_includes AppSignonPolicyRule#network_includes}
        '''
        result = self._values.get("network_includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def platform_include(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["AppSignonPolicyRulePlatformInclude"]]]:
        '''platform_include block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#platform_include AppSignonPolicyRule#platform_include}
        '''
        result = self._values.get("platform_include")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["AppSignonPolicyRulePlatformInclude"]]], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#priority AppSignonPolicyRule#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def re_authentication_frequency(self) -> typing.Optional[builtins.str]:
        '''The duration after which the end user must re-authenticate, regardless of user activity.

        Use the ISO 8601 Period format for recurring time intervals. PT0S - Every sign-in attempt, PT43800H - Once per session

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#re_authentication_frequency AppSignonPolicyRule#re_authentication_frequency}
        '''
        result = self._values.get("re_authentication_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of the rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#status AppSignonPolicyRule#status}
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The Verification Method type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#type AppSignonPolicyRule#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users_excluded(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of User IDs to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_excluded AppSignonPolicyRule#users_excluded}
        '''
        result = self._values.get("users_excluded")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def users_included(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of User IDs to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#users_included AppSignonPolicyRule#users_included}
        '''
        result = self._values.get("users_included")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_types_excluded(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of User Type IDs to exclude.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_excluded AppSignonPolicyRule#user_types_excluded}
        '''
        result = self._values.get("user_types_excluded")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_types_included(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Set of User Type IDs to include.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#user_types_included AppSignonPolicyRule#user_types_included}
        '''
        result = self._values.get("user_types_included")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSignonPolicyRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.appSignonPolicyRule.AppSignonPolicyRulePlatformInclude",
    jsii_struct_bases=[],
    name_mapping={
        "os_expression": "osExpression",
        "os_type": "osType",
        "type": "type",
    },
)
class AppSignonPolicyRulePlatformInclude:
    def __init__(
        self,
        *,
        os_expression: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_expression: Only available with OTHER OS type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#os_expression AppSignonPolicyRule#os_expression}
        :param os_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#os_type AppSignonPolicyRule#os_type}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#type AppSignonPolicyRule#type}.
        '''
        if __debug__:
            def stub(
                *,
                os_expression: typing.Optional[builtins.str] = None,
                os_type: typing.Optional[builtins.str] = None,
                type: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument os_expression", value=os_expression, expected_type=type_hints["os_expression"])
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[str, typing.Any] = {}
        if os_expression is not None:
            self._values["os_expression"] = os_expression
        if os_type is not None:
            self._values["os_type"] = os_type
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def os_expression(self) -> typing.Optional[builtins.str]:
        '''Only available with OTHER OS type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#os_expression AppSignonPolicyRule#os_expression}
        '''
        result = self._values.get("os_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#os_type AppSignonPolicyRule#os_type}.'''
        result = self._values.get("os_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/app_signon_policy_rule#type AppSignonPolicyRule#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSignonPolicyRulePlatformInclude(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppSignonPolicyRulePlatformIncludeList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSignonPolicyRule.AppSignonPolicyRulePlatformIncludeList",
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
    ) -> "AppSignonPolicyRulePlatformIncludeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppSignonPolicyRulePlatformIncludeOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AppSignonPolicyRulePlatformInclude]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AppSignonPolicyRulePlatformInclude]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AppSignonPolicyRulePlatformInclude]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[AppSignonPolicyRulePlatformInclude]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AppSignonPolicyRulePlatformIncludeOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.appSignonPolicyRule.AppSignonPolicyRulePlatformIncludeOutputReference",
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

    @jsii.member(jsii_name="resetOsExpression")
    def reset_os_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsExpression", []))

    @jsii.member(jsii_name="resetOsType")
    def reset_os_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsType", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="osExpressionInput")
    def os_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="osExpression")
    def os_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osExpression"))

    @os_expression.setter
    def os_expression(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osExpression", value)

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[AppSignonPolicyRulePlatformInclude, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[AppSignonPolicyRulePlatformInclude, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[AppSignonPolicyRulePlatformInclude, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[AppSignonPolicyRulePlatformInclude, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AppSignonPolicyRule",
    "AppSignonPolicyRuleConfig",
    "AppSignonPolicyRulePlatformInclude",
    "AppSignonPolicyRulePlatformIncludeList",
    "AppSignonPolicyRulePlatformIncludeOutputReference",
]

publication.publish()
