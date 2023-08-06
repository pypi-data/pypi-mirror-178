'''
# `snowflake_external_oauth_integration`

Refer to the Terraform Registory for docs: [`snowflake_external_oauth_integration`](https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration).
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


class ExternalOauthIntegration(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegration",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration snowflake_external_oauth_integration}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        enabled: typing.Union[builtins.bool, cdktf.IResolvable],
        issuer: builtins.str,
        name: builtins.str,
        snowflake_user_mapping_attribute: builtins.str,
        token_user_mapping_claims: typing.Sequence[builtins.str],
        type: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        any_role_mode: typing.Optional[builtins.str] = None,
        audience_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        blocked_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        jws_keys_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        rsa_public_key: typing.Optional[builtins.str] = None,
        rsa_public_key2: typing.Optional[builtins.str] = None,
        scope_delimiter: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration snowflake_external_oauth_integration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enabled: Specifies whether to initiate operation of the integration or suspend it. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#enabled ExternalOauthIntegration#enabled}
        :param issuer: Specifies the URL to define the OAuth 2.0 authorization server. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#issuer ExternalOauthIntegration#issuer}
        :param name: Specifies the name of the External Oath integration. This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#name ExternalOauthIntegration#name}
        :param snowflake_user_mapping_attribute: Indicates which Snowflake user record attribute should be used to map the access token to a Snowflake user record. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#snowflake_user_mapping_attribute ExternalOauthIntegration#snowflake_user_mapping_attribute}
        :param token_user_mapping_claims: Specifies the access token claim or claims that can be used to map the access token to a Snowflake user record. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#token_user_mapping_claims ExternalOauthIntegration#token_user_mapping_claims}
        :param type: Specifies the OAuth 2.0 authorization server to be Okta, Microsoft Azure AD, Ping Identity PingFederate, or a Custom OAuth 2.0 authorization server. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#type ExternalOauthIntegration#type}
        :param allowed_roles: Specifies the list of roles that the client can set as the primary role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#allowed_roles ExternalOauthIntegration#allowed_roles}
        :param any_role_mode: Specifies whether the OAuth client or user can use a role that is not defined in the OAuth access token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#any_role_mode ExternalOauthIntegration#any_role_mode}
        :param audience_urls: Specifies additional values that can be used for the access token's audience validation on top of using the Customer's Snowflake Account URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#audience_urls ExternalOauthIntegration#audience_urls}
        :param blocked_roles: Specifies the list of roles that a client cannot set as the primary role. Do not include ACCOUNTADMIN, ORGADMIN or SECURITYADMIN as they are already implicitly enforced and will cause in-place updates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#blocked_roles ExternalOauthIntegration#blocked_roles}
        :param comment: Specifies a comment for the OAuth integration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#comment ExternalOauthIntegration#comment}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#id ExternalOauthIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jws_keys_urls: Specifies the endpoint or a list of endpoints from which to download public keys or certificates to validate an External OAuth access token. The maximum number of URLs that can be specified in the list is 3. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#jws_keys_urls ExternalOauthIntegration#jws_keys_urls}
        :param rsa_public_key: Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#rsa_public_key ExternalOauthIntegration#rsa_public_key}
        :param rsa_public_key2: Specifies a second RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. Used for key rotation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#rsa_public_key_2 ExternalOauthIntegration#rsa_public_key_2}
        :param scope_delimiter: Specifies the scope delimiter in the authorization token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#scope_delimiter ExternalOauthIntegration#scope_delimiter}
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
                enabled: typing.Union[builtins.bool, cdktf.IResolvable],
                issuer: builtins.str,
                name: builtins.str,
                snowflake_user_mapping_attribute: builtins.str,
                token_user_mapping_claims: typing.Sequence[builtins.str],
                type: builtins.str,
                allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
                any_role_mode: typing.Optional[builtins.str] = None,
                audience_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
                blocked_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
                comment: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                jws_keys_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
                rsa_public_key: typing.Optional[builtins.str] = None,
                rsa_public_key2: typing.Optional[builtins.str] = None,
                scope_delimiter: typing.Optional[builtins.str] = None,
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
        config = ExternalOauthIntegrationConfig(
            enabled=enabled,
            issuer=issuer,
            name=name,
            snowflake_user_mapping_attribute=snowflake_user_mapping_attribute,
            token_user_mapping_claims=token_user_mapping_claims,
            type=type,
            allowed_roles=allowed_roles,
            any_role_mode=any_role_mode,
            audience_urls=audience_urls,
            blocked_roles=blocked_roles,
            comment=comment,
            id=id,
            jws_keys_urls=jws_keys_urls,
            rsa_public_key=rsa_public_key,
            rsa_public_key2=rsa_public_key2,
            scope_delimiter=scope_delimiter,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetAnyRoleMode")
    def reset_any_role_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnyRoleMode", []))

    @jsii.member(jsii_name="resetAudienceUrls")
    def reset_audience_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudienceUrls", []))

    @jsii.member(jsii_name="resetBlockedRoles")
    def reset_blocked_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlockedRoles", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetJwsKeysUrls")
    def reset_jws_keys_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwsKeysUrls", []))

    @jsii.member(jsii_name="resetRsaPublicKey")
    def reset_rsa_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRsaPublicKey", []))

    @jsii.member(jsii_name="resetRsaPublicKey2")
    def reset_rsa_public_key2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRsaPublicKey2", []))

    @jsii.member(jsii_name="resetScopeDelimiter")
    def reset_scope_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopeDelimiter", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="anyRoleModeInput")
    def any_role_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "anyRoleModeInput"))

    @builtins.property
    @jsii.member(jsii_name="audienceUrlsInput")
    def audience_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "audienceUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="blockedRolesInput")
    def blocked_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "blockedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="jwsKeysUrlsInput")
    def jws_keys_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jwsKeysUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rsaPublicKey2Input")
    def rsa_public_key2_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rsaPublicKey2Input"))

    @builtins.property
    @jsii.member(jsii_name="rsaPublicKeyInput")
    def rsa_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rsaPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeDelimiterInput")
    def scope_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeUserMappingAttributeInput")
    def snowflake_user_mapping_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snowflakeUserMappingAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenUserMappingClaimsInput")
    def token_user_mapping_claims_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tokenUserMappingClaimsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="anyRoleMode")
    def any_role_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "anyRoleMode"))

    @any_role_mode.setter
    def any_role_mode(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anyRoleMode", value)

    @builtins.property
    @jsii.member(jsii_name="audienceUrls")
    def audience_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "audienceUrls"))

    @audience_urls.setter
    def audience_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audienceUrls", value)

    @builtins.property
    @jsii.member(jsii_name="blockedRoles")
    def blocked_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "blockedRoles"))

    @blocked_roles.setter
    def blocked_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

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
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value)

    @builtins.property
    @jsii.member(jsii_name="jwsKeysUrls")
    def jws_keys_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jwsKeysUrls"))

    @jws_keys_urls.setter
    def jws_keys_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwsKeysUrls", value)

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
    @jsii.member(jsii_name="rsaPublicKey")
    def rsa_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaPublicKey"))

    @rsa_public_key.setter
    def rsa_public_key(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaPublicKey", value)

    @builtins.property
    @jsii.member(jsii_name="rsaPublicKey2")
    def rsa_public_key2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaPublicKey2"))

    @rsa_public_key2.setter
    def rsa_public_key2(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rsaPublicKey2", value)

    @builtins.property
    @jsii.member(jsii_name="scopeDelimiter")
    def scope_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scopeDelimiter"))

    @scope_delimiter.setter
    def scope_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopeDelimiter", value)

    @builtins.property
    @jsii.member(jsii_name="snowflakeUserMappingAttribute")
    def snowflake_user_mapping_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snowflakeUserMappingAttribute"))

    @snowflake_user_mapping_attribute.setter
    def snowflake_user_mapping_attribute(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snowflakeUserMappingAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="tokenUserMappingClaims")
    def token_user_mapping_claims(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tokenUserMappingClaims"))

    @token_user_mapping_claims.setter
    def token_user_mapping_claims(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.List[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenUserMappingClaims", value)

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


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalOauthIntegration.ExternalOauthIntegrationConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "enabled": "enabled",
        "issuer": "issuer",
        "name": "name",
        "snowflake_user_mapping_attribute": "snowflakeUserMappingAttribute",
        "token_user_mapping_claims": "tokenUserMappingClaims",
        "type": "type",
        "allowed_roles": "allowedRoles",
        "any_role_mode": "anyRoleMode",
        "audience_urls": "audienceUrls",
        "blocked_roles": "blockedRoles",
        "comment": "comment",
        "id": "id",
        "jws_keys_urls": "jwsKeysUrls",
        "rsa_public_key": "rsaPublicKey",
        "rsa_public_key2": "rsaPublicKey2",
        "scope_delimiter": "scopeDelimiter",
    },
)
class ExternalOauthIntegrationConfig(cdktf.TerraformMetaArguments):
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
        enabled: typing.Union[builtins.bool, cdktf.IResolvable],
        issuer: builtins.str,
        name: builtins.str,
        snowflake_user_mapping_attribute: builtins.str,
        token_user_mapping_claims: typing.Sequence[builtins.str],
        type: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        any_role_mode: typing.Optional[builtins.str] = None,
        audience_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        blocked_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        jws_keys_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        rsa_public_key: typing.Optional[builtins.str] = None,
        rsa_public_key2: typing.Optional[builtins.str] = None,
        scope_delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param enabled: Specifies whether to initiate operation of the integration or suspend it. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#enabled ExternalOauthIntegration#enabled}
        :param issuer: Specifies the URL to define the OAuth 2.0 authorization server. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#issuer ExternalOauthIntegration#issuer}
        :param name: Specifies the name of the External Oath integration. This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#name ExternalOauthIntegration#name}
        :param snowflake_user_mapping_attribute: Indicates which Snowflake user record attribute should be used to map the access token to a Snowflake user record. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#snowflake_user_mapping_attribute ExternalOauthIntegration#snowflake_user_mapping_attribute}
        :param token_user_mapping_claims: Specifies the access token claim or claims that can be used to map the access token to a Snowflake user record. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#token_user_mapping_claims ExternalOauthIntegration#token_user_mapping_claims}
        :param type: Specifies the OAuth 2.0 authorization server to be Okta, Microsoft Azure AD, Ping Identity PingFederate, or a Custom OAuth 2.0 authorization server. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#type ExternalOauthIntegration#type}
        :param allowed_roles: Specifies the list of roles that the client can set as the primary role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#allowed_roles ExternalOauthIntegration#allowed_roles}
        :param any_role_mode: Specifies whether the OAuth client or user can use a role that is not defined in the OAuth access token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#any_role_mode ExternalOauthIntegration#any_role_mode}
        :param audience_urls: Specifies additional values that can be used for the access token's audience validation on top of using the Customer's Snowflake Account URL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#audience_urls ExternalOauthIntegration#audience_urls}
        :param blocked_roles: Specifies the list of roles that a client cannot set as the primary role. Do not include ACCOUNTADMIN, ORGADMIN or SECURITYADMIN as they are already implicitly enforced and will cause in-place updates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#blocked_roles ExternalOauthIntegration#blocked_roles}
        :param comment: Specifies a comment for the OAuth integration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#comment ExternalOauthIntegration#comment}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#id ExternalOauthIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param jws_keys_urls: Specifies the endpoint or a list of endpoints from which to download public keys or certificates to validate an External OAuth access token. The maximum number of URLs that can be specified in the list is 3. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#jws_keys_urls ExternalOauthIntegration#jws_keys_urls}
        :param rsa_public_key: Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#rsa_public_key ExternalOauthIntegration#rsa_public_key}
        :param rsa_public_key2: Specifies a second RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers. Used for key rotation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#rsa_public_key_2 ExternalOauthIntegration#rsa_public_key_2}
        :param scope_delimiter: Specifies the scope delimiter in the authorization token. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#scope_delimiter ExternalOauthIntegration#scope_delimiter}
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
                enabled: typing.Union[builtins.bool, cdktf.IResolvable],
                issuer: builtins.str,
                name: builtins.str,
                snowflake_user_mapping_attribute: builtins.str,
                token_user_mapping_claims: typing.Sequence[builtins.str],
                type: builtins.str,
                allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
                any_role_mode: typing.Optional[builtins.str] = None,
                audience_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
                blocked_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
                comment: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                jws_keys_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
                rsa_public_key: typing.Optional[builtins.str] = None,
                rsa_public_key2: typing.Optional[builtins.str] = None,
                scope_delimiter: typing.Optional[builtins.str] = None,
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
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument snowflake_user_mapping_attribute", value=snowflake_user_mapping_attribute, expected_type=type_hints["snowflake_user_mapping_attribute"])
            check_type(argname="argument token_user_mapping_claims", value=token_user_mapping_claims, expected_type=type_hints["token_user_mapping_claims"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument any_role_mode", value=any_role_mode, expected_type=type_hints["any_role_mode"])
            check_type(argname="argument audience_urls", value=audience_urls, expected_type=type_hints["audience_urls"])
            check_type(argname="argument blocked_roles", value=blocked_roles, expected_type=type_hints["blocked_roles"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument jws_keys_urls", value=jws_keys_urls, expected_type=type_hints["jws_keys_urls"])
            check_type(argname="argument rsa_public_key", value=rsa_public_key, expected_type=type_hints["rsa_public_key"])
            check_type(argname="argument rsa_public_key2", value=rsa_public_key2, expected_type=type_hints["rsa_public_key2"])
            check_type(argname="argument scope_delimiter", value=scope_delimiter, expected_type=type_hints["scope_delimiter"])
        self._values: typing.Dict[str, typing.Any] = {
            "enabled": enabled,
            "issuer": issuer,
            "name": name,
            "snowflake_user_mapping_attribute": snowflake_user_mapping_attribute,
            "token_user_mapping_claims": token_user_mapping_claims,
            "type": type,
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
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if any_role_mode is not None:
            self._values["any_role_mode"] = any_role_mode
        if audience_urls is not None:
            self._values["audience_urls"] = audience_urls
        if blocked_roles is not None:
            self._values["blocked_roles"] = blocked_roles
        if comment is not None:
            self._values["comment"] = comment
        if id is not None:
            self._values["id"] = id
        if jws_keys_urls is not None:
            self._values["jws_keys_urls"] = jws_keys_urls
        if rsa_public_key is not None:
            self._values["rsa_public_key"] = rsa_public_key
        if rsa_public_key2 is not None:
            self._values["rsa_public_key2"] = rsa_public_key2
        if scope_delimiter is not None:
            self._values["scope_delimiter"] = scope_delimiter

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
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        '''Specifies whether to initiate operation of the integration or suspend it.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#enabled ExternalOauthIntegration#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], result)

    @builtins.property
    def issuer(self) -> builtins.str:
        '''Specifies the URL to define the OAuth 2.0 authorization server.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#issuer ExternalOauthIntegration#issuer}
        '''
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the External Oath integration.

        This name follows the rules for Object Identifiers. The name should be unique among security integrations in your account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#name ExternalOauthIntegration#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snowflake_user_mapping_attribute(self) -> builtins.str:
        '''Indicates which Snowflake user record attribute should be used to map the access token to a Snowflake user record.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#snowflake_user_mapping_attribute ExternalOauthIntegration#snowflake_user_mapping_attribute}
        '''
        result = self._values.get("snowflake_user_mapping_attribute")
        assert result is not None, "Required property 'snowflake_user_mapping_attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token_user_mapping_claims(self) -> typing.List[builtins.str]:
        '''Specifies the access token claim or claims that can be used to map the access token to a Snowflake user record.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#token_user_mapping_claims ExternalOauthIntegration#token_user_mapping_claims}
        '''
        result = self._values.get("token_user_mapping_claims")
        assert result is not None, "Required property 'token_user_mapping_claims' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Specifies the OAuth 2.0 authorization server to be Okta, Microsoft Azure AD, Ping Identity PingFederate, or a Custom OAuth 2.0 authorization server.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#type ExternalOauthIntegration#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of roles that the client can set as the primary role.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#allowed_roles ExternalOauthIntegration#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def any_role_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the OAuth client or user can use a role that is not defined in the OAuth access token.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#any_role_mode ExternalOauthIntegration#any_role_mode}
        '''
        result = self._values.get("any_role_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def audience_urls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies additional values that can be used for the access token's audience validation on top of using the Customer's Snowflake Account URL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#audience_urls ExternalOauthIntegration#audience_urls}
        '''
        result = self._values.get("audience_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def blocked_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of roles that a client cannot set as the primary role.

        Do not include ACCOUNTADMIN, ORGADMIN or SECURITYADMIN as they are already implicitly enforced and will cause in-place updates.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#blocked_roles ExternalOauthIntegration#blocked_roles}
        '''
        result = self._values.get("blocked_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the OAuth integration.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#comment ExternalOauthIntegration#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#id ExternalOauthIntegration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jws_keys_urls(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the endpoint or a list of endpoints from which to download public keys or certificates to validate an External OAuth access token.

        The maximum number of URLs that can be specified in the list is 3.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#jws_keys_urls ExternalOauthIntegration#jws_keys_urls}
        '''
        result = self._values.get("jws_keys_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rsa_public_key(self) -> typing.Optional[builtins.str]:
        '''Specifies a Base64-encoded RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#rsa_public_key ExternalOauthIntegration#rsa_public_key}
        '''
        result = self._values.get("rsa_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_public_key2(self) -> typing.Optional[builtins.str]:
        '''Specifies a second RSA public key, without the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- headers.

        Used for key rotation.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#rsa_public_key_2 ExternalOauthIntegration#rsa_public_key_2}
        '''
        result = self._values.get("rsa_public_key2")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope_delimiter(self) -> typing.Optional[builtins.str]:
        '''Specifies the scope delimiter in the authorization token.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/external_oauth_integration#scope_delimiter ExternalOauthIntegration#scope_delimiter}
        '''
        result = self._values.get("scope_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalOauthIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ExternalOauthIntegration",
    "ExternalOauthIntegrationConfig",
]

publication.publish()
