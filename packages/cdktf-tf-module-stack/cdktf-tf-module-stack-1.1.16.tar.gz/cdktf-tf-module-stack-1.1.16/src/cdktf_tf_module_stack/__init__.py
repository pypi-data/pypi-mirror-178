'''
# cdktf-tf-module-stack

A drop-in replacement for cdktf.TerraformStack that let's you define Terraform modules as construct.

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/tf-module-stack](https://www.npmjs.com/package/@cdktf/tf-module-stack).

`npm install @cdktf/tf-module-stack`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-tf-module-stack](https://pypi.org/project/cdktf-tf-module-stack).

`pipenv install cdktf-tf-module-stack`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.TfModuleStack](https://www.nuget.org/packages/HashiCorp.Cdktf.TfModuleStack).

`dotnet add package HashiCorp.Cdktf.TfModuleStack`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-tf-module-stack](https://mvnrepository.com/artifact/com.hashicorp/cdktf-tf-module-stack).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-tf-module-stack</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-tf-module-stack-go`](https://github.com/cdktf/cdktf-tf-module-stack-go) package.

`go get github.com/cdktf/cdktf-tf-module-stack-go/tfmodulestack`

## Usage

### Typescript

```python
import { App } from "cdktf";
import {
  TFModuleStack,
  TFModuleVariable,
  TFModuleOutput,
  ProviderRequirement,
} from "cdktf-tf-module-stack";
import { Resource } from "@cdktf/provider-null";

class MyAwesomeModule extends TFModuleStack {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    new ProviderRequirement(this, "null", "~> 2.0");
    const resource = new Resource(this, "resource");

    new TFModuleVariable(this, "my_var", {
      type: "string",
      description: "A variable",
      default: "default",
    });

    new TFModuleOutput(this, "my_output", {
      value: resource.id,
    });
  }
}

const app = new App();
new MyAwesomeModule(app, "my-awesome-module");
app.synth();
```

### Python

```python
from constructs import Construct
from cdktf import App, TerraformStack
from imports.null.resource import Resource
from cdktf_tf_module_stack import TFModuleStack, TFModuleVariable, TFModuleOutput, ProviderRequirement


class MyAwesomeModule(TFModuleStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        ProviderRequirement(self, "null", provider_version_constraint="~> 2.0")

        TFModuleVariable(self, "my_var", type="string", description="A variable", default="default")

        resource = Resource(self, "resource")

        TFModuleOutput(self, "my_output", value=resource.id)


app = App()
MyAwesomeModule(app, "my-awesome-module")
app.synth()
```

This will synthesize a Terraform JSON file that looks like this:

```json
{
  "output": {
    "my_output": [
      {
        "value": "${null_resource.resource.id}"
      }
    ]
  },
  "resource": {
    "null_resource": {
      "resource": {}
    }
  },
  "terraform": {
    "required_providers": {
      "null": {
        "source": "null",
        "version": "~> 2.0"
      }
    },
    "variable": {
      "my_var": {
        "default": "default",
        "description": "A variable",
        "type": "string"
      }
    }
  }
}
```

Please note that the provider section is missing, so that the Terraform Workspace using the generated module can be used with any provider matching the version.
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

from ._jsii import *

import cdktf
import constructs


class ProviderRequirement(
    cdktf.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/tf-module-stack.ProviderRequirement",
):
    def __init__(
        self,
        scope: constructs.Construct,
        provider_name: builtins.str,
        provider_version_constraint: typing.Optional[builtins.str] = None,
        terraform_provider_source: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param provider_name: -
        :param provider_version_constraint: -
        :param terraform_provider_source: -
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                provider_name: builtins.str,
                provider_version_constraint: typing.Optional[builtins.str] = None,
                terraform_provider_source: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument provider_version_constraint", value=provider_version_constraint, expected_type=type_hints["provider_version_constraint"])
            check_type(argname="argument terraform_provider_source", value=terraform_provider_source, expected_type=type_hints["terraform_provider_source"])
        jsii.create(self.__class__, self, [scope, provider_name, provider_version_constraint, terraform_provider_source])


class TFModuleApp(
    cdktf.App,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/tf-module-stack.TFModuleApp",
):
    def __init__(
        self,
        *,
        context: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        outdir: typing.Optional[builtins.str] = None,
        skip_validation: typing.Optional[builtins.bool] = None,
        stack_traces: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param context: (experimental) Additional context values for the application. Context set by the CLI or the ``context`` key in ``cdktf.json`` has precedence. Context can be read from any construct using ``node.getContext(key)``. Default: - no additional context
        :param outdir: (experimental) The directory to output Terraform resources. Default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"
        :param skip_validation: (experimental) Whether to skip the validation during synthesis of the app. Default: - false
        :param stack_traces: 
        '''
        options = cdktf.AppOptions(
            context=context,
            outdir=outdir,
            skip_validation=skip_validation,
            stack_traces=stack_traces,
        )

        jsii.create(self.__class__, self, [options])


