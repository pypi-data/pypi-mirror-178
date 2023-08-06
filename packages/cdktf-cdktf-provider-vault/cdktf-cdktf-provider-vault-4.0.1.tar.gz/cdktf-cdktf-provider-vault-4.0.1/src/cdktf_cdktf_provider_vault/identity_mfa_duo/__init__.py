'''
# `vault_identity_mfa_duo`

Refer to the Terraform Registory for docs: [`vault_identity_mfa_duo`](https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo).
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


class IdentityMfaDuo(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.identityMfaDuo.IdentityMfaDuo",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo vault_identity_mfa_duo}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        api_hostname: builtins.str,
        integration_key: builtins.str,
        secret_key: builtins.str,
        id: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        push_info: typing.Optional[builtins.str] = None,
        use_passcode: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        username_format: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo vault_identity_mfa_duo} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_hostname: API hostname for Duo. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#api_hostname IdentityMfaDuo#api_hostname}
        :param integration_key: Integration key for Duo. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#integration_key IdentityMfaDuo#integration_key}
        :param secret_key: Secret key for Duo. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#secret_key IdentityMfaDuo#secret_key}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#id IdentityMfaDuo#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#namespace IdentityMfaDuo#namespace}
        :param push_info: Push information for Duo. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#push_info IdentityMfaDuo#push_info}
        :param use_passcode: Require passcode upon MFA validation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#use_passcode IdentityMfaDuo#use_passcode}
        :param username_format: A template string for mapping Identity names to MFA methods. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#username_format IdentityMfaDuo#username_format}
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
                api_hostname: builtins.str,
                integration_key: builtins.str,
                secret_key: builtins.str,
                id: typing.Optional[builtins.str] = None,
                namespace: typing.Optional[builtins.str] = None,
                push_info: typing.Optional[builtins.str] = None,
                use_passcode: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                username_format: typing.Optional[builtins.str] = None,
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
        config = IdentityMfaDuoConfig(
            api_hostname=api_hostname,
            integration_key=integration_key,
            secret_key=secret_key,
            id=id,
            namespace=namespace,
            push_info=push_info,
            use_passcode=use_passcode,
            username_format=username_format,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetPushInfo")
    def reset_push_info(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushInfo", []))

    @jsii.member(jsii_name="resetUsePasscode")
    def reset_use_passcode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsePasscode", []))

    @jsii.member(jsii_name="resetUsernameFormat")
    def reset_username_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameFormat", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="methodId")
    def method_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "methodId"))

    @builtins.property
    @jsii.member(jsii_name="mountAccessor")
    def mount_accessor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountAccessor"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespaceId"))

    @builtins.property
    @jsii.member(jsii_name="namespacePath")
    def namespace_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespacePath"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property
    @jsii.member(jsii_name="apiHostnameInput")
    def api_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationKeyInput")
    def integration_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="pushInfoInput")
    def push_info_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pushInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyInput")
    def secret_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="usePasscodeInput")
    def use_passcode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "usePasscodeInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameFormatInput")
    def username_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="apiHostname")
    def api_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiHostname"))

    @api_hostname.setter
    def api_hostname(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiHostname", value)

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
    @jsii.member(jsii_name="integrationKey")
    def integration_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationKey"))

    @integration_key.setter
    def integration_key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationKey", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="pushInfo")
    def push_info(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pushInfo"))

    @push_info.setter
    def push_info(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushInfo", value)

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value)

    @builtins.property
    @jsii.member(jsii_name="usePasscode")
    def use_passcode(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "usePasscode"))

    @use_passcode.setter
    def use_passcode(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usePasscode", value)

    @builtins.property
    @jsii.member(jsii_name="usernameFormat")
    def username_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameFormat"))

    @username_format.setter
    def username_format(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameFormat", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.identityMfaDuo.IdentityMfaDuoConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_hostname": "apiHostname",
        "integration_key": "integrationKey",
        "secret_key": "secretKey",
        "id": "id",
        "namespace": "namespace",
        "push_info": "pushInfo",
        "use_passcode": "usePasscode",
        "username_format": "usernameFormat",
    },
)
class IdentityMfaDuoConfig(cdktf.TerraformMetaArguments):
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
        api_hostname: builtins.str,
        integration_key: builtins.str,
        secret_key: builtins.str,
        id: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        push_info: typing.Optional[builtins.str] = None,
        use_passcode: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        username_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_hostname: API hostname for Duo. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#api_hostname IdentityMfaDuo#api_hostname}
        :param integration_key: Integration key for Duo. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#integration_key IdentityMfaDuo#integration_key}
        :param secret_key: Secret key for Duo. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#secret_key IdentityMfaDuo#secret_key}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#id IdentityMfaDuo#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#namespace IdentityMfaDuo#namespace}
        :param push_info: Push information for Duo. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#push_info IdentityMfaDuo#push_info}
        :param use_passcode: Require passcode upon MFA validation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#use_passcode IdentityMfaDuo#use_passcode}
        :param username_format: A template string for mapping Identity names to MFA methods. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#username_format IdentityMfaDuo#username_format}
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
                api_hostname: builtins.str,
                integration_key: builtins.str,
                secret_key: builtins.str,
                id: typing.Optional[builtins.str] = None,
                namespace: typing.Optional[builtins.str] = None,
                push_info: typing.Optional[builtins.str] = None,
                use_passcode: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                username_format: typing.Optional[builtins.str] = None,
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
            check_type(argname="argument api_hostname", value=api_hostname, expected_type=type_hints["api_hostname"])
            check_type(argname="argument integration_key", value=integration_key, expected_type=type_hints["integration_key"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument push_info", value=push_info, expected_type=type_hints["push_info"])
            check_type(argname="argument use_passcode", value=use_passcode, expected_type=type_hints["use_passcode"])
            check_type(argname="argument username_format", value=username_format, expected_type=type_hints["username_format"])
        self._values: typing.Dict[str, typing.Any] = {
            "api_hostname": api_hostname,
            "integration_key": integration_key,
            "secret_key": secret_key,
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
        if id is not None:
            self._values["id"] = id
        if namespace is not None:
            self._values["namespace"] = namespace
        if push_info is not None:
            self._values["push_info"] = push_info
        if use_passcode is not None:
            self._values["use_passcode"] = use_passcode
        if username_format is not None:
            self._values["username_format"] = username_format

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
    def api_hostname(self) -> builtins.str:
        '''API hostname for Duo.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#api_hostname IdentityMfaDuo#api_hostname}
        '''
        result = self._values.get("api_hostname")
        assert result is not None, "Required property 'api_hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration_key(self) -> builtins.str:
        '''Integration key for Duo.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#integration_key IdentityMfaDuo#integration_key}
        '''
        result = self._values.get("integration_key")
        assert result is not None, "Required property 'integration_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_key(self) -> builtins.str:
        '''Secret key for Duo.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#secret_key IdentityMfaDuo#secret_key}
        '''
        result = self._values.get("secret_key")
        assert result is not None, "Required property 'secret_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#id IdentityMfaDuo#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Target namespace. (requires Enterprise).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#namespace IdentityMfaDuo#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def push_info(self) -> typing.Optional[builtins.str]:
        '''Push information for Duo.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#push_info IdentityMfaDuo#push_info}
        '''
        result = self._values.get("push_info")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_passcode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Require passcode upon MFA validation.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#use_passcode IdentityMfaDuo#use_passcode}
        '''
        result = self._values.get("use_passcode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def username_format(self) -> typing.Optional[builtins.str]:
        '''A template string for mapping Identity names to MFA methods.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/vault/r/identity_mfa_duo#username_format IdentityMfaDuo#username_format}
        '''
        result = self._values.get("username_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IdentityMfaDuoConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IdentityMfaDuo",
    "IdentityMfaDuoConfig",
]

publication.publish()
