'''
# `google_network_services_edge_cache_keyset`

Refer to the Terraform Registory for docs: [`google_network_services_edge_cache_keyset`](https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset).
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


class GoogleNetworkServicesEdgeCacheKeyset(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheKeyset.GoogleNetworkServicesEdgeCacheKeyset",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset google_network_services_edge_cache_keyset}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        public_key: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheKeysetPublicKey", typing.Dict[str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheKeysetTimeouts", typing.Dict[str, typing.Any]]] = None,
        validation_shared_keys: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys", typing.Dict[str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset google_network_services_edge_cache_keyset} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#name GoogleNetworkServicesEdgeCacheKeyset#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#description GoogleNetworkServicesEdgeCacheKeyset#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#id GoogleNetworkServicesEdgeCacheKeyset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the EdgeCache resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#labels GoogleNetworkServicesEdgeCacheKeyset#labels}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#project GoogleNetworkServicesEdgeCacheKeyset#project}.
        :param public_key: public_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#public_key GoogleNetworkServicesEdgeCacheKeyset#public_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#timeouts GoogleNetworkServicesEdgeCacheKeyset#timeouts}
        :param validation_shared_keys: validation_shared_keys block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#validation_shared_keys GoogleNetworkServicesEdgeCacheKeyset#validation_shared_keys}
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
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                project: typing.Optional[builtins.str] = None,
                public_key: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheKeysetPublicKey, typing.Dict[str, typing.Any]]]]] = None,
                timeouts: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetTimeouts, typing.Dict[str, typing.Any]]] = None,
                validation_shared_keys: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys, typing.Dict[str, typing.Any]]]]] = None,
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
        config = GoogleNetworkServicesEdgeCacheKeysetConfig(
            name=name,
            description=description,
            id=id,
            labels=labels,
            project=project,
            public_key=public_key,
            timeouts=timeouts,
            validation_shared_keys=validation_shared_keys,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPublicKey")
    def put_public_key(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheKeysetPublicKey", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheKeysetPublicKey, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPublicKey", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#create GoogleNetworkServicesEdgeCacheKeyset#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#delete GoogleNetworkServicesEdgeCacheKeyset#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#update GoogleNetworkServicesEdgeCacheKeyset#update}.
        '''
        value = GoogleNetworkServicesEdgeCacheKeysetTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putValidationSharedKeys")
    def put_validation_shared_keys(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys", typing.Dict[str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            def stub(
                value: typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys, typing.Dict[str, typing.Any]]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putValidationSharedKeys", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPublicKey")
    def reset_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicKey", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetValidationSharedKeys")
    def reset_validation_shared_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidationSharedKeys", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> "GoogleNetworkServicesEdgeCacheKeysetPublicKeyList":
        return typing.cast("GoogleNetworkServicesEdgeCacheKeysetPublicKeyList", jsii.get(self, "publicKey"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleNetworkServicesEdgeCacheKeysetTimeoutsOutputReference":
        return typing.cast("GoogleNetworkServicesEdgeCacheKeysetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="validationSharedKeys")
    def validation_shared_keys(
        self,
    ) -> "GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeysList":
        return typing.cast("GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeysList", jsii.get(self, "validationSharedKeys"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyInput")
    def public_key_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheKeysetPublicKey"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheKeysetPublicKey"]]], jsii.get(self, "publicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheKeysetTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheKeysetTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="validationSharedKeysInput")
    def validation_shared_keys_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys"]]], jsii.get(self, "validationSharedKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

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
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

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
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheKeyset.GoogleNetworkServicesEdgeCacheKeysetConfig",
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
        "description": "description",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "public_key": "publicKey",
        "timeouts": "timeouts",
        "validation_shared_keys": "validationSharedKeys",
    },
)
class GoogleNetworkServicesEdgeCacheKeysetConfig(cdktf.TerraformMetaArguments):
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
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        public_key: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheKeysetPublicKey", typing.Dict[str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesEdgeCacheKeysetTimeouts", typing.Dict[str, typing.Any]]] = None,
        validation_shared_keys: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys", typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource; provided by the client when the resource is created. The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#name GoogleNetworkServicesEdgeCacheKeyset#name}
        :param description: A human-readable description of the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#description GoogleNetworkServicesEdgeCacheKeyset#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#id GoogleNetworkServicesEdgeCacheKeyset#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the EdgeCache resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#labels GoogleNetworkServicesEdgeCacheKeyset#labels}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#project GoogleNetworkServicesEdgeCacheKeyset#project}.
        :param public_key: public_key block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#public_key GoogleNetworkServicesEdgeCacheKeyset#public_key}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#timeouts GoogleNetworkServicesEdgeCacheKeyset#timeouts}
        :param validation_shared_keys: validation_shared_keys block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#validation_shared_keys GoogleNetworkServicesEdgeCacheKeyset#validation_shared_keys}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkServicesEdgeCacheKeysetTimeouts(**timeouts)
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
                description: typing.Optional[builtins.str] = None,
                id: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                project: typing.Optional[builtins.str] = None,
                public_key: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheKeysetPublicKey, typing.Dict[str, typing.Any]]]]] = None,
                timeouts: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetTimeouts, typing.Dict[str, typing.Any]]] = None,
                validation_shared_keys: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys, typing.Dict[str, typing.Any]]]]] = None,
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
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument validation_shared_keys", value=validation_shared_keys, expected_type=type_hints["validation_shared_keys"])
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
        if public_key is not None:
            self._values["public_key"] = public_key
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if validation_shared_keys is not None:
            self._values["validation_shared_keys"] = validation_shared_keys

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
        '''Name of the resource;

        provided by the client when the resource is created.
        The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter,
        and all following characters must be a dash, underscore, letter or digit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#name GoogleNetworkServicesEdgeCacheKeyset#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#description GoogleNetworkServicesEdgeCacheKeyset#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#id GoogleNetworkServicesEdgeCacheKeyset#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of label tags associated with the EdgeCache resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#labels GoogleNetworkServicesEdgeCacheKeyset#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#project GoogleNetworkServicesEdgeCacheKeyset#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_key(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheKeysetPublicKey"]]]:
        '''public_key block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#public_key GoogleNetworkServicesEdgeCacheKeyset#public_key}
        '''
        result = self._values.get("public_key")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheKeysetPublicKey"]]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleNetworkServicesEdgeCacheKeysetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#timeouts GoogleNetworkServicesEdgeCacheKeyset#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkServicesEdgeCacheKeysetTimeouts"], result)

    @builtins.property
    def validation_shared_keys(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys"]]]:
        '''validation_shared_keys block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#validation_shared_keys GoogleNetworkServicesEdgeCacheKeyset#validation_shared_keys}
        '''
        result = self._values.get("validation_shared_keys")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheKeysetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheKeyset.GoogleNetworkServicesEdgeCacheKeysetPublicKey",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "managed": "managed", "value": "value"},
)
class GoogleNetworkServicesEdgeCacheKeysetPublicKey:
    def __init__(
        self,
        *,
        id: builtins.str,
        managed: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The ID of the public key. The ID must be 1-63 characters long, and comply with RFC1035. The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]* which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#id GoogleNetworkServicesEdgeCacheKeyset#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param managed: Set to true to have the CDN automatically manage this public key value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#managed GoogleNetworkServicesEdgeCacheKeyset#managed}
        :param value: The base64-encoded value of the Ed25519 public key. The base64 encoding can be padded (44 bytes) or unpadded (43 bytes). Representations or encodings of the public key other than this will be rejected with an error. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#value GoogleNetworkServicesEdgeCacheKeyset#value}
        '''
        if __debug__:
            def stub(
                *,
                id: builtins.str,
                managed: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                value: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument managed", value=managed, expected_type=type_hints["managed"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
        }
        if managed is not None:
            self._values["managed"] = managed
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def id(self) -> builtins.str:
        '''The ID of the public key.

        The ID must be 1-63 characters long, and comply with RFC1035.
        The name must be 1-64 characters long, and match the regular expression [a-zA-Z][a-zA-Z0-9_-]*
        which means the first character must be a letter, and all following characters must be a dash, underscore, letter or digit.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#id GoogleNetworkServicesEdgeCacheKeyset#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def managed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Set to true to have the CDN automatically manage this public key value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#managed GoogleNetworkServicesEdgeCacheKeyset#managed}
        '''
        result = self._values.get("managed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The base64-encoded value of the Ed25519 public key.

        The base64 encoding can be padded (44 bytes) or unpadded (43 bytes).
        Representations or encodings of the public key other than this will be rejected with an error.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#value GoogleNetworkServicesEdgeCacheKeyset#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheKeysetPublicKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheKeysetPublicKeyList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheKeyset.GoogleNetworkServicesEdgeCacheKeysetPublicKeyList",
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
    ) -> "GoogleNetworkServicesEdgeCacheKeysetPublicKeyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheKeysetPublicKeyOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheKeysetPublicKey]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheKeysetPublicKey]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheKeysetPublicKey]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheKeysetPublicKey]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GoogleNetworkServicesEdgeCacheKeysetPublicKeyOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheKeyset.GoogleNetworkServicesEdgeCacheKeysetPublicKeyOutputReference",
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

    @jsii.member(jsii_name="resetManaged")
    def reset_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManaged", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="managedInput")
    def managed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "managedInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

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
    @jsii.member(jsii_name="managed")
    def managed(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "managed"))

    @managed.setter
    def managed(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managed", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetPublicKey, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetPublicKey, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetPublicKey, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetPublicKey, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheKeyset.GoogleNetworkServicesEdgeCacheKeysetTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkServicesEdgeCacheKeysetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#create GoogleNetworkServicesEdgeCacheKeyset#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#delete GoogleNetworkServicesEdgeCacheKeyset#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#update GoogleNetworkServicesEdgeCacheKeyset#update}.
        '''
        if __debug__:
            def stub(
                *,
                create: typing.Optional[builtins.str] = None,
                delete: typing.Optional[builtins.str] = None,
                update: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#create GoogleNetworkServicesEdgeCacheKeyset#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#delete GoogleNetworkServicesEdgeCacheKeyset#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#update GoogleNetworkServicesEdgeCacheKeyset#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheKeysetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheKeysetTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheKeyset.GoogleNetworkServicesEdgeCacheKeysetTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            def stub(
                terraform_resource: cdktf.IInterpolatingParent,
                terraform_attribute: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheKeyset.GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys",
    jsii_struct_bases=[],
    name_mapping={"secret_version": "secretVersion"},
)
class GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys:
    def __init__(self, *, secret_version: builtins.str) -> None:
        '''
        :param secret_version: The name of the secret version in Secret Manager. The resource name of the secret version must be in the format 'projects/*/secrets/*/versions/*' where the '*' values are replaced by the secrets themselves. The secrets must be at least 16 bytes large. The recommended secret size depends on the signature algorithm you are using. If you are using HMAC-SHA1, we suggest 20-byte secrets. If you are using HMAC-SHA256, we suggest 32-byte secrets. See RFC 2104, Section 3 for more details on these recommendations. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#secret_version GoogleNetworkServicesEdgeCacheKeyset#secret_version}
        '''
        if __debug__:
            def stub(*, secret_version: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
        self._values: typing.Dict[str, typing.Any] = {
            "secret_version": secret_version,
        }

    @builtins.property
    def secret_version(self) -> builtins.str:
        '''The name of the secret version in Secret Manager.

        The resource name of the secret version must be in the format 'projects/*/secrets/*/versions/*' where the '*' values are replaced by the secrets themselves.
        The secrets must be at least 16 bytes large.  The recommended secret size depends on the signature algorithm you are using.
        If you are using HMAC-SHA1, we suggest 20-byte secrets.
        If you are using HMAC-SHA256, we suggest 32-byte secrets.
        See RFC 2104, Section 3 for more details on these recommendations.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_network_services_edge_cache_keyset#secret_version GoogleNetworkServicesEdgeCacheKeyset#secret_version}
        '''
        result = self._values.get("secret_version")
        assert result is not None, "Required property 'secret_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeysList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheKeyset.GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeysList",
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
    ) -> "GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            def stub(index: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeysOutputReference", jsii.invoke(self, "get", [index]))

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
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys]]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys]]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeysOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesEdgeCacheKeyset.GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeysOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="secretVersionInput")
    def secret_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVersion")
    def secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVersion"))

    @secret_version.setter
    def secret_version(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVersion", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GoogleNetworkServicesEdgeCacheKeyset",
    "GoogleNetworkServicesEdgeCacheKeysetConfig",
    "GoogleNetworkServicesEdgeCacheKeysetPublicKey",
    "GoogleNetworkServicesEdgeCacheKeysetPublicKeyList",
    "GoogleNetworkServicesEdgeCacheKeysetPublicKeyOutputReference",
    "GoogleNetworkServicesEdgeCacheKeysetTimeouts",
    "GoogleNetworkServicesEdgeCacheKeysetTimeoutsOutputReference",
    "GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeys",
    "GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeysList",
    "GoogleNetworkServicesEdgeCacheKeysetValidationSharedKeysOutputReference",
]

publication.publish()