class TFModuleOutput(
    cdktf.TerraformOutput,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/tf-module-stack.TFModuleOutput",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        value: typing.Any,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        description: typing.Optional[builtins.str] = None,
        sensitive: typing.Optional[builtins.bool] = None,
        static_id: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param value: 
        :param depends_on: 
        :param description: 
        :param sensitive: 
        :param static_id: (experimental) If set to true the synthesized Terraform Output will be named after the ``id`` passed to the constructor instead of the default (TerraformOutput.friendlyUniqueId). Default: false
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                name: builtins.str,
                *,
                value: typing.Any,
                depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
                description: typing.Optional[builtins.str] = None,
                sensitive: typing.Optional[builtins.bool] = None,
                static_id: typing.Optional[builtins.bool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        config = cdktf.TerraformOutputConfig(
            value=value,
            depends_on=depends_on,
            description=description,
            sensitive=sensitive,
            static_id=static_id,
        )

        jsii.create(self.__class__, self, [scope, name, config])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))


class TFModuleStack(
    cdktf.TerraformStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/tf-module-stack.TFModuleStack",
):
    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            def stub(scope: constructs.Construct, id: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))


class TFModuleVariable(
    cdktf.TerraformVariable,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/tf-module-stack.TFModuleVariable",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        default: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[builtins.bool] = None,
        sensitive: typing.Optional[builtins.bool] = None,
        type: typing.Optional[builtins.str] = None,
        validation: typing.Optional[typing.Sequence[typing.Union[cdktf.TerraformVariableValidationConfig, typing.Dict[str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param default: 
        :param description: 
        :param nullable: 
        :param sensitive: 
        :param type: (experimental) The type argument in a variable block allows you to restrict the type of value that will be accepted as the value for a variable. If no type constraint is set then a value of any type is accepted. While type constraints are optional, we recommend specifying them; they serve as easy reminders for users of the module, and allow Terraform to return a helpful error message if the wrong type is used. Type constraints are created from a mixture of type keywords and type constructors. The supported type keywords are: - string - number - bool The type constructors allow you to specify complex types such as collections: - list(<TYPE>) - set(<TYPE>) - map(<TYPE>) - object({<ATTR NAME> = <TYPE>, ... }) - tuple([<TYPE>, ...]) The keyword any may be used to indicate that any type is acceptable. For more information on the meaning and behavior of these different types, as well as detailed information about automatic conversion of complex types, see {@link https://www.terraform.io/docs/configuration/types.html|Type Constraints}. If both the type and default arguments are specified, the given default value must be convertible to the specified type.
        :param validation: (experimental) Specify arbitrary custom validation rules for a particular variable using a validation block nested within the corresponding variable block.
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                name: builtins.str,
                *,
                default: typing.Any = None,
                description: typing.Optional[builtins.str] = None,
                nullable: typing.Optional[builtins.bool] = None,
                sensitive: typing.Optional[builtins.bool] = None,
                type: typing.Optional[builtins.str] = None,
                validation: typing.Optional[typing.Sequence[typing.Union[cdktf.TerraformVariableValidationConfig, typing.Dict[str, typing.Any]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        config = cdktf.TerraformVariableConfig(
            default=default,
            description=description,
            nullable=nullable,
            sensitive=sensitive,
            type=type,
            validation=validation,
        )

        jsii.create(self.__class__, self, [scope, name, config])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.invoke(self, "toTerraform", []))


__all__ = [
    "ProviderRequirement",
    "TFModuleApp",
    "TFModuleOutput",
    "TFModuleStack",
    "TFModuleVariable",
]

publication.publish()
