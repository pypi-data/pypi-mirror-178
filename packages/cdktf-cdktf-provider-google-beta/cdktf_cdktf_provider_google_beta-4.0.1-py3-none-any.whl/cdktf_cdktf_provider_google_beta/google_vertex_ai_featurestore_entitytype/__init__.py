'''
# `google_vertex_ai_featurestore_entitytype`

Refer to the Terraform Registory for docs: [`google_vertex_ai_featurestore_entitytype`](https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype).
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


class GoogleVertexAiFeaturestoreEntitytype(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytype",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype google_vertex_ai_featurestore_entitytype}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        featurestore: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        monitoring_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig", typing.Dict[str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeTimeouts", typing.Dict[str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[cdktf.SSHProvisionerConnection, typing.Dict[str, typing.Any]], typing.Union[cdktf.WinrmProvisionerConnection, typing.Dict[str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        for_each: typing.Optional[cdktf.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[cdktf.TerraformResourceLifecycle, typing.Dict[str, typing.Any]]] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[cdktf.FileProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.LocalExecProvisioner, typing.Dict[str, typing.Any]], typing.Union[cdktf.RemoteExecProvisioner, typing.Dict[str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype google_vertex_ai_featurestore_entitytype} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param featurestore: The name of the Featurestore to use, in the format projects/{project}/locations/{location}/featurestores/{featurestore}. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#featurestore GoogleVertexAiFeaturestoreEntitytype#featurestore}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#id GoogleVertexAiFeaturestoreEntitytype#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this EntityType. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#labels GoogleVertexAiFeaturestoreEntitytype#labels}
        :param monitoring_config: monitoring_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#monitoring_config GoogleVertexAiFeaturestoreEntitytype#monitoring_config}
        :param name: The name of the EntityType. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#name GoogleVertexAiFeaturestoreEntitytype#name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#timeouts GoogleVertexAiFeaturestoreEntitytype#timeouts}
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
                featurestore: builtins.str,
                id: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                monitoring_config: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig, typing.Dict[str, typing.Any]]] = None,
                name: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeTimeouts, typing.Dict[str, typing.Any]]] = None,
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
        config = GoogleVertexAiFeaturestoreEntitytypeConfig(
            featurestore=featurestore,
            id=id,
            labels=labels,
            monitoring_config=monitoring_config,
            name=name,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putMonitoringConfig")
    def put_monitoring_config(
        self,
        *,
        categorical_threshold_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig", typing.Dict[str, typing.Any]]] = None,
        import_features_analysis: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis", typing.Dict[str, typing.Any]]] = None,
        numerical_threshold_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig", typing.Dict[str, typing.Any]]] = None,
        snapshot_analysis: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param categorical_threshold_config: categorical_threshold_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#categorical_threshold_config GoogleVertexAiFeaturestoreEntitytype#categorical_threshold_config}
        :param import_features_analysis: import_features_analysis block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#import_features_analysis GoogleVertexAiFeaturestoreEntitytype#import_features_analysis}
        :param numerical_threshold_config: numerical_threshold_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#numerical_threshold_config GoogleVertexAiFeaturestoreEntitytype#numerical_threshold_config}
        :param snapshot_analysis: snapshot_analysis block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#snapshot_analysis GoogleVertexAiFeaturestoreEntitytype#snapshot_analysis}
        '''
        value = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig(
            categorical_threshold_config=categorical_threshold_config,
            import_features_analysis=import_features_analysis,
            numerical_threshold_config=numerical_threshold_config,
            snapshot_analysis=snapshot_analysis,
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoringConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#create GoogleVertexAiFeaturestoreEntitytype#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#delete GoogleVertexAiFeaturestoreEntitytype#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#update GoogleVertexAiFeaturestoreEntitytype#update}.
        '''
        value = GoogleVertexAiFeaturestoreEntitytypeTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMonitoringConfig")
    def reset_monitoring_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringConfig", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="monitoringConfig")
    def monitoring_config(
        self,
    ) -> "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference":
        return typing.cast("GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference", jsii.get(self, "monitoringConfig"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleVertexAiFeaturestoreEntitytypeTimeoutsOutputReference":
        return typing.cast("GoogleVertexAiFeaturestoreEntitytypeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="featurestoreInput")
    def featurestore_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featurestoreInput"))

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
    @jsii.member(jsii_name="monitoringConfigInput")
    def monitoring_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig"], jsii.get(self, "monitoringConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeTimeouts", cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeTimeouts", cdktf.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="featurestore")
    def featurestore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "featurestore"))

    @featurestore.setter
    def featurestore(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "featurestore", value)

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


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "featurestore": "featurestore",
        "id": "id",
        "labels": "labels",
        "monitoring_config": "monitoringConfig",
        "name": "name",
        "timeouts": "timeouts",
    },
)
class GoogleVertexAiFeaturestoreEntitytypeConfig(cdktf.TerraformMetaArguments):
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
        featurestore: builtins.str,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        monitoring_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig", typing.Dict[str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeTimeouts", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param featurestore: The name of the Featurestore to use, in the format projects/{project}/locations/{location}/featurestores/{featurestore}. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#featurestore GoogleVertexAiFeaturestoreEntitytype#featurestore}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#id GoogleVertexAiFeaturestoreEntitytype#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: A set of key/value label pairs to assign to this EntityType. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#labels GoogleVertexAiFeaturestoreEntitytype#labels}
        :param monitoring_config: monitoring_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#monitoring_config GoogleVertexAiFeaturestoreEntitytype#monitoring_config}
        :param name: The name of the EntityType. This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#name GoogleVertexAiFeaturestoreEntitytype#name}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#timeouts GoogleVertexAiFeaturestoreEntitytype#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(monitoring_config, dict):
            monitoring_config = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig(**monitoring_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleVertexAiFeaturestoreEntitytypeTimeouts(**timeouts)
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
                featurestore: builtins.str,
                id: typing.Optional[builtins.str] = None,
                labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                monitoring_config: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig, typing.Dict[str, typing.Any]]] = None,
                name: typing.Optional[builtins.str] = None,
                timeouts: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeTimeouts, typing.Dict[str, typing.Any]]] = None,
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
            check_type(argname="argument featurestore", value=featurestore, expected_type=type_hints["featurestore"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument monitoring_config", value=monitoring_config, expected_type=type_hints["monitoring_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[str, typing.Any] = {
            "featurestore": featurestore,
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
        if labels is not None:
            self._values["labels"] = labels
        if monitoring_config is not None:
            self._values["monitoring_config"] = monitoring_config
        if name is not None:
            self._values["name"] = name
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def featurestore(self) -> builtins.str:
        '''The name of the Featurestore to use, in the format projects/{project}/locations/{location}/featurestores/{featurestore}.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#featurestore GoogleVertexAiFeaturestoreEntitytype#featurestore}
        '''
        result = self._values.get("featurestore")
        assert result is not None, "Required property 'featurestore' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#id GoogleVertexAiFeaturestoreEntitytype#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A set of key/value label pairs to assign to this EntityType.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#labels GoogleVertexAiFeaturestoreEntitytype#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def monitoring_config(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig"]:
        '''monitoring_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#monitoring_config GoogleVertexAiFeaturestoreEntitytype#monitoring_config}
        '''
        result = self._values.get("monitoring_config")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the EntityType.

        This value may be up to 60 characters, and valid characters are [a-z0-9_]. The first character cannot be a number.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#name GoogleVertexAiFeaturestoreEntitytype#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#timeouts GoogleVertexAiFeaturestoreEntitytype#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig",
    jsii_struct_bases=[],
    name_mapping={
        "categorical_threshold_config": "categoricalThresholdConfig",
        "import_features_analysis": "importFeaturesAnalysis",
        "numerical_threshold_config": "numericalThresholdConfig",
        "snapshot_analysis": "snapshotAnalysis",
    },
)
class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig:
    def __init__(
        self,
        *,
        categorical_threshold_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig", typing.Dict[str, typing.Any]]] = None,
        import_features_analysis: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis", typing.Dict[str, typing.Any]]] = None,
        numerical_threshold_config: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig", typing.Dict[str, typing.Any]]] = None,
        snapshot_analysis: typing.Optional[typing.Union["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param categorical_threshold_config: categorical_threshold_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#categorical_threshold_config GoogleVertexAiFeaturestoreEntitytype#categorical_threshold_config}
        :param import_features_analysis: import_features_analysis block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#import_features_analysis GoogleVertexAiFeaturestoreEntitytype#import_features_analysis}
        :param numerical_threshold_config: numerical_threshold_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#numerical_threshold_config GoogleVertexAiFeaturestoreEntitytype#numerical_threshold_config}
        :param snapshot_analysis: snapshot_analysis block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#snapshot_analysis GoogleVertexAiFeaturestoreEntitytype#snapshot_analysis}
        '''
        if isinstance(categorical_threshold_config, dict):
            categorical_threshold_config = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig(**categorical_threshold_config)
        if isinstance(import_features_analysis, dict):
            import_features_analysis = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis(**import_features_analysis)
        if isinstance(numerical_threshold_config, dict):
            numerical_threshold_config = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig(**numerical_threshold_config)
        if isinstance(snapshot_analysis, dict):
            snapshot_analysis = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis(**snapshot_analysis)
        if __debug__:
            def stub(
                *,
                categorical_threshold_config: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig, typing.Dict[str, typing.Any]]] = None,
                import_features_analysis: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis, typing.Dict[str, typing.Any]]] = None,
                numerical_threshold_config: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig, typing.Dict[str, typing.Any]]] = None,
                snapshot_analysis: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument categorical_threshold_config", value=categorical_threshold_config, expected_type=type_hints["categorical_threshold_config"])
            check_type(argname="argument import_features_analysis", value=import_features_analysis, expected_type=type_hints["import_features_analysis"])
            check_type(argname="argument numerical_threshold_config", value=numerical_threshold_config, expected_type=type_hints["numerical_threshold_config"])
            check_type(argname="argument snapshot_analysis", value=snapshot_analysis, expected_type=type_hints["snapshot_analysis"])
        self._values: typing.Dict[str, typing.Any] = {}
        if categorical_threshold_config is not None:
            self._values["categorical_threshold_config"] = categorical_threshold_config
        if import_features_analysis is not None:
            self._values["import_features_analysis"] = import_features_analysis
        if numerical_threshold_config is not None:
            self._values["numerical_threshold_config"] = numerical_threshold_config
        if snapshot_analysis is not None:
            self._values["snapshot_analysis"] = snapshot_analysis

    @builtins.property
    def categorical_threshold_config(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig"]:
        '''categorical_threshold_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#categorical_threshold_config GoogleVertexAiFeaturestoreEntitytype#categorical_threshold_config}
        '''
        result = self._values.get("categorical_threshold_config")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig"], result)

    @builtins.property
    def import_features_analysis(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis"]:
        '''import_features_analysis block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#import_features_analysis GoogleVertexAiFeaturestoreEntitytype#import_features_analysis}
        '''
        result = self._values.get("import_features_analysis")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis"], result)

    @builtins.property
    def numerical_threshold_config(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig"]:
        '''numerical_threshold_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#numerical_threshold_config GoogleVertexAiFeaturestoreEntitytype#numerical_threshold_config}
        '''
        result = self._values.get("numerical_threshold_config")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig"], result)

    @builtins.property
    def snapshot_analysis(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"]:
        '''snapshot_analysis block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#snapshot_analysis GoogleVertexAiFeaturestoreEntitytype#snapshot_analysis}
        '''
        result = self._values.get("snapshot_analysis")
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig:
    def __init__(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For categorical feature, the distribution distance is calculated by L-inifinity norm. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        if __debug__:
            def stub(*, value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[str, typing.Any] = {
            "value": value,
        }

    @builtins.property
    def value(self) -> jsii.Number:
        '''Specify a threshold value that can trigger the alert.

        For categorical feature, the distribution distance is calculated by L-inifinity norm. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis",
    jsii_struct_bases=[],
    name_mapping={
        "anomaly_detection_baseline": "anomalyDetectionBaseline",
        "state": "state",
    },
)
class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis:
    def __init__(
        self,
        *,
        anomaly_detection_baseline: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param anomaly_detection_baseline: Defines the baseline to do anomaly detection for feature values imported by each [entityTypes.importFeatureValues][] operation. The value must be one of the values below: LATEST_STATS: Choose the later one statistics generated by either most recent snapshot analysis or previous import features analysis. If non of them exists, skip anomaly detection and only generate a statistics. MOST_RECENT_SNAPSHOT_STATS: Use the statistics generated by the most recent snapshot analysis if exists. PREVIOUS_IMPORT_FEATURES_STATS: Use the statistics generated by the previous import features analysis if exists. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#anomaly_detection_baseline GoogleVertexAiFeaturestoreEntitytype#anomaly_detection_baseline}
        :param state: Whether to enable / disable / inherite default hebavior for import features analysis. The value must be one of the values below: DEFAULT: The default behavior of whether to enable the monitoring. EntityType-level config: disabled. ENABLED: Explicitly enables import features analysis. EntityType-level config: by default enables import features analysis for all Features under it. DISABLED: Explicitly disables import features analysis. EntityType-level config: by default disables import features analysis for all Features under it. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#state GoogleVertexAiFeaturestoreEntitytype#state}
        '''
        if __debug__:
            def stub(
                *,
                anomaly_detection_baseline: typing.Optional[builtins.str] = None,
                state: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument anomaly_detection_baseline", value=anomaly_detection_baseline, expected_type=type_hints["anomaly_detection_baseline"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[str, typing.Any] = {}
        if anomaly_detection_baseline is not None:
            self._values["anomaly_detection_baseline"] = anomaly_detection_baseline
        if state is not None:
            self._values["state"] = state

    @builtins.property
    def anomaly_detection_baseline(self) -> typing.Optional[builtins.str]:
        '''Defines the baseline to do anomaly detection for feature values imported by each [entityTypes.importFeatureValues][] operation. The value must be one of the values below: LATEST_STATS: Choose the later one statistics generated by either most recent snapshot analysis or previous import features analysis. If non of them exists, skip anomaly detection and only generate a statistics. MOST_RECENT_SNAPSHOT_STATS: Use the statistics generated by the most recent snapshot analysis if exists. PREVIOUS_IMPORT_FEATURES_STATS: Use the statistics generated by the previous import features analysis if exists.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#anomaly_detection_baseline GoogleVertexAiFeaturestoreEntitytype#anomaly_detection_baseline}
        '''
        result = self._values.get("anomaly_detection_baseline")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Whether to enable / disable / inherite default hebavior for import features analysis.

        The value must be one of the values below:
        DEFAULT: The default behavior of whether to enable the monitoring. EntityType-level config: disabled.
        ENABLED: Explicitly enables import features analysis. EntityType-level config: by default enables import features analysis for all Features under it.
        DISABLED: Explicitly disables import features analysis. EntityType-level config: by default disables import features analysis for all Features under it.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#state GoogleVertexAiFeaturestoreEntitytype#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference",
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

    @jsii.member(jsii_name="resetAnomalyDetectionBaseline")
    def reset_anomaly_detection_baseline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnomalyDetectionBaseline", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @builtins.property
    @jsii.member(jsii_name="anomalyDetectionBaselineInput")
    def anomaly_detection_baseline_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "anomalyDetectionBaselineInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="anomalyDetectionBaseline")
    def anomaly_detection_baseline(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "anomalyDetectionBaseline"))

    @anomaly_detection_baseline.setter
    def anomaly_detection_baseline(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anomalyDetectionBaseline", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig:
    def __init__(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For numerical feature, the distribution distance is calculated by Jensen–Shannon divergence. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        if __debug__:
            def stub(*, value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[str, typing.Any] = {
            "value": value,
        }

    @builtins.property
    def value(self) -> jsii.Number:
        '''Specify a threshold value that can trigger the alert.

        For numerical feature, the distribution distance is calculated by Jensen–Shannon divergence. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference",
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

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference",
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

    @jsii.member(jsii_name="putCategoricalThresholdConfig")
    def put_categorical_threshold_config(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For categorical feature, the distribution distance is calculated by L-inifinity norm. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        value_ = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig(
            value=value
        )

        return typing.cast(None, jsii.invoke(self, "putCategoricalThresholdConfig", [value_]))

    @jsii.member(jsii_name="putImportFeaturesAnalysis")
    def put_import_features_analysis(
        self,
        *,
        anomaly_detection_baseline: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param anomaly_detection_baseline: Defines the baseline to do anomaly detection for feature values imported by each [entityTypes.importFeatureValues][] operation. The value must be one of the values below: LATEST_STATS: Choose the later one statistics generated by either most recent snapshot analysis or previous import features analysis. If non of them exists, skip anomaly detection and only generate a statistics. MOST_RECENT_SNAPSHOT_STATS: Use the statistics generated by the most recent snapshot analysis if exists. PREVIOUS_IMPORT_FEATURES_STATS: Use the statistics generated by the previous import features analysis if exists. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#anomaly_detection_baseline GoogleVertexAiFeaturestoreEntitytype#anomaly_detection_baseline}
        :param state: Whether to enable / disable / inherite default hebavior for import features analysis. The value must be one of the values below: DEFAULT: The default behavior of whether to enable the monitoring. EntityType-level config: disabled. ENABLED: Explicitly enables import features analysis. EntityType-level config: by default enables import features analysis for all Features under it. DISABLED: Explicitly disables import features analysis. EntityType-level config: by default disables import features analysis for all Features under it. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#state GoogleVertexAiFeaturestoreEntitytype#state}
        '''
        value = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis(
            anomaly_detection_baseline=anomaly_detection_baseline, state=state
        )

        return typing.cast(None, jsii.invoke(self, "putImportFeaturesAnalysis", [value]))

    @jsii.member(jsii_name="putNumericalThresholdConfig")
    def put_numerical_threshold_config(self, *, value: jsii.Number) -> None:
        '''
        :param value: Specify a threshold value that can trigger the alert. For numerical feature, the distribution distance is calculated by Jensen–Shannon divergence. Each feature must have a non-zero threshold if they need to be monitored. Otherwise no alert will be triggered for that feature. The default value is 0.3. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#value GoogleVertexAiFeaturestoreEntitytype#value}
        '''
        value_ = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig(
            value=value
        )

        return typing.cast(None, jsii.invoke(self, "putNumericalThresholdConfig", [value_]))

    @jsii.member(jsii_name="putSnapshotAnalysis")
    def put_snapshot_analysis(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        monitoring_interval: typing.Optional[builtins.str] = None,
        monitoring_interval_days: typing.Optional[jsii.Number] = None,
        staleness_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disabled: The monitoring schedule for snapshot analysis. For EntityType-level config: unset / disabled = true indicates disabled by default for Features under it; otherwise by default enable snapshot analysis monitoring with monitoringInterval for Features under it. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#disabled GoogleVertexAiFeaturestoreEntitytype#disabled}
        :param monitoring_interval: Configuration of the snapshot analysis based monitoring pipeline running interval. The value is rolled up to full day. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#monitoring_interval GoogleVertexAiFeaturestoreEntitytype#monitoring_interval}
        :param monitoring_interval_days: Configuration of the snapshot analysis based monitoring pipeline running interval. The value indicates number of days. The default value is 1. If both FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days and [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval][] are set when creating/updating EntityTypes/Features, FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days will be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#monitoring_interval_days GoogleVertexAiFeaturestoreEntitytype#monitoring_interval_days}
        :param staleness_days: Customized export features time window for snapshot analysis. Unit is one day. The default value is 21 days. Minimum value is 1 day. Maximum value is 4000 days. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#staleness_days GoogleVertexAiFeaturestoreEntitytype#staleness_days}
        '''
        value = GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis(
            disabled=disabled,
            monitoring_interval=monitoring_interval,
            monitoring_interval_days=monitoring_interval_days,
            staleness_days=staleness_days,
        )

        return typing.cast(None, jsii.invoke(self, "putSnapshotAnalysis", [value]))

    @jsii.member(jsii_name="resetCategoricalThresholdConfig")
    def reset_categorical_threshold_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategoricalThresholdConfig", []))

    @jsii.member(jsii_name="resetImportFeaturesAnalysis")
    def reset_import_features_analysis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportFeaturesAnalysis", []))

    @jsii.member(jsii_name="resetNumericalThresholdConfig")
    def reset_numerical_threshold_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumericalThresholdConfig", []))

    @jsii.member(jsii_name="resetSnapshotAnalysis")
    def reset_snapshot_analysis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotAnalysis", []))

    @builtins.property
    @jsii.member(jsii_name="categoricalThresholdConfig")
    def categorical_threshold_config(
        self,
    ) -> GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference:
        return typing.cast(GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference, jsii.get(self, "categoricalThresholdConfig"))

    @builtins.property
    @jsii.member(jsii_name="importFeaturesAnalysis")
    def import_features_analysis(
        self,
    ) -> GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference:
        return typing.cast(GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference, jsii.get(self, "importFeaturesAnalysis"))

    @builtins.property
    @jsii.member(jsii_name="numericalThresholdConfig")
    def numerical_threshold_config(
        self,
    ) -> GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference:
        return typing.cast(GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference, jsii.get(self, "numericalThresholdConfig"))

    @builtins.property
    @jsii.member(jsii_name="snapshotAnalysis")
    def snapshot_analysis(
        self,
    ) -> "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference":
        return typing.cast("GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference", jsii.get(self, "snapshotAnalysis"))

    @builtins.property
    @jsii.member(jsii_name="categoricalThresholdConfigInput")
    def categorical_threshold_config_input(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig], jsii.get(self, "categoricalThresholdConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="importFeaturesAnalysisInput")
    def import_features_analysis_input(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis], jsii.get(self, "importFeaturesAnalysisInput"))

    @builtins.property
    @jsii.member(jsii_name="numericalThresholdConfigInput")
    def numerical_threshold_config_input(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig], jsii.get(self, "numericalThresholdConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotAnalysisInput")
    def snapshot_analysis_input(
        self,
    ) -> typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"]:
        return typing.cast(typing.Optional["GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis"], jsii.get(self, "snapshotAnalysisInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis",
    jsii_struct_bases=[],
    name_mapping={
        "disabled": "disabled",
        "monitoring_interval": "monitoringInterval",
        "monitoring_interval_days": "monitoringIntervalDays",
        "staleness_days": "stalenessDays",
    },
)
class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis:
    def __init__(
        self,
        *,
        disabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        monitoring_interval: typing.Optional[builtins.str] = None,
        monitoring_interval_days: typing.Optional[jsii.Number] = None,
        staleness_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disabled: The monitoring schedule for snapshot analysis. For EntityType-level config: unset / disabled = true indicates disabled by default for Features under it; otherwise by default enable snapshot analysis monitoring with monitoringInterval for Features under it. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#disabled GoogleVertexAiFeaturestoreEntitytype#disabled}
        :param monitoring_interval: Configuration of the snapshot analysis based monitoring pipeline running interval. The value is rolled up to full day. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#monitoring_interval GoogleVertexAiFeaturestoreEntitytype#monitoring_interval}
        :param monitoring_interval_days: Configuration of the snapshot analysis based monitoring pipeline running interval. The value indicates number of days. The default value is 1. If both FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days and [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval][] are set when creating/updating EntityTypes/Features, FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days will be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#monitoring_interval_days GoogleVertexAiFeaturestoreEntitytype#monitoring_interval_days}
        :param staleness_days: Customized export features time window for snapshot analysis. Unit is one day. The default value is 21 days. Minimum value is 1 day. Maximum value is 4000 days. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#staleness_days GoogleVertexAiFeaturestoreEntitytype#staleness_days}
        '''
        if __debug__:
            def stub(
                *,
                disabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
                monitoring_interval: typing.Optional[builtins.str] = None,
                monitoring_interval_days: typing.Optional[jsii.Number] = None,
                staleness_days: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument monitoring_interval", value=monitoring_interval, expected_type=type_hints["monitoring_interval"])
            check_type(argname="argument monitoring_interval_days", value=monitoring_interval_days, expected_type=type_hints["monitoring_interval_days"])
            check_type(argname="argument staleness_days", value=staleness_days, expected_type=type_hints["staleness_days"])
        self._values: typing.Dict[str, typing.Any] = {}
        if disabled is not None:
            self._values["disabled"] = disabled
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_interval_days is not None:
            self._values["monitoring_interval_days"] = monitoring_interval_days
        if staleness_days is not None:
            self._values["staleness_days"] = staleness_days

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''The monitoring schedule for snapshot analysis.

        For EntityType-level config: unset / disabled = true indicates disabled by default for Features under it; otherwise by default enable snapshot analysis monitoring with monitoringInterval for Features under it.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#disabled GoogleVertexAiFeaturestoreEntitytype#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[builtins.str]:
        '''Configuration of the snapshot analysis based monitoring pipeline running interval. The value is rolled up to full day.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#monitoring_interval GoogleVertexAiFeaturestoreEntitytype#monitoring_interval}
        '''
        result = self._values.get("monitoring_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitoring_interval_days(self) -> typing.Optional[jsii.Number]:
        '''Configuration of the snapshot analysis based monitoring pipeline running interval.

        The value indicates number of days. The default value is 1.
        If both FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days and [FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval][] are set when creating/updating EntityTypes/Features, FeaturestoreMonitoringConfig.SnapshotAnalysis.monitoring_interval_days will be used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#monitoring_interval_days GoogleVertexAiFeaturestoreEntitytype#monitoring_interval_days}
        '''
        result = self._values.get("monitoring_interval_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def staleness_days(self) -> typing.Optional[jsii.Number]:
        '''Customized export features time window for snapshot analysis.

        Unit is one day. The default value is 21 days. Minimum value is 1 day. Maximum value is 4000 days.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#staleness_days GoogleVertexAiFeaturestoreEntitytype#staleness_days}
        '''
        result = self._values.get("staleness_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference",
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

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetMonitoringInterval")
    def reset_monitoring_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringInterval", []))

    @jsii.member(jsii_name="resetMonitoringIntervalDays")
    def reset_monitoring_interval_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoringIntervalDays", []))

    @jsii.member(jsii_name="resetStalenessDays")
    def reset_staleness_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStalenessDays", []))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringIntervalDaysInput")
    def monitoring_interval_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monitoringIntervalDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringIntervalInput")
    def monitoring_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitoringIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="stalenessDaysInput")
    def staleness_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "stalenessDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        if __debug__:
            def stub(value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value)

    @builtins.property
    @jsii.member(jsii_name="monitoringInterval")
    def monitoring_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitoringInterval"))

    @monitoring_interval.setter
    def monitoring_interval(self, value: builtins.str) -> None:
        if __debug__:
            def stub(value: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitoringInterval", value)

    @builtins.property
    @jsii.member(jsii_name="monitoringIntervalDays")
    def monitoring_interval_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "monitoringIntervalDays"))

    @monitoring_interval_days.setter
    def monitoring_interval_days(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitoringIntervalDays", value)

    @builtins.property
    @jsii.member(jsii_name="stalenessDays")
    def staleness_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stalenessDays"))

    @staleness_days.setter
    def staleness_days(self, value: jsii.Number) -> None:
        if __debug__:
            def stub(value: jsii.Number) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stalenessDays", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis]:
        return typing.cast(typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleVertexAiFeaturestoreEntitytypeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#create GoogleVertexAiFeaturestoreEntitytype#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#delete GoogleVertexAiFeaturestoreEntitytype#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#update GoogleVertexAiFeaturestoreEntitytype#update}.
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#create GoogleVertexAiFeaturestoreEntitytype#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#delete GoogleVertexAiFeaturestoreEntitytype#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/r/google_vertex_ai_featurestore_entitytype#update GoogleVertexAiFeaturestoreEntitytype#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiFeaturestoreEntitytypeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiFeaturestoreEntitytypeTimeoutsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiFeaturestoreEntitytype.GoogleVertexAiFeaturestoreEntitytypeTimeoutsOutputReference",
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
    ) -> typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeTimeouts, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeTimeouts, cdktf.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeTimeouts, cdktf.IResolvable]],
    ) -> None:
        if __debug__:
            def stub(
                value: typing.Optional[typing.Union[GoogleVertexAiFeaturestoreEntitytypeTimeouts, cdktf.IResolvable]],
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GoogleVertexAiFeaturestoreEntitytype",
    "GoogleVertexAiFeaturestoreEntitytypeConfig",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfig",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfig",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigCategoricalThresholdConfigOutputReference",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysis",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigImportFeaturesAnalysisOutputReference",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfig",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigNumericalThresholdConfigOutputReference",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigOutputReference",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysis",
    "GoogleVertexAiFeaturestoreEntitytypeMonitoringConfigSnapshotAnalysisOutputReference",
    "GoogleVertexAiFeaturestoreEntitytypeTimeouts",
    "GoogleVertexAiFeaturestoreEntitytypeTimeoutsOutputReference",
]

publication.publish()
