'''
<!--
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
-->

# CDK Enterprise IaC

Utilities for using CDK within enterprise constraints

## Install

Typescript

```zsh
npm install @cdklabs/cdk-enterprise-iac
```

Python

```zsh
pip install cdklabs.cdk-enterprise-iac
```

## Usage

There are many tools available, all detailed in [`API.md`](./API.md).

A few examples of these tools below

### Resource extraction

:warning: Resource extraction is in an experimental phase. Test and validate before using in production. Please open any issues found [here](https://github.com/cdklabs/cdk-enterprise-iac/)

In many enterprises, there are separate teams with different IAM permissions than developers deploying CDK applications.

For example there might be a networking team with permissions to deploy `AWS::EC2::SecurityGroup` and `AWS::EC2::EIP`, or a security team with permissions to deploy `AWS::IAM::Role` and `AWS::IAM::Policy`, but the developers deploying the CDK don't have those permissions

When a developer doesn't have permissions to deploy necessary resources in their CDK application, writing good code becomes difficult to manage when a cdk deploy will quickly error due to not being able to deploy something like an `AWS::IAM::Role` which is foundational to any project deployed into AWS.

Using the `ResourceExtractor` Aspect, developers can write their CDK code as though they had sufficient IAM permissions, but extract those resources into a separate stack for an external team to deploy on their behalf.

Take the following example stack

```python
import { App, Aspects, RemovalPolicy, Stack } from 'aws-cdk-lib';
import { Code, Function, Runtime } from 'aws-cdk-lib/aws-lambda';
import { Bucket } from 'aws-cdk-lib/aws-s3';

const app = new App();
const appStack = new Stack(app, 'MyAppStack');

const func = new Function(appStack, 'TestLambda', {
  code: Code.fromAsset(path.join(__dirname, 'lambda-handler')),
  handler: 'index.handler',
  runtime: Runtime.PYTHON_3_9,
});
const bucket = new Bucket(appStack, 'TestBucket', {
  autoDeleteObjects: true,
  removalPolicy: RemovalPolicy.DESTROY,
});
bucket.grantReadWrite(func);

app.synth()
```

The synthesized Cloudformation would include *all* AWS resources required, including resources a developer might not have permissions to deploy

The above example would include the following snippet in the synthesized Cloudformation

```yaml
TestLambdaServiceRoleC28C2D9C:
  Type: 'AWS::IAM::Role'
  Properties:
    AssumeRolePolicyDocument:
      Statement:
        - Action: 'sts:AssumeRole'
          Effect: Allow
          Principal:
            Service: lambda.amazonaws.com
      Version: 2012-10-17
    # excluding remaining properties
  TestLambda2F70C45E:
    Type: 'AWS::Lambda::Function'
    Properties:
      Role: !GetAtt
        - TestLambdaServiceRoleC28C2D9C
        - Arn
      # excluding remaining properties
```

While including `bucket.grantReadWrite(func)` in the CDK application ensures an IAM role with least privilege IAM policies for the application, the creation of IAM resources such as Roles and Policies may be restricted to a security team, resulting in the synthesized Cloudformation template not being deployable by a developer.

Using the `ResourceExtractor`, we can pull out an arbitrary list of Cloudformation resources that a developer *doesn't* have permissions to provision, and create a separate stack that can be sent to a security team.

```python
import { App, Aspects, RemovalPolicy, Stack } from 'aws-cdk-lib';
import { Code, Function, Runtime } from 'aws-cdk-lib/aws-lambda';
import { Bucket } from 'aws-cdk-lib/aws-s3';
// Import ResourceExtractor
import { ResourceExtractor } from '@cdklabs/cdk-enterprise-iac';

const app = new App();
const appStack = new Stack(app, 'MyAppStack');
// Set up a destination stack to extract resources to
const extractedStack = new Stack(app, 'ExtractedStack');

const func = new Function(appStack, 'TestLambda', {
  code: Code.fromAsset(path.join(__dirname, 'lambda-handler')),
  handler: 'index.handler',
  runtime: Runtime.PYTHON_3_9,
});
const bucket = new Bucket(appStack, 'TestBucket', {
  autoDeleteObjects: true,
  removalPolicy: RemovalPolicy.DESTROY,
});
bucket.grantReadWrite(func);

// Capture the output of app.synth()
const synthedApp = app.synth();
// Apply the ResourceExtractor Aspect
Aspects.of(app).add(
  new ResourceExtractor({
    // synthesized stacks to examine
    stackArtifacts: synthedApp.stacks,
    // Array of Cloudformation resources to extract
    resourceTypesToExtract: [
      'AWS::IAM::Role',
      'AWS::IAM::Policy',
      'AWS::IAM::ManagedPolicy',
      'AWS::IAM::InstanceProfile',
    ],
    // Destination stack for extracted resources
    extractDestinationStack: extractedStack,
  })
);
// Resynthing since ResourceExtractor has modified the app
app.synth({ force: true });
```

In the example above, *all* resources are created in the `appStack`, and an empty `extractedStack` is also created.

We apply the `ResourceExtractor` Aspect, specifying the Cloudformation resource types the developer is unable to deploy due to insufficient IAM permissions.

Now when we list stacks in the CDK project, we can see an added stack

```zsh
$ cdk ls
MyAppStack
ExtractedStack
```

Taking a look at these synthesized stacks, in the `ExtractedStack` we'll find:

```yaml
Resources:
  TestLambdaServiceRoleC28C2D9C:
    Type: 'AWS::IAM::Role'
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Action: 'sts:AssumeRole'
            Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
        Version: 2012-10-17
      # excluding remaining properties
Outputs:
  ExportAppStackTestLambdaServiceRoleC28C2D9C:
    Value:
      'Fn::GetAtt':
        - TestLambdaServiceRoleC28C2D9C
        - Arn
    Export:
      Name: 'AppStack:TestLambdaServiceRoleC28C2D9C'  # Exported name
```

And inside the synthesized `MyAppStack` template:

```yaml
Resources:
  TestLambda2F70C45E:
    Type: 'AWS::Lambda::Function'
    Properties:
      Role: !ImportValue 'AppStack:TestLambdaServiceRoleC28C2D9C'  # Using ImportValue instrinsic function to use pre-created IAM role
      # excluding remaining properties
```

In this scenario, a developer is able to provide an external security team with sufficient IAM privileges to deploy the `ExtractedStack`.

Once deployed, a developer can run `cdk deploy MyAppStack` without errors due to insufficient IAM privileges

#### Value Sharing methods

When resources are extracted from a stack, there must be a method to reference the resources that have been extracted.

There are three methods (see `ResourceExtractorShareMethod` enum)

* `CFN_OUTPUT`
* `SSM_PARAMETER`
* `API_LOOKUP`

##### `CFN_OUTPUT`

The default sharing method is `CFN_OUTPUT`, which uses Cloudformation Export/Import to Export values in the extracted stack (see [Outputs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html)), and use the [Fn::ImportValue](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-importvalue.html) intrinsic function to reference those values.

This works fine, but some teams may prefer a looser coupling between the extracted stack deployed by an external team and the rest of the CDK infrastructure.

##### `SSM_PARAMETER`

In this method, the extracted stack generates Parameters in AWS Systems Manager Parameter Store, and modifies the CDK application to look up the generated parameter using [`aws_ssm.StringParameter.valueFromLookup()`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ssm.StringParameter.html#static-valuewbrfromwbrlookupscope-parametername) at synthesis time.

Example on using this method:

```python
import { ResourceExtractor, ResourceExtractorShareMethod } from '@cdklabs/cdk-enterprise-iac';

Aspects.of(app).add(
  new ResourceExtractor({
    stackArtifacts: synthedApp.stacks,
    resourceTypesToExtract: [
      'AWS::IAM::Role',
      'AWS::IAM::Policy',
      'AWS::IAM::ManagedPolicy',
      'AWS::IAM::InstanceProfile',
    ],
    extractDestinationStack: extractedStack,
    valueShareMethod: ResourceExtractorShareMethod.SSM_PARAMETER,  // Specify SSM_PARAMETER Method
  });
);
```

##### `API_LOOKUP`

The `API_LOOKUP` sharing method is a work in progress, and not yet supported

#### Resource Partials

Some resources that get extracted might reference resources that aren't yet created.

In our example CDK application we include the line

```python
bucket.grantReadWrite(func);
```

This creates an `AWS::IAM::Policy` that includes the necessary Actions scoped down to the S3 bucket.

When the `AWS::IAM::Policy` is extracted, it's unable to use `Ref` or `Fn::GetAtt` to reference the S3 bucket since the S3 bucket wasn't extracted.

In this case we substitute the reference with a "partial ARN" that makes a best effort to scope the resources in the IAM policy statement to the ARN of the yet-to-be created S3 bucket.

There are multiple resource types supported out of the box (found in [`createDefaultTransforms`](src/patches/resource-extractor/resourceTransformer.ts)). In the event you have a resource not yet supported, you'll receive a `MissingTransformError`. In this case you can either open an [issue](https://github.com/cdklabs/cdk-enterprise-iac/issues) with the resource in question, or you can include the `additionalTransforms` property.

Consider the following:

```python
const vpc = new Vpc(stack, 'TestVpc');
const db = new DatabaseInstance(stack, 'TestDb', {
  vpc,
  engine: DatabaseInstanceEngine.POSTGRES,
})
const func = new Function(stack, 'TestLambda', {
  code: Code.fromAsset(path.join(__dirname, 'lambda-handler')),
  handler: 'index.handler',
  runtime: Runtime.PYTHON_3_9,
});
db.secret?.grantRead(func)

const synthedApp = app.synth();
Aspects.of(app).add(
  new ResourceExtractor({
    extractDestinationStack: extractedStack,
    stackArtifacts: synthedApp.stacks,
    valueShareMethod: ResourceExtractorShareMethod.CFN_OUTPUT,
    resourceTypesToExtract: ['AWS::IAM::Role', 'AWS::IAM::Policy'],
    additionalTransforms: {
      'AWS::SecretsManager::SecretTargetAttachment': `arn:${Aws.PARTITION}:secretsmanager:${Aws.REGION}:${Aws.ACCOUNT_ID}:secret:some-expected-value*`,
    },
  });
);
app.synth({ force: true });
```

In this case, there is a `AWS::SecretsManager::SecretTargetAttachment` generated to complete the final link between a Secrets Manager secret and the associated database by adding the database connection information to the secret JSON, which returns the ARN of the generated secret.

In the context of extracting the IAM policy, we want to tell the `ResourceExtractor` how to handle the resource section of the IAM policy statement so that it is scoped down sufficiently.

In this case rather than using a `Ref: LogicalIdForTheSecretTargetAttachment` we construct the ARN we want to use.

### Adding permissions boundaries to all generated IAM roles

Example for `AddPermissionBoundary` in Typescript project.

```python
import * as cdk from 'aws-cdk-lib';
import { MyStack } from '../lib/my-project-stack';
import { Aspects } from 'aws-cdk-lib';
import { AddPermissionBoundary } from '@cdklabs/cdk-enterprise-iac';

const app = new cdk.App();
new MyStack(app, 'MyStack');

Aspects.of(app).add(
  new AddPermissionBoundary({
    permissionsBoundaryPolicyName: 'MyPermissionBoundaryName',
    instanceProfilePrefix: 'MY_PREFIX_', // optional, Defaults to ''
    policyPrefix: 'MY_POLICY_PREFIX_', // optional, Defaults to ''
    rolePrefix: 'MY_ROLE_PREFIX_', // optional, Defaults to ''
  })
);
```

Example for `AddPermissionBoundary` in Python project.

```python
import aws_cdk as cdk
from cdklabs.cdk_enterprise_iac import AddPermissionBoundary
from test_py.test_py_stack import TestPyStack


app = cdk.App()
TestPyStack(app, "TestPyStack")

cdk.Aspects.of(app).add(AddPermissionBoundary(
    permissions_boundary_policy_name="MyPermissionBoundaryName",
    instance_profile_prefix="MY_PREFIX_",  # optional, Defaults to ""
    policy_prefix="MY_POLICY_PREFIX_",  # optional, Defaults to ""
    role_prefix="MY_ROLE_PREFIX_"  # optional, Defaults to ""
))

app.synth()
```

Details in [API.md](API.md)

## Generated API.md

---


Generated API.md below:

<details>
    <summary>Expand to view API docs</summary>

# API Reference <a name="API Reference" id="api-reference"></a>

## Constructs <a name="Constructs" id="Constructs"></a>

### EcsIsoServiceAutoscaler <a name="EcsIsoServiceAutoscaler" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler"></a>

Creates a EcsIsoServiceAutoscaler construct.

This construct allows you to scale an ECS service in an ISO
region where classic ECS Autoscaling may not be available.

#### Initializers <a name="Initializers" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.Initializer"></a>

```python
import { EcsIsoServiceAutoscaler } from '@cdklabs/cdk-enterprise-iac'

new EcsIsoServiceAutoscaler(scope: Construct, id: string, props: EcsIsoServiceAutoscalerProps)
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.Initializer.parameter.scope">scope</a></code> | <code>constructs.Construct</code> | *No description.* |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.Initializer.parameter.id">id</a></code> | <code>string</code> | *No description.* |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.Initializer.parameter.props">props</a></code> | <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps">EcsIsoServiceAutoscalerProps</a></code> | *No description.* |

---


##### `scope`<sup>Required</sup> <a name="scope" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.Initializer.parameter.scope"></a>

* *Type:* constructs.Construct

---


##### `id`<sup>Required</sup> <a name="id" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.Initializer.parameter.id"></a>

* *Type:* string

---


##### `props`<sup>Required</sup> <a name="props" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.Initializer.parameter.props"></a>

* *Type:* <a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps">EcsIsoServiceAutoscalerProps</a>

---


#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.toString">toString</a></code> | Returns a string representation of this construct. |

---


##### `toString` <a name="toString" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.toString"></a>

```python
public toString(): string
```

Returns a string representation of this construct.

#### Static Functions <a name="Static Functions" id="Static Functions"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.isConstruct">isConstruct</a></code> | Checks if `x` is a construct. |

---


##### ~~`isConstruct`~~ <a name="isConstruct" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.isConstruct"></a>

```python
import { EcsIsoServiceAutoscaler } from '@cdklabs/cdk-enterprise-iac'

EcsIsoServiceAutoscaler.isConstruct(x: any)
```

Checks if `x` is a construct.

###### `x`<sup>Required</sup> <a name="x" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.isConstruct.parameter.x"></a>

* *Type:* any

Any object.

---


#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.property.node">node</a></code> | <code>constructs.Node</code> | The tree node. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.property.ecsScalingManagerFunction">ecsScalingManagerFunction</a></code> | <code>aws-cdk-lib.aws_lambda.Function</code> | *No description.* |

---


##### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.property.node"></a>

```python
public readonly node: Node;
```

* *Type:* constructs.Node

The tree node.

---


##### `ecsScalingManagerFunction`<sup>Required</sup> <a name="ecsScalingManagerFunction" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler.property.ecsScalingManagerFunction"></a>

```python
public readonly ecsScalingManagerFunction: Function;
```

* *Type:* aws-cdk-lib.aws_lambda.Function

---


### PopulateWithConfig <a name="PopulateWithConfig" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfig"></a>

Populate a provided VPC with subnets based on a provided configuration.

*Example*

```python
const mySubnetConfig: SubnetConfig[] = [
   {
     groupName: 'app',
     cidrRange: '172.31.0.0/27',
     availabilityZone: 'a',
     subnetType: subnetType.PUBLIC,
   },
   {
     groupName: 'app',
     cidrRange: '172.31.0.32/27',
     availabilityZone: 'b',
     subnetType: subnetType.PUBLIC,
   },
   {
     groupName: 'db',
     cidrRange: '172.31.0.64/27',
     availabilityZone: 'a',
     subnetType: subnetType.PRIVATE_WITH_EGRESS,
   },
   {
     groupName: 'db',
     cidrRange: '172.31.0.96/27',
     availabilityZone: 'b',
     subnetType: subnetType.PRIVATE_WITH_EGRESS,
   },
   {
     groupName: 'iso',
     cidrRange: '172.31.0.128/26',
     availabilityZone: 'a',
     subnetType: subnetType.PRIVATE_ISOLATED,
   },
   {
     groupName: 'iso',
     cidrRange: '172.31.0.196/26',
     availabilityZone: 'b',
     subnetType: subnetType.PRIVATE_ISOLATED,
   },
 ];
new PopulateWithConfig(this, "vpcPopulater", {
  vpcId: 'vpc-abcdefg1234567',
  privateRouteTableId: 'rt-abcdefg123456',
  localRouteTableId: 'rt-123456abcdefg',
  subnetConfig: mySubnetConfig,
})
```

#### Initializers <a name="Initializers" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfig.Initializer"></a>

```python
import { PopulateWithConfig } from '@cdklabs/cdk-enterprise-iac'

new PopulateWithConfig(scope: Construct, id: string, props: PopulateWithConfigProps)
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfig.Initializer.parameter.scope">scope</a></code> | <code>constructs.Construct</code> | *No description.* |
| <code><a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfig.Initializer.parameter.id">id</a></code> | <code>string</code> | *No description.* |
| <code><a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfig.Initializer.parameter.props">props</a></code> | <code><a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps">PopulateWithConfigProps</a></code> | *No description.* |

---


##### `scope`<sup>Required</sup> <a name="scope" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfig.Initializer.parameter.scope"></a>

* *Type:* constructs.Construct

---


##### `id`<sup>Required</sup> <a name="id" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfig.Initializer.parameter.id"></a>

* *Type:* string

---


##### `props`<sup>Required</sup> <a name="props" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfig.Initializer.parameter.props"></a>

* *Type:* <a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps">PopulateWithConfigProps</a>

---


#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfig.toString">toString</a></code> | Returns a string representation of this construct. |

---


##### `toString` <a name="toString" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfig.toString"></a>

```python
public toString(): string
```

Returns a string representation of this construct.

#### Static Functions <a name="Static Functions" id="Static Functions"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfig.isConstruct">isConstruct</a></code> | Checks if `x` is a construct. |

---


##### ~~`isConstruct`~~ <a name="isConstruct" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfig.isConstruct"></a>

```python
import { PopulateWithConfig } from '@cdklabs/cdk-enterprise-iac'

PopulateWithConfig.isConstruct(x: any)
```

Checks if `x` is a construct.

###### `x`<sup>Required</sup> <a name="x" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfig.isConstruct.parameter.x"></a>

* *Type:* any

Any object.

---


#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfig.property.node">node</a></code> | <code>constructs.Node</code> | The tree node. |

---


##### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfig.property.node"></a>

```python
public readonly node: Node;
```

* *Type:* constructs.Node

The tree node.

---


### SplitVpcEvenly <a name="SplitVpcEvenly" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenly"></a>

Splits a VPC evenly between a provided number of AZs (3 if not defined), and attaches a provided route table to each, and labels.

*Example*

```python
// with more specific properties
new SplitVpcEvenly(this, 'evenSplitVpc', {
  vpcId: 'vpc-abcdefg123456',
  vpcCidr: '172.16.0.0/16',
  routeTableId: 'rt-abcdefgh123456',
  cidrBits: '10',
  numberOfAzs: 4,
  subnetType: subnetType.PRIVATE_ISOLATED,
});
```

#### Initializers <a name="Initializers" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.Initializer"></a>

```python
import { SplitVpcEvenly } from '@cdklabs/cdk-enterprise-iac'

new SplitVpcEvenly(scope: Construct, id: string, props: SplitVpcEvenlyProps)
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.Initializer.parameter.scope">scope</a></code> | <code>constructs.Construct</code> | *No description.* |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.Initializer.parameter.id">id</a></code> | <code>string</code> | *No description.* |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.Initializer.parameter.props">props</a></code> | <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps">SplitVpcEvenlyProps</a></code> | *No description.* |

---


##### `scope`<sup>Required</sup> <a name="scope" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.Initializer.parameter.scope"></a>

* *Type:* constructs.Construct

---


##### `id`<sup>Required</sup> <a name="id" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.Initializer.parameter.id"></a>

* *Type:* string

---


##### `props`<sup>Required</sup> <a name="props" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.Initializer.parameter.props"></a>

* *Type:* <a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps">SplitVpcEvenlyProps</a>

---


#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.toString">toString</a></code> | Returns a string representation of this construct. |

---


##### `toString` <a name="toString" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.toString"></a>

```python
public toString(): string
```

Returns a string representation of this construct.

#### Static Functions <a name="Static Functions" id="Static Functions"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.isConstruct">isConstruct</a></code> | Checks if `x` is a construct. |

---


##### ~~`isConstruct`~~ <a name="isConstruct" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.isConstruct"></a>

```python
import { SplitVpcEvenly } from '@cdklabs/cdk-enterprise-iac'

SplitVpcEvenly.isConstruct(x: any)
```

Checks if `x` is a construct.

###### `x`<sup>Required</sup> <a name="x" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.isConstruct.parameter.x"></a>

* *Type:* any

Any object.

---


#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.property.node">node</a></code> | <code>constructs.Node</code> | The tree node. |

---


##### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenly.property.node"></a>

```python
public readonly node: Node;
```

* *Type:* constructs.Node

The tree node.

---


## Structs <a name="Structs" id="Structs"></a>

### AddCfnInitProxyProps <a name="AddCfnInitProxyProps" id="@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps"></a>

Properties for the proxy server to use with cfn helper commands.

#### Initializer <a name="Initializer" id="@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps.Initializer"></a>

```python
import { AddCfnInitProxyProps } from '@cdklabs/cdk-enterprise-iac'

const addCfnInitProxyProps: AddCfnInitProxyProps = { ... }
```

#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps.property.proxyHost">proxyHost</a></code> | <code>string</code> | host of your proxy. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps.property.proxyPort">proxyPort</a></code> | <code>number</code> | proxy port. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps.property.proxyCredentials">proxyCredentials</a></code> | <code>aws-cdk-lib.aws_secretsmanager.ISecret</code> | JSON secret containing `user` and `password` properties to use if your proxy requires credentials `http://user:password@host:port` could contain sensitive data, so using a Secret. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps.property.proxyType">proxyType</a></code> | <code><a href="#@cdklabs/cdk-enterprise-iac.ProxyType">ProxyType</a></code> | Proxy Type. |

---


##### `proxyHost`<sup>Required</sup> <a name="proxyHost" id="@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps.property.proxyHost"></a>

```python
public readonly proxyHost: string;
```

* *Type:* string

host of your proxy.

---


*Example*

```python
example.com
```

##### `proxyPort`<sup>Required</sup> <a name="proxyPort" id="@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps.property.proxyPort"></a>

```python
public readonly proxyPort: number;
```

* *Type:* number

proxy port.

---


*Example*

```python
8080
```

##### `proxyCredentials`<sup>Optional</sup> <a name="proxyCredentials" id="@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps.property.proxyCredentials"></a>

```python
public readonly proxyCredentials: ISecret;
```

* *Type:* aws-cdk-lib.aws_secretsmanager.ISecret

JSON secret containing `user` and `password` properties to use if your proxy requires credentials `http://user:password@host:port` could contain sensitive data, so using a Secret.

Note that while the `user` and `password` won't be visible in the cloudformation template
they **will** be in plain text inside your `UserData`

---


*Example*

```python
const secret = new Secret(stack, 'TestSecret', {
 secretObjectValue: {
   user: SecretValue,
   password: SecretValue,
 },
});
```

##### `proxyType`<sup>Optional</sup> <a name="proxyType" id="@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps.property.proxyType"></a>

```python
public readonly proxyType: ProxyType;
```

* *Type:* <a href="#@cdklabs/cdk-enterprise-iac.ProxyType">ProxyType</a>
* *Default:* ProxyType.HTTP

Proxy Type.

---


*Example*

```python
ProxyType.HTTPS
```

### AddPermissionBoundaryProps <a name="AddPermissionBoundaryProps" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps"></a>

Properties to pass to the AddPermissionBoundary.

#### Initializer <a name="Initializer" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps.Initializer"></a>

```python
import { AddPermissionBoundaryProps } from '@cdklabs/cdk-enterprise-iac'

const addPermissionBoundaryProps: AddPermissionBoundaryProps = { ... }
```

#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps.property.permissionsBoundaryPolicyName">permissionsBoundaryPolicyName</a></code> | <code>string</code> | Name of Permissions Boundary Policy to add to all IAM roles. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps.property.instanceProfilePrefix">instanceProfilePrefix</a></code> | <code>string</code> | A prefix to prepend to the name of the IAM InstanceProfiles (Default: ''). |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps.property.policyPrefix">policyPrefix</a></code> | <code>string</code> | A prefix to prepend to the name of the IAM Policies and ManagedPolicies (Default: ''). |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps.property.rolePrefix">rolePrefix</a></code> | <code>string</code> | A prefix to prepend to the name of IAM Roles (Default: ''). |

---


##### `permissionsBoundaryPolicyName`<sup>Required</sup> <a name="permissionsBoundaryPolicyName" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps.property.permissionsBoundaryPolicyName"></a>

```python
public readonly permissionsBoundaryPolicyName: string;
```

* *Type:* string

Name of Permissions Boundary Policy to add to all IAM roles.

---


##### `instanceProfilePrefix`<sup>Optional</sup> <a name="instanceProfilePrefix" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps.property.instanceProfilePrefix"></a>

```python
public readonly instanceProfilePrefix: string;
```

* *Type:* string

A prefix to prepend to the name of the IAM InstanceProfiles (Default: '').

---


##### `policyPrefix`<sup>Optional</sup> <a name="policyPrefix" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps.property.policyPrefix"></a>

```python
public readonly policyPrefix: string;
```

* *Type:* string

A prefix to prepend to the name of the IAM Policies and ManagedPolicies (Default: '').

---


##### `rolePrefix`<sup>Optional</sup> <a name="rolePrefix" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps.property.rolePrefix"></a>

```python
public readonly rolePrefix: string;
```

* *Type:* string

A prefix to prepend to the name of IAM Roles (Default: '').

---


### EcsIsoServiceAutoscalerProps <a name="EcsIsoServiceAutoscalerProps" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps"></a>

#### Initializer <a name="Initializer" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.Initializer"></a>

```python
import { EcsIsoServiceAutoscalerProps } from '@cdklabs/cdk-enterprise-iac'

const ecsIsoServiceAutoscalerProps: EcsIsoServiceAutoscalerProps = { ... }
```

#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.ecsCluster">ecsCluster</a></code> | <code>aws-cdk-lib.aws_ecs.Cluster</code> | The cluster the service you wish to scale resides in. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.ecsService">ecsService</a></code> | <code>aws-cdk-lib.aws_ecs.IService</code> | The ECS service you wish to scale. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.scaleAlarm">scaleAlarm</a></code> | <code>aws-cdk-lib.aws_cloudwatch.Alarm</code> | The Cloudwatch Alarm that will cause scaling actions to be invoked, whether it's in or not in alarm will determine scale up and down actions. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.maximumTaskCount">maximumTaskCount</a></code> | <code>number</code> | The maximum number of tasks that the service will scale out to. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.minimumTaskCount">minimumTaskCount</a></code> | <code>number</code> | The minimum number of tasks the service will have. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.role">role</a></code> | <code>aws-cdk-lib.aws_iam.IRole</code> | Optional IAM role to attach to the created lambda to adjust the desired count on the ECS Service. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.scaleInCooldown">scaleInCooldown</a></code> | <code>aws-cdk-lib.Duration</code> | How long will the application wait before performing another scale in action. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.scaleInIncrement">scaleInIncrement</a></code> | <code>number</code> | The number of tasks that will scale in on scale in alarm status. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.scaleOutCooldown">scaleOutCooldown</a></code> | <code>aws-cdk-lib.Duration</code> | How long will a the application wait before performing another scale out action. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.scaleOutIncrement">scaleOutIncrement</a></code> | <code>number</code> | The number of tasks that will scale out on scale out alarm status. |

---


##### `ecsCluster`<sup>Required</sup> <a name="ecsCluster" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.ecsCluster"></a>

```python
public readonly ecsCluster: Cluster;
```

* *Type:* aws-cdk-lib.aws_ecs.Cluster

The cluster the service you wish to scale resides in.

---


##### `ecsService`<sup>Required</sup> <a name="ecsService" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.ecsService"></a>

```python
public readonly ecsService: IService;
```

* *Type:* aws-cdk-lib.aws_ecs.IService

The ECS service you wish to scale.

---


##### `scaleAlarm`<sup>Required</sup> <a name="scaleAlarm" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.scaleAlarm"></a>

```python
public readonly scaleAlarm: Alarm;
```

* *Type:* aws-cdk-lib.aws_cloudwatch.Alarm

The Cloudwatch Alarm that will cause scaling actions to be invoked, whether it's in or not in alarm will determine scale up and down actions.

---


##### `maximumTaskCount`<sup>Optional</sup> <a name="maximumTaskCount" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.maximumTaskCount"></a>

```python
public readonly maximumTaskCount: number;
```

* *Type:* number
* *Default:* 10

The maximum number of tasks that the service will scale out to.

Note: This does not provide any protection from scaling out above the maximum allowed in your account, set this variable and manage account quotas appropriately.

---


##### `minimumTaskCount`<sup>Optional</sup> <a name="minimumTaskCount" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.minimumTaskCount"></a>

```python
public readonly minimumTaskCount: number;
```

* *Type:* number
* *Default:* 1

The minimum number of tasks the service will have.

---


##### `role`<sup>Optional</sup> <a name="role" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.role"></a>

```python
public readonly role: IRole;
```

* *Type:* aws-cdk-lib.aws_iam.IRole
* *Default:* A role is created for you with least privilege IAM policy

Optional IAM role to attach to the created lambda to adjust the desired count on the ECS Service.

Ensure this role has appropriate privileges. Example IAM policy statements:

```json
{
  "PolicyDocument": {
    "Statement": [
      {
        "Action": "cloudwatch:DescribeAlarms",
        "Effect": "Allow",
        "Resource": "arn:${Partition}:cloudwatch:${Region}:${Account}:alarm:${AlarmName}"
      },
      {
        "Action": [
          "ecs:DescribeServices",
          "ecs:UpdateService"
        ],
        "Condition": {
          "StringEquals": {
            "ecs:cluster": "arn:${Partition}:ecs:${Region}:${Account}:cluster/${ClusterName}"
          }
        },
        "Effect": "Allow",
        "Resource": "arn:${Partition}:ecs:${Region}:${Account}:service/${ClusterName}/${ServiceName}"
      }
    ],
    "Version": "2012-10-17"
  }
}
```

---


##### `scaleInCooldown`<sup>Optional</sup> <a name="scaleInCooldown" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.scaleInCooldown"></a>

```python
public readonly scaleInCooldown: Duration;
```

* *Type:* aws-cdk-lib.Duration
* *Default:* 60 seconds

How long will the application wait before performing another scale in action.

---


##### `scaleInIncrement`<sup>Optional</sup> <a name="scaleInIncrement" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.scaleInIncrement"></a>

```python
public readonly scaleInIncrement: number;
```

* *Type:* number
* *Default:* 1

The number of tasks that will scale in on scale in alarm status.

---


##### `scaleOutCooldown`<sup>Optional</sup> <a name="scaleOutCooldown" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.scaleOutCooldown"></a>

```python
public readonly scaleOutCooldown: Duration;
```

* *Type:* aws-cdk-lib.Duration
* *Default:* 60 seconds

How long will a the application wait before performing another scale out action.

---


##### `scaleOutIncrement`<sup>Optional</sup> <a name="scaleOutIncrement" id="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps.property.scaleOutIncrement"></a>

```python
public readonly scaleOutIncrement: number;
```

* *Type:* number
* *Default:* 1

The number of tasks that will scale out on scale out alarm status.

---


### PopulateWithConfigProps <a name="PopulateWithConfigProps" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps"></a>

#### Initializer <a name="Initializer" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps.Initializer"></a>

```python
import { PopulateWithConfigProps } from '@cdklabs/cdk-enterprise-iac'

const populateWithConfigProps: PopulateWithConfigProps = { ... }
```

#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps.property.localRouteTableId">localRouteTableId</a></code> | <code>string</code> | Local route table ID, with routes only to local VPC. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps.property.privateRouteTableId">privateRouteTableId</a></code> | <code>string</code> | Route table ID for a provided route table with routes to enterprise network. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps.property.subnetConfig">subnetConfig</a></code> | <code><a href="#@cdklabs/cdk-enterprise-iac.SubnetConfig">SubnetConfig</a>[]</code> | List of Subnet configs to provision to provision. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps.property.vpcId">vpcId</a></code> | <code>string</code> | ID of the VPC provided that needs to be populated. |

---


##### `localRouteTableId`<sup>Required</sup> <a name="localRouteTableId" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps.property.localRouteTableId"></a>

```python
public readonly localRouteTableId: string;
```

* *Type:* string

Local route table ID, with routes only to local VPC.

---


##### `privateRouteTableId`<sup>Required</sup> <a name="privateRouteTableId" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps.property.privateRouteTableId"></a>

```python
public readonly privateRouteTableId: string;
```

* *Type:* string

Route table ID for a provided route table with routes to enterprise network.

Both subnetType.PUBLIC and subnetType.PRIVATE_WITH_EGRESS will use this property

---


##### `subnetConfig`<sup>Required</sup> <a name="subnetConfig" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps.property.subnetConfig"></a>

```python
public readonly subnetConfig: SubnetConfig[];
```

* *Type:* <a href="#@cdklabs/cdk-enterprise-iac.SubnetConfig">SubnetConfig</a>[]

List of Subnet configs to provision to provision.

---


##### `vpcId`<sup>Required</sup> <a name="vpcId" id="@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps.property.vpcId"></a>

```python
public readonly vpcId: string;
```

* *Type:* string

ID of the VPC provided that needs to be populated.

---


### RemoveTagsProps <a name="RemoveTagsProps" id="@cdklabs/cdk-enterprise-iac.RemoveTagsProps"></a>

#### Initializer <a name="Initializer" id="@cdklabs/cdk-enterprise-iac.RemoveTagsProps.Initializer"></a>

```python
import { RemoveTagsProps } from '@cdklabs/cdk-enterprise-iac'

const removeTagsProps: RemoveTagsProps = { ... }
```

#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.RemoveTagsProps.property.cloudformationResource">cloudformationResource</a></code> | <code>string</code> | Name of Cloudformation resource Type (e.g. 'AWS::Lambda::Function'). |
| <code><a href="#@cdklabs/cdk-enterprise-iac.RemoveTagsProps.property.tagPropertyName">tagPropertyName</a></code> | <code>string</code> | Name of the tag property to remove from the resource. |

---


##### `cloudformationResource`<sup>Required</sup> <a name="cloudformationResource" id="@cdklabs/cdk-enterprise-iac.RemoveTagsProps.property.cloudformationResource"></a>

```python
public readonly cloudformationResource: string;
```

* *Type:* string

Name of Cloudformation resource Type (e.g. 'AWS::Lambda::Function').

---


##### `tagPropertyName`<sup>Optional</sup> <a name="tagPropertyName" id="@cdklabs/cdk-enterprise-iac.RemoveTagsProps.property.tagPropertyName"></a>

```python
public readonly tagPropertyName: string;
```

* *Type:* string
* *Default:* Tags

Name of the tag property to remove from the resource.

---


### ResourceExtractorProps <a name="ResourceExtractorProps" id="@cdklabs/cdk-enterprise-iac.ResourceExtractorProps"></a>

#### Initializer <a name="Initializer" id="@cdklabs/cdk-enterprise-iac.ResourceExtractorProps.Initializer"></a>

```python
import { ResourceExtractorProps } from '@cdklabs/cdk-enterprise-iac'

const resourceExtractorProps: ResourceExtractorProps = { ... }
```

#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorProps.property.extractDestinationStack">extractDestinationStack</a></code> | <code>aws-cdk-lib.Stack</code> | Stack to move found extracted resources into. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorProps.property.resourceTypesToExtract">resourceTypesToExtract</a></code> | <code>string[]</code> | List of resource types to extract, ex: `AWS::IAM::Role`. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorProps.property.stackArtifacts">stackArtifacts</a></code> | <code>aws-cdk-lib.cx_api.CloudFormationStackArtifact[]</code> | Synthed stack artifacts from your CDK app. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorProps.property.additionalTransforms">additionalTransforms</a></code> | <code>{[ key: string ]: string}</code> | Additional resource transformations. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorProps.property.valueShareMethod">valueShareMethod</a></code> | <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorShareMethod">ResourceExtractorShareMethod</a></code> | The sharing method to use when passing exported resources from the "Extracted Stack" into the original stack(s). |

---


##### `extractDestinationStack`<sup>Required</sup> <a name="extractDestinationStack" id="@cdklabs/cdk-enterprise-iac.ResourceExtractorProps.property.extractDestinationStack"></a>

```python
public readonly extractDestinationStack: Stack;
```

* *Type:* aws-cdk-lib.Stack

Stack to move found extracted resources into.

---


##### `resourceTypesToExtract`<sup>Required</sup> <a name="resourceTypesToExtract" id="@cdklabs/cdk-enterprise-iac.ResourceExtractorProps.property.resourceTypesToExtract"></a>

```python
public readonly resourceTypesToExtract: string[];
```

* *Type:* string[]

List of resource types to extract, ex: `AWS::IAM::Role`.

---


##### `stackArtifacts`<sup>Required</sup> <a name="stackArtifacts" id="@cdklabs/cdk-enterprise-iac.ResourceExtractorProps.property.stackArtifacts"></a>

```python
public readonly stackArtifacts: CloudFormationStackArtifact[];
```

* *Type:* aws-cdk-lib.cx_api.CloudFormationStackArtifact[]

Synthed stack artifacts from your CDK app.

---


##### `additionalTransforms`<sup>Optional</sup> <a name="additionalTransforms" id="@cdklabs/cdk-enterprise-iac.ResourceExtractorProps.property.additionalTransforms"></a>

```python
public readonly additionalTransforms: {[ key: string ]: string};
```

* *Type:* {[ key: string ]: string}

Additional resource transformations.

---


##### `valueShareMethod`<sup>Optional</sup> <a name="valueShareMethod" id="@cdklabs/cdk-enterprise-iac.ResourceExtractorProps.property.valueShareMethod"></a>

```python
public readonly valueShareMethod: ResourceExtractorShareMethod;
```

* *Type:* <a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorShareMethod">ResourceExtractorShareMethod</a>

The sharing method to use when passing exported resources from the "Extracted Stack" into the original stack(s).

---


### SetApiGatewayEndpointConfigurationProps <a name="SetApiGatewayEndpointConfigurationProps" id="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfigurationProps"></a>

#### Initializer <a name="Initializer" id="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfigurationProps.Initializer"></a>

```python
import { SetApiGatewayEndpointConfigurationProps } from '@cdklabs/cdk-enterprise-iac'

const setApiGatewayEndpointConfigurationProps: SetApiGatewayEndpointConfigurationProps = { ... }
```

#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfigurationProps.property.endpointType">endpointType</a></code> | <code>aws-cdk-lib.aws_apigateway.EndpointType</code> | API Gateway endpoint type to override to. |

---


##### `endpointType`<sup>Optional</sup> <a name="endpointType" id="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfigurationProps.property.endpointType"></a>

```python
public readonly endpointType: EndpointType;
```

* *Type:* aws-cdk-lib.aws_apigateway.EndpointType
* *Default:* EndpointType.REGIONAL

API Gateway endpoint type to override to.

Defaults to EndpointType.REGIONAL

---


### SplitVpcEvenlyProps <a name="SplitVpcEvenlyProps" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps"></a>

#### Initializer <a name="Initializer" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.Initializer"></a>

```python
import { SplitVpcEvenlyProps } from '@cdklabs/cdk-enterprise-iac'

const splitVpcEvenlyProps: SplitVpcEvenlyProps = { ... }
```

#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.routeTableId">routeTableId</a></code> | <code>string</code> | Route Table ID that will be attached to each subnet created. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.vpcCidr">vpcCidr</a></code> | <code>string</code> | CIDR range of the VPC you're populating. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.vpcId">vpcId</a></code> | <code>string</code> | ID of the existing VPC you're trying to populate. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.cidrBits">cidrBits</a></code> | <code>string</code> | `cidrBits` argument for the [`Fn::Cidr`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-cidr.html) Cloudformation intrinsic function. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.numberOfAzs">numberOfAzs</a></code> | <code>number</code> | Number of AZs to evenly split into. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.subnetType">subnetType</a></code> | <code>aws-cdk-lib.aws_ec2.SubnetType</code> | *No description.* |

---


##### `routeTableId`<sup>Required</sup> <a name="routeTableId" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.routeTableId"></a>

```python
public readonly routeTableId: string;
```

* *Type:* string

Route Table ID that will be attached to each subnet created.

---


##### `vpcCidr`<sup>Required</sup> <a name="vpcCidr" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.vpcCidr"></a>

```python
public readonly vpcCidr: string;
```

* *Type:* string

CIDR range of the VPC you're populating.

---


##### `vpcId`<sup>Required</sup> <a name="vpcId" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.vpcId"></a>

```python
public readonly vpcId: string;
```

* *Type:* string

ID of the existing VPC you're trying to populate.

---


##### `cidrBits`<sup>Optional</sup> <a name="cidrBits" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.cidrBits"></a>

```python
public readonly cidrBits: string;
```

* *Type:* string
* *Default:* '6'

`cidrBits` argument for the [`Fn::Cidr`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-cidr.html) Cloudformation intrinsic function.

---


##### `numberOfAzs`<sup>Optional</sup> <a name="numberOfAzs" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.numberOfAzs"></a>

```python
public readonly numberOfAzs: number;
```

* *Type:* number
* *Default:* 3

Number of AZs to evenly split into.

---


##### `subnetType`<sup>Optional</sup> <a name="subnetType" id="@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps.property.subnetType"></a>

```python
public readonly subnetType: SubnetType;
```

* *Type:* aws-cdk-lib.aws_ec2.SubnetType
* *Default:* subnetType.PRIVATE

---


### SubnetConfig <a name="SubnetConfig" id="@cdklabs/cdk-enterprise-iac.SubnetConfig"></a>

#### Initializer <a name="Initializer" id="@cdklabs/cdk-enterprise-iac.SubnetConfig.Initializer"></a>

```python
import { SubnetConfig } from '@cdklabs/cdk-enterprise-iac'

const subnetConfig: SubnetConfig = { ... }
```

#### Properties <a name="Properties" id="Properties"></a>

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SubnetConfig.property.availabilityZone">availabilityZone</a></code> | <code>string</code> | Which availability zone the subnet should be in. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SubnetConfig.property.cidrRange">cidrRange</a></code> | <code>string</code> | Cidr range of the subnet to create. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SubnetConfig.property.groupName">groupName</a></code> | <code>string</code> | Logical group name of a subnet. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SubnetConfig.property.subnetType">subnetType</a></code> | <code>aws-cdk-lib.aws_ec2.SubnetType</code> | What [SubnetType](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.SubnetType.html) to use. |

---


##### `availabilityZone`<sup>Required</sup> <a name="availabilityZone" id="@cdklabs/cdk-enterprise-iac.SubnetConfig.property.availabilityZone"></a>

```python
public readonly availabilityZone: string;
```

* *Type:* string

Which availability zone the subnet should be in.

---


##### `cidrRange`<sup>Required</sup> <a name="cidrRange" id="@cdklabs/cdk-enterprise-iac.SubnetConfig.property.cidrRange"></a>

```python
public readonly cidrRange: string;
```

* *Type:* string

Cidr range of the subnet to create.

---


##### `groupName`<sup>Required</sup> <a name="groupName" id="@cdklabs/cdk-enterprise-iac.SubnetConfig.property.groupName"></a>

```python
public readonly groupName: string;
```

* *Type:* string

Logical group name of a subnet.

---


*Example*

```python
db
```

##### `subnetType`<sup>Required</sup> <a name="subnetType" id="@cdklabs/cdk-enterprise-iac.SubnetConfig.property.subnetType"></a>

```python
public readonly subnetType: SubnetType;
```

* *Type:* aws-cdk-lib.aws_ec2.SubnetType

What [SubnetType](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.SubnetType.html) to use.

This will govern the `aws-cdk:subnet-type` tag on the subnet

SubnetType | `aws-cdk:subnet-type` tag value
--- | ---
`PRIVATE_ISOLATED` | 'Isolated'
`PRIVATE_WITH_EGRESS` | 'Private'
`PUBLIC` | 'Public'

---


## Classes <a name="Classes" id="Classes"></a>

### AddCfnInitProxy <a name="AddCfnInitProxy" id="@cdklabs/cdk-enterprise-iac.AddCfnInitProxy"></a>

* *Implements:* aws-cdk-lib.IAspect

Add proxy configuration to Cloudformation helper functions.

#### Initializers <a name="Initializers" id="@cdklabs/cdk-enterprise-iac.AddCfnInitProxy.Initializer"></a>

```python
import { AddCfnInitProxy } from '@cdklabs/cdk-enterprise-iac'

new AddCfnInitProxy(props: AddCfnInitProxyProps)
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddCfnInitProxy.Initializer.parameter.props">props</a></code> | <code><a href="#@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps">AddCfnInitProxyProps</a></code> | *No description.* |

---


##### `props`<sup>Required</sup> <a name="props" id="@cdklabs/cdk-enterprise-iac.AddCfnInitProxy.Initializer.parameter.props"></a>

* *Type:* <a href="#@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps">AddCfnInitProxyProps</a>

---


#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddCfnInitProxy.visit">visit</a></code> | All aspects can visit an IConstruct. |

---


##### `visit` <a name="visit" id="@cdklabs/cdk-enterprise-iac.AddCfnInitProxy.visit"></a>

```python
public visit(node: IConstruct): void
```

All aspects can visit an IConstruct.

###### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.AddCfnInitProxy.visit.parameter.node"></a>

* *Type:* constructs.IConstruct

---


### AddLambdaEnvironmentVariables <a name="AddLambdaEnvironmentVariables" id="@cdklabs/cdk-enterprise-iac.AddLambdaEnvironmentVariables"></a>

* *Implements:* aws-cdk-lib.IAspect

Add one or more environment variables to *all* lambda functions within a scope.

#### Initializers <a name="Initializers" id="@cdklabs/cdk-enterprise-iac.AddLambdaEnvironmentVariables.Initializer"></a>

```python
import { AddLambdaEnvironmentVariables } from '@cdklabs/cdk-enterprise-iac'

new AddLambdaEnvironmentVariables(props: {[ key: string ]: string})
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddLambdaEnvironmentVariables.Initializer.parameter.props">props</a></code> | <code>{[ key: string ]: string}</code> | : string} props - Key Value pair(s) for environment variables to add to all lambda functions. |

---


##### `props`<sup>Required</sup> <a name="props" id="@cdklabs/cdk-enterprise-iac.AddLambdaEnvironmentVariables.Initializer.parameter.props"></a>

* *Type:* {[ key: string ]: string}

: string} props - Key Value pair(s) for environment variables to add to all lambda functions.

---


#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddLambdaEnvironmentVariables.visit">visit</a></code> | All aspects can visit an IConstruct. |

---


##### `visit` <a name="visit" id="@cdklabs/cdk-enterprise-iac.AddLambdaEnvironmentVariables.visit"></a>

```python
public visit(node: IConstruct): void
```

All aspects can visit an IConstruct.

###### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.AddLambdaEnvironmentVariables.visit.parameter.node"></a>

* *Type:* constructs.IConstruct

---


### AddPermissionBoundary <a name="AddPermissionBoundary" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary"></a>

* *Implements:* aws-cdk-lib.IAspect

A patch for Adding Permissions Boundaries to all IAM roles.

Additional options for adding prefixes to IAM role, policy and instance profile names

Can account for non commercial partitions (e.g. aws-gov, aws-cn)

#### Initializers <a name="Initializers" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.Initializer"></a>

```python
import { AddPermissionBoundary } from '@cdklabs/cdk-enterprise-iac'

new AddPermissionBoundary(props: AddPermissionBoundaryProps)
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.Initializer.parameter.props">props</a></code> | <code><a href="#@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps">AddPermissionBoundaryProps</a></code> | *No description.* |

---


##### `props`<sup>Required</sup> <a name="props" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.Initializer.parameter.props"></a>

* *Type:* <a href="#@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps">AddPermissionBoundaryProps</a>

---


#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.checkAndOverride">checkAndOverride</a></code> | *No description.* |
| <code><a href="#@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.visit">visit</a></code> | All aspects can visit an IConstruct. |

---


##### `checkAndOverride` <a name="checkAndOverride" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.checkAndOverride"></a>

```python
public checkAndOverride(node: CfnResource, prefix: string, length: number, cfnProp: string, cdkProp?: string): void
```

###### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.checkAndOverride.parameter.node"></a>

* *Type:* aws-cdk-lib.CfnResource

---


###### `prefix`<sup>Required</sup> <a name="prefix" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.checkAndOverride.parameter.prefix"></a>

* *Type:* string

---


###### `length`<sup>Required</sup> <a name="length" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.checkAndOverride.parameter.length"></a>

* *Type:* number

---


###### `cfnProp`<sup>Required</sup> <a name="cfnProp" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.checkAndOverride.parameter.cfnProp"></a>

* *Type:* string

---


###### `cdkProp`<sup>Optional</sup> <a name="cdkProp" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.checkAndOverride.parameter.cdkProp"></a>

* *Type:* string

---


##### `visit` <a name="visit" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.visit"></a>

```python
public visit(node: IConstruct): void
```

All aspects can visit an IConstruct.

###### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary.visit.parameter.node"></a>

* *Type:* constructs.IConstruct

---


### ConvertInlinePoliciesToManaged <a name="ConvertInlinePoliciesToManaged" id="@cdklabs/cdk-enterprise-iac.ConvertInlinePoliciesToManaged"></a>

* *Implements:* aws-cdk-lib.IAspect

Patch for turning all Policies into ConvertInlinePoliciesToManaged.

Some users have policies in place that make it impossible to create inline policies. Instead,
they must use managed policies.

Note that order matters with this aspect. Specifically, it should generally be added first.
This is because other aspects may add overrides that would be lost if applied before
this aspect since the original aspect is removed and replaced.

*Example*

```python
// Replace all AWS::IAM::Policy resources with equivalent AWS::IAM::ManagedPolicy
Aspects.of(stack).add(new ConvertInlinePoliciesToManaged())
```

#### Initializers <a name="Initializers" id="@cdklabs/cdk-enterprise-iac.ConvertInlinePoliciesToManaged.Initializer"></a>

```python
import { ConvertInlinePoliciesToManaged } from '@cdklabs/cdk-enterprise-iac'

new ConvertInlinePoliciesToManaged()
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |

---


#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ConvertInlinePoliciesToManaged.visit">visit</a></code> | All aspects can visit an IConstruct. |

---


##### `visit` <a name="visit" id="@cdklabs/cdk-enterprise-iac.ConvertInlinePoliciesToManaged.visit"></a>

```python
public visit(node: IConstruct): void
```

All aspects can visit an IConstruct.

###### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.ConvertInlinePoliciesToManaged.visit.parameter.node"></a>

* *Type:* constructs.IConstruct

---


### RemovePublicAccessBlockConfiguration <a name="RemovePublicAccessBlockConfiguration" id="@cdklabs/cdk-enterprise-iac.RemovePublicAccessBlockConfiguration"></a>

* *Implements:* aws-cdk-lib.IAspect

Looks for S3 Buckets, and removes the `PublicAccessBlockConfiguration` property.

For use in regions where Cloudformation doesn't support this property

#### Initializers <a name="Initializers" id="@cdklabs/cdk-enterprise-iac.RemovePublicAccessBlockConfiguration.Initializer"></a>

```python
import { RemovePublicAccessBlockConfiguration } from '@cdklabs/cdk-enterprise-iac'

new RemovePublicAccessBlockConfiguration()
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |

---


#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.RemovePublicAccessBlockConfiguration.visit">visit</a></code> | All aspects can visit an IConstruct. |

---


##### `visit` <a name="visit" id="@cdklabs/cdk-enterprise-iac.RemovePublicAccessBlockConfiguration.visit"></a>

```python
public visit(node: IConstruct): void
```

All aspects can visit an IConstruct.

###### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.RemovePublicAccessBlockConfiguration.visit.parameter.node"></a>

* *Type:* constructs.IConstruct

---


### RemoveTags <a name="RemoveTags" id="@cdklabs/cdk-enterprise-iac.RemoveTags"></a>

* *Implements:* aws-cdk-lib.IAspect

Patch for removing tags from a specific Cloudformation Resource.

In some regions, the 'Tags' property isn't supported in Cloudformation. This patch makes it easy to remove

*Example*

```python
// Remove tags on a resource
Aspects.of(stack).add(new RemoveTags({
  cloudformationResource: 'AWS::ECS::Cluster',
}));
// Remove tags without the standard 'Tags' name
Aspects.of(stack).add(new RemoveTags({
  cloudformationResource: 'AWS::Backup::BackupPlan',
   tagPropertyName: 'BackupPlanTags',
}));
```

#### Initializers <a name="Initializers" id="@cdklabs/cdk-enterprise-iac.RemoveTags.Initializer"></a>

```python
import { RemoveTags } from '@cdklabs/cdk-enterprise-iac'

new RemoveTags(props: RemoveTagsProps)
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.RemoveTags.Initializer.parameter.props">props</a></code> | <code><a href="#@cdklabs/cdk-enterprise-iac.RemoveTagsProps">RemoveTagsProps</a></code> | *No description.* |

---


##### `props`<sup>Required</sup> <a name="props" id="@cdklabs/cdk-enterprise-iac.RemoveTags.Initializer.parameter.props"></a>

* *Type:* <a href="#@cdklabs/cdk-enterprise-iac.RemoveTagsProps">RemoveTagsProps</a>

---


#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.RemoveTags.visit">visit</a></code> | All aspects can visit an IConstruct. |

---


##### `visit` <a name="visit" id="@cdklabs/cdk-enterprise-iac.RemoveTags.visit"></a>

```python
public visit(node: IConstruct): void
```

All aspects can visit an IConstruct.

###### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.RemoveTags.visit.parameter.node"></a>

* *Type:* constructs.IConstruct

---


### ResourceExtractor <a name="ResourceExtractor" id="@cdklabs/cdk-enterprise-iac.ResourceExtractor"></a>

* *Implements:* aws-cdk-lib.IAspect

This Aspect takes a CDK application, all synthesized CloudFormationStackArtifact, a value share method, and a list of Cloudformation resources that should be pulled out of the main CDK application, which should be synthesized to a cloudformation template that an external team (e.g. security team) to deploy, and adjusting the CDK application to reference pre-created resources already pulled out.

*Example*

```python
 const app = App()
 const stack = new Stack(app, 'MyStack');
 extractedStack = new Stack(app, 'ExtractedStack');
 const synthedApp = app.synth();
 Aspects.of(app).add(new ResourceExtractor({
   extractDestinationStack: extractedStack,
   stackArtifacts: synthedApp.stacks,
   valueShareMethod: ResourceExtractorShareMethod.CFN_OUTPUT,
   resourceTypesToExtract: [
     'AWS::IAM::Role',
     'AWS::IAM::Policy',
     'AWS::IAM::ManagedPolicy',
     'AWS::IAM::InstanceProfile',
   ],
 });
 app.synth({ force: true });
```

#### Initializers <a name="Initializers" id="@cdklabs/cdk-enterprise-iac.ResourceExtractor.Initializer"></a>

```python
import { ResourceExtractor } from '@cdklabs/cdk-enterprise-iac'

new ResourceExtractor(props: ResourceExtractorProps)
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractor.Initializer.parameter.props">props</a></code> | <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorProps">ResourceExtractorProps</a></code> | *No description.* |

---


##### `props`<sup>Required</sup> <a name="props" id="@cdklabs/cdk-enterprise-iac.ResourceExtractor.Initializer.parameter.props"></a>

* *Type:* <a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorProps">ResourceExtractorProps</a>

---


#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractor.visit">visit</a></code> | Entrypoint. |

---


##### `visit` <a name="visit" id="@cdklabs/cdk-enterprise-iac.ResourceExtractor.visit"></a>

```python
public visit(node: IConstruct): void
```

Entrypoint.

###### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.ResourceExtractor.visit.parameter.node"></a>

* *Type:* constructs.IConstruct

---


### SetApiGatewayEndpointConfiguration <a name="SetApiGatewayEndpointConfiguration" id="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfiguration"></a>

* *Implements:* aws-cdk-lib.IAspect

Override RestApis to use a set endpoint configuration.

Some regions don't support EDGE endpoints, and some enterprises require
specific endpoint types for RestApis

#### Initializers <a name="Initializers" id="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfiguration.Initializer"></a>

```python
import { SetApiGatewayEndpointConfiguration } from '@cdklabs/cdk-enterprise-iac'

new SetApiGatewayEndpointConfiguration(props?: SetApiGatewayEndpointConfigurationProps)
```

| **Name** | **Type** | **Description** |
| --- | --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfiguration.Initializer.parameter.props">props</a></code> | <code><a href="#@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfigurationProps">SetApiGatewayEndpointConfigurationProps</a></code> | *No description.* |

---


##### `props`<sup>Optional</sup> <a name="props" id="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfiguration.Initializer.parameter.props"></a>

* *Type:* <a href="#@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfigurationProps">SetApiGatewayEndpointConfigurationProps</a>

---


#### Methods <a name="Methods" id="Methods"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfiguration.visit">visit</a></code> | All aspects can visit an IConstruct. |

---


##### `visit` <a name="visit" id="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfiguration.visit"></a>

```python
public visit(node: IConstruct): void
```

All aspects can visit an IConstruct.

###### `node`<sup>Required</sup> <a name="node" id="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfiguration.visit.parameter.node"></a>

* *Type:* constructs.IConstruct

---


## Enums <a name="Enums" id="Enums"></a>

### ProxyType <a name="ProxyType" id="@cdklabs/cdk-enterprise-iac.ProxyType"></a>

Whether an http-proxy or https-proxy.

#### Members <a name="Members" id="Members"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ProxyType.HTTP">HTTP</a></code> | --http-proxy. |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ProxyType.HTTPS">HTTPS</a></code> | --https-proxy. |

---


##### `HTTP` <a name="HTTP" id="@cdklabs/cdk-enterprise-iac.ProxyType.HTTP"></a>

-http-proxy.

---


##### `HTTPS` <a name="HTTPS" id="@cdklabs/cdk-enterprise-iac.ProxyType.HTTPS"></a>

-https-proxy.

---


### ResourceExtractorShareMethod <a name="ResourceExtractorShareMethod" id="@cdklabs/cdk-enterprise-iac.ResourceExtractorShareMethod"></a>

The available value sharing methods to pass values from the extracted stack onto the original stack(s).

#### Members <a name="Members" id="Members"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorShareMethod.CFN_OUTPUT">CFN_OUTPUT</a></code> | *No description.* |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorShareMethod.SSM_PARAMETER">SSM_PARAMETER</a></code> | *No description.* |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceExtractorShareMethod.API_LOOKUP">API_LOOKUP</a></code> | *No description.* |

---


##### `CFN_OUTPUT` <a name="CFN_OUTPUT" id="@cdklabs/cdk-enterprise-iac.ResourceExtractorShareMethod.CFN_OUTPUT"></a>

---


##### `SSM_PARAMETER` <a name="SSM_PARAMETER" id="@cdklabs/cdk-enterprise-iac.ResourceExtractorShareMethod.SSM_PARAMETER"></a>

---


##### `API_LOOKUP` <a name="API_LOOKUP" id="@cdklabs/cdk-enterprise-iac.ResourceExtractorShareMethod.API_LOOKUP"></a>

---


### ResourceTransform <a name="ResourceTransform" id="@cdklabs/cdk-enterprise-iac.ResourceTransform"></a>

#### Members <a name="Members" id="Members"></a>

| **Name** | **Description** |
| --- | --- |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceTransform.STACK_NAME">STACK_NAME</a></code> | *No description.* |
| <code><a href="#@cdklabs/cdk-enterprise-iac.ResourceTransform.LOGICAL_ID">LOGICAL_ID</a></code> | *No description.* |

---


##### `STACK_NAME` <a name="STACK_NAME" id="@cdklabs/cdk-enterprise-iac.ResourceTransform.STACK_NAME"></a>

---


##### `LOGICAL_ID` <a name="LOGICAL_ID" id="@cdklabs/cdk-enterprise-iac.ResourceTransform.LOGICAL_ID"></a>

---
</details>
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

import aws_cdk
import aws_cdk.aws_apigateway
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_secretsmanager
import aws_cdk.cx_api
import constructs


@jsii.implements(aws_cdk.IAspect)
class AddCfnInitProxy(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.AddCfnInitProxy",
):
    '''Add proxy configuration to Cloudformation helper functions.

    :extends: IAspect
    '''

    def __init__(
        self,
        *,
        proxy_host: builtins.str,
        proxy_port: jsii.Number,
        proxy_credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret] = None,
        proxy_type: typing.Optional["ProxyType"] = None,
    ) -> None:
        '''
        :param proxy_host: host of your proxy.
        :param proxy_port: proxy port.
        :param proxy_credentials: JSON secret containing ``user`` and ``password`` properties to use if your proxy requires credentials ``http://user:password@host:port`` could contain sensitive data, so using a Secret. Note that while the ``user`` and ``password`` won't be visible in the cloudformation template they **will** be in plain text inside your ``UserData``
        :param proxy_type: Proxy Type. Default: ProxyType.HTTP
        '''
        props = AddCfnInitProxyProps(
            proxy_host=proxy_host,
            proxy_port=proxy_port,
            proxy_credentials=proxy_credentials,
            proxy_type=proxy_type,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            def stub(node: constructs.IConstruct) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.AddCfnInitProxyProps",
    jsii_struct_bases=[],
    name_mapping={
        "proxy_host": "proxyHost",
        "proxy_port": "proxyPort",
        "proxy_credentials": "proxyCredentials",
        "proxy_type": "proxyType",
    },
)
class AddCfnInitProxyProps:
    def __init__(
        self,
        *,
        proxy_host: builtins.str,
        proxy_port: jsii.Number,
        proxy_credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret] = None,
        proxy_type: typing.Optional["ProxyType"] = None,
    ) -> None:
        '''Properties for the proxy server to use with cfn helper commands.

        :param proxy_host: host of your proxy.
        :param proxy_port: proxy port.
        :param proxy_credentials: JSON secret containing ``user`` and ``password`` properties to use if your proxy requires credentials ``http://user:password@host:port`` could contain sensitive data, so using a Secret. Note that while the ``user`` and ``password`` won't be visible in the cloudformation template they **will** be in plain text inside your ``UserData``
        :param proxy_type: Proxy Type. Default: ProxyType.HTTP
        '''
        if __debug__:
            def stub(
                *,
                proxy_host: builtins.str,
                proxy_port: jsii.Number,
                proxy_credentials: typing.Optional[aws_cdk.aws_secretsmanager.ISecret] = None,
                proxy_type: typing.Optional[ProxyType] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument proxy_host", value=proxy_host, expected_type=type_hints["proxy_host"])
            check_type(argname="argument proxy_port", value=proxy_port, expected_type=type_hints["proxy_port"])
            check_type(argname="argument proxy_credentials", value=proxy_credentials, expected_type=type_hints["proxy_credentials"])
            check_type(argname="argument proxy_type", value=proxy_type, expected_type=type_hints["proxy_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "proxy_host": proxy_host,
            "proxy_port": proxy_port,
        }
        if proxy_credentials is not None:
            self._values["proxy_credentials"] = proxy_credentials
        if proxy_type is not None:
            self._values["proxy_type"] = proxy_type

    @builtins.property
    def proxy_host(self) -> builtins.str:
        '''host of your proxy.

        Example::

            example.com
        '''
        result = self._values.get("proxy_host")
        assert result is not None, "Required property 'proxy_host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def proxy_port(self) -> jsii.Number:
        '''proxy port.

        Example::

            8080
        '''
        result = self._values.get("proxy_port")
        assert result is not None, "Required property 'proxy_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def proxy_credentials(self) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        '''JSON secret containing ``user`` and ``password`` properties to use if your proxy requires credentials ``http://user:password@host:port`` could contain sensitive data, so using a Secret.

        Note that while the ``user`` and ``password`` won't be visible in the cloudformation template
        they **will** be in plain text inside your ``UserData``

        Example::

            const secret = new Secret(stack, 'TestSecret', {
             secretObjectValue: {
               user: SecretValue,
               password: SecretValue,
             },
            });
        '''
        result = self._values.get("proxy_credentials")
        return typing.cast(typing.Optional[aws_cdk.aws_secretsmanager.ISecret], result)

    @builtins.property
    def proxy_type(self) -> typing.Optional["ProxyType"]:
        '''Proxy Type.

        :default: ProxyType.HTTP

        Example::

            ProxyType.HTTPS
        '''
        result = self._values.get("proxy_type")
        return typing.cast(typing.Optional["ProxyType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddCfnInitProxyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.IAspect)
class AddLambdaEnvironmentVariables(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.AddLambdaEnvironmentVariables",
):
    '''Add one or more environment variables to *all* lambda functions within a scope.

    :extends: IAspect
    '''

    def __init__(self, props: typing.Mapping[builtins.str, builtins.str]) -> None:
        '''
        :param props: : string} props - Key Value pair(s) for environment variables to add to all lambda functions.
        '''
        if __debug__:
            def stub(props: typing.Mapping[builtins.str, builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            def stub(node: constructs.IConstruct) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.implements(aws_cdk.IAspect)
class AddPermissionBoundary(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.AddPermissionBoundary",
):
    '''A patch for Adding Permissions Boundaries to all IAM roles.

    Additional options for adding prefixes to IAM role, policy and instance profile names

    Can account for non commercial partitions (e.g. aws-gov, aws-cn)
    '''

    def __init__(
        self,
        *,
        permissions_boundary_policy_name: builtins.str,
        instance_profile_prefix: typing.Optional[builtins.str] = None,
        policy_prefix: typing.Optional[builtins.str] = None,
        role_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param permissions_boundary_policy_name: Name of Permissions Boundary Policy to add to all IAM roles.
        :param instance_profile_prefix: A prefix to prepend to the name of the IAM InstanceProfiles (Default: '').
        :param policy_prefix: A prefix to prepend to the name of the IAM Policies and ManagedPolicies (Default: '').
        :param role_prefix: A prefix to prepend to the name of IAM Roles (Default: '').
        '''
        props = AddPermissionBoundaryProps(
            permissions_boundary_policy_name=permissions_boundary_policy_name,
            instance_profile_prefix=instance_profile_prefix,
            policy_prefix=policy_prefix,
            role_prefix=role_prefix,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="checkAndOverride")
    def check_and_override(
        self,
        node: aws_cdk.CfnResource,
        prefix: builtins.str,
        length: jsii.Number,
        cfn_prop: builtins.str,
        cdk_prop: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param node: -
        :param prefix: -
        :param length: -
        :param cfn_prop: -
        :param cdk_prop: -
        '''
        if __debug__:
            def stub(
                node: aws_cdk.CfnResource,
                prefix: builtins.str,
                length: jsii.Number,
                cfn_prop: builtins.str,
                cdk_prop: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument length", value=length, expected_type=type_hints["length"])
            check_type(argname="argument cfn_prop", value=cfn_prop, expected_type=type_hints["cfn_prop"])
            check_type(argname="argument cdk_prop", value=cdk_prop, expected_type=type_hints["cdk_prop"])
        return typing.cast(None, jsii.invoke(self, "checkAndOverride", [node, prefix, length, cfn_prop, cdk_prop]))

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            def stub(node: constructs.IConstruct) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.AddPermissionBoundaryProps",
    jsii_struct_bases=[],
    name_mapping={
        "permissions_boundary_policy_name": "permissionsBoundaryPolicyName",
        "instance_profile_prefix": "instanceProfilePrefix",
        "policy_prefix": "policyPrefix",
        "role_prefix": "rolePrefix",
    },
)
class AddPermissionBoundaryProps:
    def __init__(
        self,
        *,
        permissions_boundary_policy_name: builtins.str,
        instance_profile_prefix: typing.Optional[builtins.str] = None,
        policy_prefix: typing.Optional[builtins.str] = None,
        role_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties to pass to the AddPermissionBoundary.

        :param permissions_boundary_policy_name: Name of Permissions Boundary Policy to add to all IAM roles.
        :param instance_profile_prefix: A prefix to prepend to the name of the IAM InstanceProfiles (Default: '').
        :param policy_prefix: A prefix to prepend to the name of the IAM Policies and ManagedPolicies (Default: '').
        :param role_prefix: A prefix to prepend to the name of IAM Roles (Default: '').

        :interface: AddPermissionBoundaryProps
        '''
        if __debug__:
            def stub(
                *,
                permissions_boundary_policy_name: builtins.str,
                instance_profile_prefix: typing.Optional[builtins.str] = None,
                policy_prefix: typing.Optional[builtins.str] = None,
                role_prefix: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument permissions_boundary_policy_name", value=permissions_boundary_policy_name, expected_type=type_hints["permissions_boundary_policy_name"])
            check_type(argname="argument instance_profile_prefix", value=instance_profile_prefix, expected_type=type_hints["instance_profile_prefix"])
            check_type(argname="argument policy_prefix", value=policy_prefix, expected_type=type_hints["policy_prefix"])
            check_type(argname="argument role_prefix", value=role_prefix, expected_type=type_hints["role_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "permissions_boundary_policy_name": permissions_boundary_policy_name,
        }
        if instance_profile_prefix is not None:
            self._values["instance_profile_prefix"] = instance_profile_prefix
        if policy_prefix is not None:
            self._values["policy_prefix"] = policy_prefix
        if role_prefix is not None:
            self._values["role_prefix"] = role_prefix

    @builtins.property
    def permissions_boundary_policy_name(self) -> builtins.str:
        '''Name of Permissions Boundary Policy to add to all IAM roles.'''
        result = self._values.get("permissions_boundary_policy_name")
        assert result is not None, "Required property 'permissions_boundary_policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_profile_prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix to prepend to the name of the IAM InstanceProfiles (Default: '').'''
        result = self._values.get("instance_profile_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix to prepend to the name of the IAM Policies and ManagedPolicies (Default: '').'''
        result = self._values.get("policy_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix to prepend to the name of IAM Roles (Default: '').'''
        result = self._values.get("role_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddPermissionBoundaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.IAspect)
class ConvertInlinePoliciesToManaged(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.ConvertInlinePoliciesToManaged",
):
    '''Patch for turning all Policies into ConvertInlinePoliciesToManaged.

    Some users have policies in place that make it impossible to create inline policies. Instead,
    they must use managed policies.

    Note that order matters with this aspect. Specifically, it should generally be added first.
    This is because other aspects may add overrides that would be lost if applied before
    this aspect since the original aspect is removed and replaced.

    Example::

        // Replace all AWS::IAM::Policy resources with equivalent AWS::IAM::ManagedPolicy
        Aspects.of(stack).add(new ConvertInlinePoliciesToManaged())
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            def stub(node: constructs.IConstruct) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


class EcsIsoServiceAutoscaler(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscaler",
):
    '''Creates a EcsIsoServiceAutoscaler construct.

    This construct allows you to scale an ECS service in an ISO
    region where classic ECS Autoscaling may not be available.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        ecs_cluster: aws_cdk.aws_ecs.Cluster,
        ecs_service: aws_cdk.aws_ecs.IService,
        scale_alarm: aws_cdk.aws_cloudwatch.AlarmBase,
        maximum_task_count: typing.Optional[jsii.Number] = None,
        minimum_task_count: typing.Optional[jsii.Number] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        scale_in_cooldown: typing.Optional[aws_cdk.Duration] = None,
        scale_in_increment: typing.Optional[jsii.Number] = None,
        scale_out_cooldown: typing.Optional[aws_cdk.Duration] = None,
        scale_out_increment: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ecs_cluster: The cluster the service you wish to scale resides in.
        :param ecs_service: The ECS service you wish to scale.
        :param scale_alarm: The Cloudwatch Alarm that will cause scaling actions to be invoked, whether it's in or not in alarm will determine scale up and down actions. Note: composite alarms can not be generated with CFN in all regions, while this allows you to pass in a composite alarm alarm creation is outside the scope of this construct
        :param maximum_task_count: The maximum number of tasks that the service will scale out to. Note: This does not provide any protection from scaling out above the maximum allowed in your account, set this variable and manage account quotas appropriately. Default: 10
        :param minimum_task_count: The minimum number of tasks the service will have. Default: 1
        :param role: Optional IAM role to attach to the created lambda to adjust the desired count on the ECS Service. Ensure this role has appropriate privileges. Example IAM policy statements:: { "PolicyDocument": { "Statement": [ { "Action": "cloudwatch:DescribeAlarms", "Effect": "Allow", "Resource": "arn:${Partition}:cloudwatch:${Region}:${Account}:alarm:${AlarmName}" }, { "Action": [ "ecs:DescribeServices", "ecs:UpdateService" ], "Condition": { "StringEquals": { "ecs:cluster": "arn:${Partition}:ecs:${Region}:${Account}:cluster/${ClusterName}" } }, "Effect": "Allow", "Resource": "arn:${Partition}:ecs:${Region}:${Account}:service/${ClusterName}/${ServiceName}" } ], "Version": "2012-10-17" } } Default: A role is created for you with least privilege IAM policy
        :param scale_in_cooldown: How long will the application wait before performing another scale in action. Default: 60 seconds
        :param scale_in_increment: The number of tasks that will scale in on scale in alarm status. Default: 1
        :param scale_out_cooldown: How long will a the application wait before performing another scale out action. Default: 60 seconds
        :param scale_out_increment: The number of tasks that will scale out on scale out alarm status. Default: 1
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                ecs_cluster: aws_cdk.aws_ecs.Cluster,
                ecs_service: aws_cdk.aws_ecs.IService,
                scale_alarm: aws_cdk.aws_cloudwatch.AlarmBase,
                maximum_task_count: typing.Optional[jsii.Number] = None,
                minimum_task_count: typing.Optional[jsii.Number] = None,
                role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
                scale_in_cooldown: typing.Optional[aws_cdk.Duration] = None,
                scale_in_increment: typing.Optional[jsii.Number] = None,
                scale_out_cooldown: typing.Optional[aws_cdk.Duration] = None,
                scale_out_increment: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcsIsoServiceAutoscalerProps(
            ecs_cluster=ecs_cluster,
            ecs_service=ecs_service,
            scale_alarm=scale_alarm,
            maximum_task_count=maximum_task_count,
            minimum_task_count=minimum_task_count,
            role=role,
            scale_in_cooldown=scale_in_cooldown,
            scale_in_increment=scale_in_increment,
            scale_out_cooldown=scale_out_cooldown,
            scale_out_increment=scale_out_increment,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="ecsScalingManagerFunction")
    def ecs_scaling_manager_function(self) -> aws_cdk.aws_lambda.Function:
        return typing.cast(aws_cdk.aws_lambda.Function, jsii.get(self, "ecsScalingManagerFunction"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.EcsIsoServiceAutoscalerProps",
    jsii_struct_bases=[],
    name_mapping={
        "ecs_cluster": "ecsCluster",
        "ecs_service": "ecsService",
        "scale_alarm": "scaleAlarm",
        "maximum_task_count": "maximumTaskCount",
        "minimum_task_count": "minimumTaskCount",
        "role": "role",
        "scale_in_cooldown": "scaleInCooldown",
        "scale_in_increment": "scaleInIncrement",
        "scale_out_cooldown": "scaleOutCooldown",
        "scale_out_increment": "scaleOutIncrement",
    },
)
class EcsIsoServiceAutoscalerProps:
    def __init__(
        self,
        *,
        ecs_cluster: aws_cdk.aws_ecs.Cluster,
        ecs_service: aws_cdk.aws_ecs.IService,
        scale_alarm: aws_cdk.aws_cloudwatch.AlarmBase,
        maximum_task_count: typing.Optional[jsii.Number] = None,
        minimum_task_count: typing.Optional[jsii.Number] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        scale_in_cooldown: typing.Optional[aws_cdk.Duration] = None,
        scale_in_increment: typing.Optional[jsii.Number] = None,
        scale_out_cooldown: typing.Optional[aws_cdk.Duration] = None,
        scale_out_increment: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param ecs_cluster: The cluster the service you wish to scale resides in.
        :param ecs_service: The ECS service you wish to scale.
        :param scale_alarm: The Cloudwatch Alarm that will cause scaling actions to be invoked, whether it's in or not in alarm will determine scale up and down actions. Note: composite alarms can not be generated with CFN in all regions, while this allows you to pass in a composite alarm alarm creation is outside the scope of this construct
        :param maximum_task_count: The maximum number of tasks that the service will scale out to. Note: This does not provide any protection from scaling out above the maximum allowed in your account, set this variable and manage account quotas appropriately. Default: 10
        :param minimum_task_count: The minimum number of tasks the service will have. Default: 1
        :param role: Optional IAM role to attach to the created lambda to adjust the desired count on the ECS Service. Ensure this role has appropriate privileges. Example IAM policy statements:: { "PolicyDocument": { "Statement": [ { "Action": "cloudwatch:DescribeAlarms", "Effect": "Allow", "Resource": "arn:${Partition}:cloudwatch:${Region}:${Account}:alarm:${AlarmName}" }, { "Action": [ "ecs:DescribeServices", "ecs:UpdateService" ], "Condition": { "StringEquals": { "ecs:cluster": "arn:${Partition}:ecs:${Region}:${Account}:cluster/${ClusterName}" } }, "Effect": "Allow", "Resource": "arn:${Partition}:ecs:${Region}:${Account}:service/${ClusterName}/${ServiceName}" } ], "Version": "2012-10-17" } } Default: A role is created for you with least privilege IAM policy
        :param scale_in_cooldown: How long will the application wait before performing another scale in action. Default: 60 seconds
        :param scale_in_increment: The number of tasks that will scale in on scale in alarm status. Default: 1
        :param scale_out_cooldown: How long will a the application wait before performing another scale out action. Default: 60 seconds
        :param scale_out_increment: The number of tasks that will scale out on scale out alarm status. Default: 1
        '''
        if __debug__:
            def stub(
                *,
                ecs_cluster: aws_cdk.aws_ecs.Cluster,
                ecs_service: aws_cdk.aws_ecs.IService,
                scale_alarm: aws_cdk.aws_cloudwatch.AlarmBase,
                maximum_task_count: typing.Optional[jsii.Number] = None,
                minimum_task_count: typing.Optional[jsii.Number] = None,
                role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
                scale_in_cooldown: typing.Optional[aws_cdk.Duration] = None,
                scale_in_increment: typing.Optional[jsii.Number] = None,
                scale_out_cooldown: typing.Optional[aws_cdk.Duration] = None,
                scale_out_increment: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument ecs_cluster", value=ecs_cluster, expected_type=type_hints["ecs_cluster"])
            check_type(argname="argument ecs_service", value=ecs_service, expected_type=type_hints["ecs_service"])
            check_type(argname="argument scale_alarm", value=scale_alarm, expected_type=type_hints["scale_alarm"])
            check_type(argname="argument maximum_task_count", value=maximum_task_count, expected_type=type_hints["maximum_task_count"])
            check_type(argname="argument minimum_task_count", value=minimum_task_count, expected_type=type_hints["minimum_task_count"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument scale_in_cooldown", value=scale_in_cooldown, expected_type=type_hints["scale_in_cooldown"])
            check_type(argname="argument scale_in_increment", value=scale_in_increment, expected_type=type_hints["scale_in_increment"])
            check_type(argname="argument scale_out_cooldown", value=scale_out_cooldown, expected_type=type_hints["scale_out_cooldown"])
            check_type(argname="argument scale_out_increment", value=scale_out_increment, expected_type=type_hints["scale_out_increment"])
        self._values: typing.Dict[str, typing.Any] = {
            "ecs_cluster": ecs_cluster,
            "ecs_service": ecs_service,
            "scale_alarm": scale_alarm,
        }
        if maximum_task_count is not None:
            self._values["maximum_task_count"] = maximum_task_count
        if minimum_task_count is not None:
            self._values["minimum_task_count"] = minimum_task_count
        if role is not None:
            self._values["role"] = role
        if scale_in_cooldown is not None:
            self._values["scale_in_cooldown"] = scale_in_cooldown
        if scale_in_increment is not None:
            self._values["scale_in_increment"] = scale_in_increment
        if scale_out_cooldown is not None:
            self._values["scale_out_cooldown"] = scale_out_cooldown
        if scale_out_increment is not None:
            self._values["scale_out_increment"] = scale_out_increment

    @builtins.property
    def ecs_cluster(self) -> aws_cdk.aws_ecs.Cluster:
        '''The cluster the service you wish to scale resides in.'''
        result = self._values.get("ecs_cluster")
        assert result is not None, "Required property 'ecs_cluster' is missing"
        return typing.cast(aws_cdk.aws_ecs.Cluster, result)

    @builtins.property
    def ecs_service(self) -> aws_cdk.aws_ecs.IService:
        '''The ECS service you wish to scale.'''
        result = self._values.get("ecs_service")
        assert result is not None, "Required property 'ecs_service' is missing"
        return typing.cast(aws_cdk.aws_ecs.IService, result)

    @builtins.property
    def scale_alarm(self) -> aws_cdk.aws_cloudwatch.AlarmBase:
        '''The Cloudwatch Alarm that will cause scaling actions to be invoked, whether it's in or not in alarm will determine scale up and down actions.

        Note: composite alarms can not be generated with CFN in all regions, while this allows you to pass in a composite alarm alarm creation is outside the scope of this construct
        '''
        result = self._values.get("scale_alarm")
        assert result is not None, "Required property 'scale_alarm' is missing"
        return typing.cast(aws_cdk.aws_cloudwatch.AlarmBase, result)

    @builtins.property
    def maximum_task_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of tasks that the service will scale out to.

        Note: This does not provide any protection from scaling out above the maximum allowed in your account, set this variable and manage account quotas appropriately.

        :default: 10
        '''
        result = self._values.get("maximum_task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_task_count(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of tasks the service will have.

        :default: 1
        '''
        result = self._values.get("minimum_task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''Optional IAM role to attach to the created lambda to adjust the desired count on the ECS Service.

        Ensure this role has appropriate privileges. Example IAM policy statements::

           {
             "PolicyDocument": {
               "Statement": [
                 {
                   "Action": "cloudwatch:DescribeAlarms",
                   "Effect": "Allow",
                   "Resource": "arn:${Partition}:cloudwatch:${Region}:${Account}:alarm:${AlarmName}"
                 },
                 {
                   "Action": [
                     "ecs:DescribeServices",
                     "ecs:UpdateService"
                   ],
                   "Condition": {
                     "StringEquals": {
                       "ecs:cluster": "arn:${Partition}:ecs:${Region}:${Account}:cluster/${ClusterName}"
                     }
                   },
                   "Effect": "Allow",
                   "Resource": "arn:${Partition}:ecs:${Region}:${Account}:service/${ClusterName}/${ServiceName}"
                 }
               ],
               "Version": "2012-10-17"
             }
           }

        :default: A role is created for you with least privilege IAM policy
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def scale_in_cooldown(self) -> typing.Optional[aws_cdk.Duration]:
        '''How long will the application wait before performing another scale in action.

        :default: 60 seconds
        '''
        result = self._values.get("scale_in_cooldown")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def scale_in_increment(self) -> typing.Optional[jsii.Number]:
        '''The number of tasks that will scale in on scale in alarm status.

        :default: 1
        '''
        result = self._values.get("scale_in_increment")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scale_out_cooldown(self) -> typing.Optional[aws_cdk.Duration]:
        '''How long will a the application wait before performing another scale out action.

        :default: 60 seconds
        '''
        result = self._values.get("scale_out_cooldown")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def scale_out_increment(self) -> typing.Optional[jsii.Number]:
        '''The number of tasks that will scale out on scale out alarm status.

        :default: 1
        '''
        result = self._values.get("scale_out_increment")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsIsoServiceAutoscalerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PopulateWithConfig(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.PopulateWithConfig",
):
    '''Populate a provided VPC with subnets based on a provided configuration.

    Example::

        const mySubnetConfig: SubnetConfig[] = [
           {
             groupName: 'app',
             cidrRange: '172.31.0.0/27',
             availabilityZone: 'a',
             subnetType: subnetType.PUBLIC,
           },
           {
             groupName: 'app',
             cidrRange: '172.31.0.32/27',
             availabilityZone: 'b',
             subnetType: subnetType.PUBLIC,
           },
           {
             groupName: 'db',
             cidrRange: '172.31.0.64/27',
             availabilityZone: 'a',
             subnetType: subnetType.PRIVATE_WITH_EGRESS,
           },
           {
             groupName: 'db',
             cidrRange: '172.31.0.96/27',
             availabilityZone: 'b',
             subnetType: subnetType.PRIVATE_WITH_EGRESS,
           },
           {
             groupName: 'iso',
             cidrRange: '172.31.0.128/26',
             availabilityZone: 'a',
             subnetType: subnetType.PRIVATE_ISOLATED,
           },
           {
             groupName: 'iso',
             cidrRange: '172.31.0.196/26',
             availabilityZone: 'b',
             subnetType: subnetType.PRIVATE_ISOLATED,
           },
         ];
        new PopulateWithConfig(this, "vpcPopulater", {
          vpcId: 'vpc-abcdefg1234567',
          privateRouteTableId: 'rt-abcdefg123456',
          localRouteTableId: 'rt-123456abcdefg',
          subnetConfig: mySubnetConfig,
        })
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        local_route_table_id: builtins.str,
        private_route_table_id: builtins.str,
        subnet_config: typing.Sequence[typing.Union["SubnetConfig", typing.Dict[str, typing.Any]]],
        vpc_id: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param local_route_table_id: Local route table ID, with routes only to local VPC.
        :param private_route_table_id: Route table ID for a provided route table with routes to enterprise network. Both subnetType.PUBLIC and subnetType.PRIVATE_WITH_EGRESS will use this property
        :param subnet_config: List of Subnet configs to provision to provision.
        :param vpc_id: ID of the VPC provided that needs to be populated.
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                local_route_table_id: builtins.str,
                private_route_table_id: builtins.str,
                subnet_config: typing.Sequence[typing.Union[SubnetConfig, typing.Dict[str, typing.Any]]],
                vpc_id: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PopulateWithConfigProps(
            local_route_table_id=local_route_table_id,
            private_route_table_id=private_route_table_id,
            subnet_config=subnet_config,
            vpc_id=vpc_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.PopulateWithConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "local_route_table_id": "localRouteTableId",
        "private_route_table_id": "privateRouteTableId",
        "subnet_config": "subnetConfig",
        "vpc_id": "vpcId",
    },
)
class PopulateWithConfigProps:
    def __init__(
        self,
        *,
        local_route_table_id: builtins.str,
        private_route_table_id: builtins.str,
        subnet_config: typing.Sequence[typing.Union["SubnetConfig", typing.Dict[str, typing.Any]]],
        vpc_id: builtins.str,
    ) -> None:
        '''
        :param local_route_table_id: Local route table ID, with routes only to local VPC.
        :param private_route_table_id: Route table ID for a provided route table with routes to enterprise network. Both subnetType.PUBLIC and subnetType.PRIVATE_WITH_EGRESS will use this property
        :param subnet_config: List of Subnet configs to provision to provision.
        :param vpc_id: ID of the VPC provided that needs to be populated.
        '''
        if __debug__:
            def stub(
                *,
                local_route_table_id: builtins.str,
                private_route_table_id: builtins.str,
                subnet_config: typing.Sequence[typing.Union[SubnetConfig, typing.Dict[str, typing.Any]]],
                vpc_id: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument local_route_table_id", value=local_route_table_id, expected_type=type_hints["local_route_table_id"])
            check_type(argname="argument private_route_table_id", value=private_route_table_id, expected_type=type_hints["private_route_table_id"])
            check_type(argname="argument subnet_config", value=subnet_config, expected_type=type_hints["subnet_config"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "local_route_table_id": local_route_table_id,
            "private_route_table_id": private_route_table_id,
            "subnet_config": subnet_config,
            "vpc_id": vpc_id,
        }

    @builtins.property
    def local_route_table_id(self) -> builtins.str:
        '''Local route table ID, with routes only to local VPC.'''
        result = self._values.get("local_route_table_id")
        assert result is not None, "Required property 'local_route_table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_route_table_id(self) -> builtins.str:
        '''Route table ID for a provided route table with routes to enterprise network.

        Both subnetType.PUBLIC and subnetType.PRIVATE_WITH_EGRESS will use this property
        '''
        result = self._values.get("private_route_table_id")
        assert result is not None, "Required property 'private_route_table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_config(self) -> typing.List["SubnetConfig"]:
        '''List of Subnet configs to provision to provision.'''
        result = self._values.get("subnet_config")
        assert result is not None, "Required property 'subnet_config' is missing"
        return typing.cast(typing.List["SubnetConfig"], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''ID of the VPC provided that needs to be populated.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PopulateWithConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/cdk-enterprise-iac.ProxyType")
class ProxyType(enum.Enum):
    '''Whether an http-proxy or https-proxy.'''

    HTTP = "HTTP"
    '''--http-proxy.'''
    HTTPS = "HTTPS"
    '''--https-proxy.'''


@jsii.implements(aws_cdk.IAspect)
class RemovePublicAccessBlockConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.RemovePublicAccessBlockConfiguration",
):
    '''Looks for S3 Buckets, and removes the ``PublicAccessBlockConfiguration`` property.

    For use in regions where Cloudformation doesn't support this property
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            def stub(node: constructs.IConstruct) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.implements(aws_cdk.IAspect)
class RemoveTags(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.RemoveTags",
):
    '''Patch for removing tags from a specific Cloudformation Resource.

    In some regions, the 'Tags' property isn't supported in Cloudformation. This patch makes it easy to remove

    Example::

        // Remove tags on a resource
        Aspects.of(stack).add(new RemoveTags({
          cloudformationResource: 'AWS::ECS::Cluster',
        }));
        // Remove tags without the standard 'Tags' name
        Aspects.of(stack).add(new RemoveTags({
          cloudformationResource: 'AWS::Backup::BackupPlan',
           tagPropertyName: 'BackupPlanTags',
        }));
    '''

    def __init__(
        self,
        *,
        cloudformation_resource: builtins.str,
        tag_property_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloudformation_resource: Name of Cloudformation resource Type (e.g. 'AWS::Lambda::Function').
        :param tag_property_name: Name of the tag property to remove from the resource. Default: Tags
        '''
        props = RemoveTagsProps(
            cloudformation_resource=cloudformation_resource,
            tag_property_name=tag_property_name,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            def stub(node: constructs.IConstruct) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.RemoveTagsProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloudformation_resource": "cloudformationResource",
        "tag_property_name": "tagPropertyName",
    },
)
class RemoveTagsProps:
    def __init__(
        self,
        *,
        cloudformation_resource: builtins.str,
        tag_property_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloudformation_resource: Name of Cloudformation resource Type (e.g. 'AWS::Lambda::Function').
        :param tag_property_name: Name of the tag property to remove from the resource. Default: Tags
        '''
        if __debug__:
            def stub(
                *,
                cloudformation_resource: builtins.str,
                tag_property_name: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument cloudformation_resource", value=cloudformation_resource, expected_type=type_hints["cloudformation_resource"])
            check_type(argname="argument tag_property_name", value=tag_property_name, expected_type=type_hints["tag_property_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "cloudformation_resource": cloudformation_resource,
        }
        if tag_property_name is not None:
            self._values["tag_property_name"] = tag_property_name

    @builtins.property
    def cloudformation_resource(self) -> builtins.str:
        '''Name of Cloudformation resource Type (e.g. 'AWS::Lambda::Function').'''
        result = self._values.get("cloudformation_resource")
        assert result is not None, "Required property 'cloudformation_resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_property_name(self) -> typing.Optional[builtins.str]:
        '''Name of the tag property to remove from the resource.

        :default: Tags
        '''
        result = self._values.get("tag_property_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoveTagsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.IAspect)
class ResourceExtractor(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.ResourceExtractor",
):
    '''This Aspect takes a CDK application, all synthesized CloudFormationStackArtifact, a value share method, and a list of Cloudformation resources that should be pulled out of the main CDK application, which should be synthesized to a cloudformation template that an external team (e.g. security team) to deploy, and adjusting the CDK application to reference pre-created resources already pulled out.

    Example::

         const app = App()
         const stack = new Stack(app, 'MyStack');
         extractedStack = new Stack(app, 'ExtractedStack');
         const synthedApp = app.synth();
         Aspects.of(app).add(new ResourceExtractor({
           extractDestinationStack: extractedStack,
           stackArtifacts: synthedApp.stacks,
           valueShareMethod: ResourceExtractorShareMethod.CFN_OUTPUT,
           resourceTypesToExtract: [
             'AWS::IAM::Role',
             'AWS::IAM::Policy',
             'AWS::IAM::ManagedPolicy',
             'AWS::IAM::InstanceProfile',
           ],
         });
         app.synth({ force: true });
    '''

    def __init__(
        self,
        *,
        extract_destination_stack: aws_cdk.Stack,
        resource_types_to_extract: typing.Sequence[builtins.str],
        stack_artifacts: typing.Sequence[aws_cdk.cx_api.CloudFormationStackArtifact],
        additional_transforms: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        value_share_method: typing.Optional["ResourceExtractorShareMethod"] = None,
    ) -> None:
        '''
        :param extract_destination_stack: Stack to move found extracted resources into.
        :param resource_types_to_extract: List of resource types to extract, ex: ``AWS::IAM::Role``.
        :param stack_artifacts: Synthed stack artifacts from your CDK app.
        :param additional_transforms: Additional resource transformations.
        :param value_share_method: The sharing method to use when passing exported resources from the "Extracted Stack" into the original stack(s).
        '''
        props = ResourceExtractorProps(
            extract_destination_stack=extract_destination_stack,
            resource_types_to_extract=resource_types_to_extract,
            stack_artifacts=stack_artifacts,
            additional_transforms=additional_transforms,
            value_share_method=value_share_method,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''Entrypoint.

        :param node: -
        '''
        if __debug__:
            def stub(node: constructs.IConstruct) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.ResourceExtractorProps",
    jsii_struct_bases=[],
    name_mapping={
        "extract_destination_stack": "extractDestinationStack",
        "resource_types_to_extract": "resourceTypesToExtract",
        "stack_artifacts": "stackArtifacts",
        "additional_transforms": "additionalTransforms",
        "value_share_method": "valueShareMethod",
    },
)
class ResourceExtractorProps:
    def __init__(
        self,
        *,
        extract_destination_stack: aws_cdk.Stack,
        resource_types_to_extract: typing.Sequence[builtins.str],
        stack_artifacts: typing.Sequence[aws_cdk.cx_api.CloudFormationStackArtifact],
        additional_transforms: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        value_share_method: typing.Optional["ResourceExtractorShareMethod"] = None,
    ) -> None:
        '''
        :param extract_destination_stack: Stack to move found extracted resources into.
        :param resource_types_to_extract: List of resource types to extract, ex: ``AWS::IAM::Role``.
        :param stack_artifacts: Synthed stack artifacts from your CDK app.
        :param additional_transforms: Additional resource transformations.
        :param value_share_method: The sharing method to use when passing exported resources from the "Extracted Stack" into the original stack(s).
        '''
        if __debug__:
            def stub(
                *,
                extract_destination_stack: aws_cdk.Stack,
                resource_types_to_extract: typing.Sequence[builtins.str],
                stack_artifacts: typing.Sequence[aws_cdk.cx_api.CloudFormationStackArtifact],
                additional_transforms: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                value_share_method: typing.Optional[ResourceExtractorShareMethod] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument extract_destination_stack", value=extract_destination_stack, expected_type=type_hints["extract_destination_stack"])
            check_type(argname="argument resource_types_to_extract", value=resource_types_to_extract, expected_type=type_hints["resource_types_to_extract"])
            check_type(argname="argument stack_artifacts", value=stack_artifacts, expected_type=type_hints["stack_artifacts"])
            check_type(argname="argument additional_transforms", value=additional_transforms, expected_type=type_hints["additional_transforms"])
            check_type(argname="argument value_share_method", value=value_share_method, expected_type=type_hints["value_share_method"])
        self._values: typing.Dict[str, typing.Any] = {
            "extract_destination_stack": extract_destination_stack,
            "resource_types_to_extract": resource_types_to_extract,
            "stack_artifacts": stack_artifacts,
        }
        if additional_transforms is not None:
            self._values["additional_transforms"] = additional_transforms
        if value_share_method is not None:
            self._values["value_share_method"] = value_share_method

    @builtins.property
    def extract_destination_stack(self) -> aws_cdk.Stack:
        '''Stack to move found extracted resources into.'''
        result = self._values.get("extract_destination_stack")
        assert result is not None, "Required property 'extract_destination_stack' is missing"
        return typing.cast(aws_cdk.Stack, result)

    @builtins.property
    def resource_types_to_extract(self) -> typing.List[builtins.str]:
        '''List of resource types to extract, ex: ``AWS::IAM::Role``.'''
        result = self._values.get("resource_types_to_extract")
        assert result is not None, "Required property 'resource_types_to_extract' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def stack_artifacts(
        self,
    ) -> typing.List[aws_cdk.cx_api.CloudFormationStackArtifact]:
        '''Synthed stack artifacts from your CDK app.'''
        result = self._values.get("stack_artifacts")
        assert result is not None, "Required property 'stack_artifacts' is missing"
        return typing.cast(typing.List[aws_cdk.cx_api.CloudFormationStackArtifact], result)

    @builtins.property
    def additional_transforms(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional resource transformations.'''
        result = self._values.get("additional_transforms")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def value_share_method(self) -> typing.Optional["ResourceExtractorShareMethod"]:
        '''The sharing method to use when passing exported resources from the "Extracted Stack" into the original stack(s).'''
        result = self._values.get("value_share_method")
        return typing.cast(typing.Optional["ResourceExtractorShareMethod"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceExtractorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/cdk-enterprise-iac.ResourceExtractorShareMethod")
class ResourceExtractorShareMethod(enum.Enum):
    '''The available value sharing methods to pass values from the extracted stack onto the original stack(s).'''

    CFN_OUTPUT = "CFN_OUTPUT"
    SSM_PARAMETER = "SSM_PARAMETER"
    API_LOOKUP = "API_LOOKUP"


@jsii.enum(jsii_type="@cdklabs/cdk-enterprise-iac.ResourceTransform")
class ResourceTransform(enum.Enum):
    STACK_NAME = "STACK_NAME"
    LOGICAL_ID = "LOGICAL_ID"


@jsii.implements(aws_cdk.IAspect)
class SetApiGatewayEndpointConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfiguration",
):
    '''Override RestApis to use a set endpoint configuration.

    Some regions don't support EDGE endpoints, and some enterprises require
    specific endpoint types for RestApis
    '''

    def __init__(
        self,
        *,
        endpoint_type: typing.Optional[aws_cdk.aws_apigateway.EndpointType] = None,
    ) -> None:
        '''
        :param endpoint_type: API Gateway endpoint type to override to. Defaults to EndpointType.REGIONAL Default: EndpointType.REGIONAL
        '''
        props = SetApiGatewayEndpointConfigurationProps(endpoint_type=endpoint_type)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            def stub(node: constructs.IConstruct) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.SetApiGatewayEndpointConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={"endpoint_type": "endpointType"},
)
class SetApiGatewayEndpointConfigurationProps:
    def __init__(
        self,
        *,
        endpoint_type: typing.Optional[aws_cdk.aws_apigateway.EndpointType] = None,
    ) -> None:
        '''
        :param endpoint_type: API Gateway endpoint type to override to. Defaults to EndpointType.REGIONAL Default: EndpointType.REGIONAL
        '''
        if __debug__:
            def stub(
                *,
                endpoint_type: typing.Optional[aws_cdk.aws_apigateway.EndpointType] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
        self._values: typing.Dict[str, typing.Any] = {}
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type

    @builtins.property
    def endpoint_type(self) -> typing.Optional[aws_cdk.aws_apigateway.EndpointType]:
        '''API Gateway endpoint type to override to.

        Defaults to EndpointType.REGIONAL

        :default: EndpointType.REGIONAL
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[aws_cdk.aws_apigateway.EndpointType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetApiGatewayEndpointConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SplitVpcEvenly(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-enterprise-iac.SplitVpcEvenly",
):
    '''Splits a VPC evenly between a provided number of AZs (3 if not defined), and attaches a provided route table to each, and labels.

    Example::

        // with more specific properties
        new SplitVpcEvenly(this, 'evenSplitVpc', {
          vpcId: 'vpc-abcdefg123456',
          vpcCidr: '172.16.0.0/16',
          routeTableId: 'rt-abcdefgh123456',
          cidrBits: '10',
          numberOfAzs: 4,
          subnetType: subnetType.PRIVATE_ISOLATED,
        });
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        route_table_id: builtins.str,
        vpc_cidr: builtins.str,
        vpc_id: builtins.str,
        cidr_bits: typing.Optional[builtins.str] = None,
        number_of_azs: typing.Optional[jsii.Number] = None,
        subnet_type: typing.Optional[aws_cdk.aws_ec2.SubnetType] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param route_table_id: Route Table ID that will be attached to each subnet created.
        :param vpc_cidr: CIDR range of the VPC you're populating.
        :param vpc_id: ID of the existing VPC you're trying to populate.
        :param cidr_bits: ``cidrBits`` argument for the ```Fn::Cidr`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-cidr.html>`_ Cloudformation intrinsic function. Default: '6'
        :param number_of_azs: Number of AZs to evenly split into. Default: 3
        :param subnet_type: Default: subnetType.PRIVATE
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                route_table_id: builtins.str,
                vpc_cidr: builtins.str,
                vpc_id: builtins.str,
                cidr_bits: typing.Optional[builtins.str] = None,
                number_of_azs: typing.Optional[jsii.Number] = None,
                subnet_type: typing.Optional[aws_cdk.aws_ec2.SubnetType] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SplitVpcEvenlyProps(
            route_table_id=route_table_id,
            vpc_cidr=vpc_cidr,
            vpc_id=vpc_id,
            cidr_bits=cidr_bits,
            number_of_azs=number_of_azs,
            subnet_type=subnet_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.SplitVpcEvenlyProps",
    jsii_struct_bases=[],
    name_mapping={
        "route_table_id": "routeTableId",
        "vpc_cidr": "vpcCidr",
        "vpc_id": "vpcId",
        "cidr_bits": "cidrBits",
        "number_of_azs": "numberOfAzs",
        "subnet_type": "subnetType",
    },
)
class SplitVpcEvenlyProps:
    def __init__(
        self,
        *,
        route_table_id: builtins.str,
        vpc_cidr: builtins.str,
        vpc_id: builtins.str,
        cidr_bits: typing.Optional[builtins.str] = None,
        number_of_azs: typing.Optional[jsii.Number] = None,
        subnet_type: typing.Optional[aws_cdk.aws_ec2.SubnetType] = None,
    ) -> None:
        '''
        :param route_table_id: Route Table ID that will be attached to each subnet created.
        :param vpc_cidr: CIDR range of the VPC you're populating.
        :param vpc_id: ID of the existing VPC you're trying to populate.
        :param cidr_bits: ``cidrBits`` argument for the ```Fn::Cidr`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-cidr.html>`_ Cloudformation intrinsic function. Default: '6'
        :param number_of_azs: Number of AZs to evenly split into. Default: 3
        :param subnet_type: Default: subnetType.PRIVATE
        '''
        if __debug__:
            def stub(
                *,
                route_table_id: builtins.str,
                vpc_cidr: builtins.str,
                vpc_id: builtins.str,
                cidr_bits: typing.Optional[builtins.str] = None,
                number_of_azs: typing.Optional[jsii.Number] = None,
                subnet_type: typing.Optional[aws_cdk.aws_ec2.SubnetType] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument route_table_id", value=route_table_id, expected_type=type_hints["route_table_id"])
            check_type(argname="argument vpc_cidr", value=vpc_cidr, expected_type=type_hints["vpc_cidr"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument cidr_bits", value=cidr_bits, expected_type=type_hints["cidr_bits"])
            check_type(argname="argument number_of_azs", value=number_of_azs, expected_type=type_hints["number_of_azs"])
            check_type(argname="argument subnet_type", value=subnet_type, expected_type=type_hints["subnet_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "route_table_id": route_table_id,
            "vpc_cidr": vpc_cidr,
            "vpc_id": vpc_id,
        }
        if cidr_bits is not None:
            self._values["cidr_bits"] = cidr_bits
        if number_of_azs is not None:
            self._values["number_of_azs"] = number_of_azs
        if subnet_type is not None:
            self._values["subnet_type"] = subnet_type

    @builtins.property
    def route_table_id(self) -> builtins.str:
        '''Route Table ID that will be attached to each subnet created.'''
        result = self._values.get("route_table_id")
        assert result is not None, "Required property 'route_table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_cidr(self) -> builtins.str:
        '''CIDR range of the VPC you're populating.'''
        result = self._values.get("vpc_cidr")
        assert result is not None, "Required property 'vpc_cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''ID of the existing VPC you're trying to populate.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cidr_bits(self) -> typing.Optional[builtins.str]:
        '''``cidrBits`` argument for the ```Fn::Cidr`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-cidr.html>`_ Cloudformation intrinsic function.

        :default: '6'
        '''
        result = self._values.get("cidr_bits")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def number_of_azs(self) -> typing.Optional[jsii.Number]:
        '''Number of AZs to evenly split into.

        :default: 3
        '''
        result = self._values.get("number_of_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def subnet_type(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetType]:
        '''
        :default: subnetType.PRIVATE
        '''
        result = self._values.get("subnet_type")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SplitVpcEvenlyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdklabs/cdk-enterprise-iac.SubnetConfig",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "cidr_range": "cidrRange",
        "group_name": "groupName",
        "subnet_type": "subnetType",
    },
)
class SubnetConfig:
    def __init__(
        self,
        *,
        availability_zone: builtins.str,
        cidr_range: builtins.str,
        group_name: builtins.str,
        subnet_type: aws_cdk.aws_ec2.SubnetType,
    ) -> None:
        '''
        :param availability_zone: Which availability zone the subnet should be in.
        :param cidr_range: Cidr range of the subnet to create.
        :param group_name: Logical group name of a subnet.
        :param subnet_type: What `SubnetType <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.SubnetType.html>`_ to use. This will govern the ``aws-cdk:subnet-type`` tag on the subnet SubnetType | ``aws-cdk:subnet-type`` tag value --- | --- ``PRIVATE_ISOLATED`` | 'Isolated' ``PRIVATE_WITH_EGRESS`` | 'Private' ``PUBLIC`` | 'Public'
        '''
        if __debug__:
            def stub(
                *,
                availability_zone: builtins.str,
                cidr_range: builtins.str,
                group_name: builtins.str,
                subnet_type: aws_cdk.aws_ec2.SubnetType,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument cidr_range", value=cidr_range, expected_type=type_hints["cidr_range"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument subnet_type", value=subnet_type, expected_type=type_hints["subnet_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "availability_zone": availability_zone,
            "cidr_range": cidr_range,
            "group_name": group_name,
            "subnet_type": subnet_type,
        }

    @builtins.property
    def availability_zone(self) -> builtins.str:
        '''Which availability zone the subnet should be in.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cidr_range(self) -> builtins.str:
        '''Cidr range of the subnet to create.'''
        result = self._values.get("cidr_range")
        assert result is not None, "Required property 'cidr_range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_name(self) -> builtins.str:
        '''Logical group name of a subnet.

        Example::

            db
        '''
        result = self._values.get("group_name")
        assert result is not None, "Required property 'group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_type(self) -> aws_cdk.aws_ec2.SubnetType:
        '''What `SubnetType <https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2.SubnetType.html>`_ to use.

        This will govern the ``aws-cdk:subnet-type`` tag on the subnet

        SubnetType | ``aws-cdk:subnet-type`` tag value
        --- | ---
        ``PRIVATE_ISOLATED`` | 'Isolated'
        ``PRIVATE_WITH_EGRESS`` | 'Private'
        ``PUBLIC`` | 'Public'
        '''
        result = self._values.get("subnet_type")
        assert result is not None, "Required property 'subnet_type' is missing"
        return typing.cast(aws_cdk.aws_ec2.SubnetType, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubnetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddCfnInitProxy",
    "AddCfnInitProxyProps",
    "AddLambdaEnvironmentVariables",
    "AddPermissionBoundary",
    "AddPermissionBoundaryProps",
    "ConvertInlinePoliciesToManaged",
    "EcsIsoServiceAutoscaler",
    "EcsIsoServiceAutoscalerProps",
    "PopulateWithConfig",
    "PopulateWithConfigProps",
    "ProxyType",
    "RemovePublicAccessBlockConfiguration",
    "RemoveTags",
    "RemoveTagsProps",
    "ResourceExtractor",
    "ResourceExtractorProps",
    "ResourceExtractorShareMethod",
    "ResourceTransform",
    "SetApiGatewayEndpointConfiguration",
    "SetApiGatewayEndpointConfigurationProps",
    "SplitVpcEvenly",
    "SplitVpcEvenlyProps",
    "SubnetConfig",
]

publication.publish()
