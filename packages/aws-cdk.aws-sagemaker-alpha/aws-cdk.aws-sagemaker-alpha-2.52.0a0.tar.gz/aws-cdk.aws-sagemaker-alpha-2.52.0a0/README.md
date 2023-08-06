# Amazon SageMaker Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

Amazon SageMaker provides every developer and data scientist with the ability to build, train, and
deploy machine learning models quickly. Amazon SageMaker is a fully-managed service that covers the
entire machine learning workflow to label and prepare your data, choose an algorithm, train the
model, tune and optimize it for deployment, make predictions, and take action. Your models get to
production faster with much less effort and lower cost.

## Installation

Install the module:

```console
$ npm i @aws-cdk/aws-sagemaker
```

Import it into your code:

```python
import aws_cdk.aws_sagemaker_alpha as sagemaker
```

## Model

To create a machine learning model with Amazon Sagemaker, use the `Model` construct. This construct
includes properties that can be configured to define model components, including the model inference
code as a Docker image and an optional set of separate model data artifacts. See the [AWS
documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-marketplace-develop.html)
to learn more about SageMaker models.

### Single Container Model

In the event that a single container is sufficient for your inference use-case, you can define a
single-container model:

```python
import aws_cdk.aws_sagemaker_alpha as sagemaker
import path as path


image = sagemaker.ContainerImage.from_asset(path.join("path", "to", "Dockerfile", "directory"))
model_data = sagemaker.ModelData.from_asset(path.join("path", "to", "artifact", "file.tar.gz"))

model = sagemaker.Model(self, "PrimaryContainerModel",
    containers=[sagemaker.ContainerDefinition(
        image=image,
        model_data=model_data
    )
    ]
)
```

### Inference Pipeline Model

An inference pipeline is an Amazon SageMaker model that is composed of a linear sequence of multiple
containers that process requests for inferences on data. See the [AWS
documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/inference-pipelines.html) to learn
more about SageMaker inference pipelines. To define an inference pipeline, you can provide
additional containers for your model:

```python
import aws_cdk.aws_sagemaker_alpha as sagemaker

# image1: sagemaker.ContainerImage
# model_data1: sagemaker.ModelData
# image2: sagemaker.ContainerImage
# model_data2: sagemaker.ModelData
# image3: sagemaker.ContainerImage
# model_data3: sagemaker.ModelData


model = sagemaker.Model(self, "InferencePipelineModel",
    containers=[sagemaker.ContainerDefinition(image=image1, model_data=model_data1), sagemaker.ContainerDefinition(image=image2, model_data=model_data2), sagemaker.ContainerDefinition(image=image3, model_data=model_data3)
    ]
)
```

### Container Images

Inference code can be stored in the Amazon EC2 Container Registry (Amazon ECR), which is specified
via `ContainerDefinition`'s `image` property which accepts a class that extends the `ContainerImage`
abstract base class.

#### Asset Image

Reference a local directory containing a Dockerfile:

```python
import aws_cdk.aws_sagemaker_alpha as sagemaker
import path as path


image = sagemaker.ContainerImage.from_asset(path.join("path", "to", "Dockerfile", "directory"))
```

#### ECR Image

Reference an image available within ECR:

```python
import aws_cdk.aws_ecr as ecr
import aws_cdk.aws_sagemaker_alpha as sagemaker


repository = ecr.Repository.from_repository_name(self, "Repository", "repo")
image = sagemaker.ContainerImage.from_ecr_repository(repository, "tag")
```

### Model Artifacts

If you choose to decouple your model artifacts from your inference code (as is natural given
different rates of change between inference code and model artifacts), the artifacts can be
specified via the `modelData` property which accepts a class that extends the `ModelData` abstract
base class. The default is to have no model artifacts associated with a model.

#### Asset Model Data

Reference local model data:

```python
import aws_cdk.aws_sagemaker_alpha as sagemaker
import path as path


model_data = sagemaker.ModelData.from_asset(path.join("path", "to", "artifact", "file.tar.gz"))
```

#### S3 Model Data

Reference an S3 bucket and object key as the artifacts for a model:

```python
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_sagemaker_alpha as sagemaker


bucket = s3.Bucket(self, "MyBucket")
model_data = sagemaker.ModelData.from_bucket(bucket, "path/to/artifact/file.tar.gz")
```

## Model Hosting

Amazon SageMaker provides model hosting services for model deployment. Amazon SageMaker provides an
HTTPS endpoint where your machine learning model is available to provide inferences.

### Endpoint Configuration

By using the `EndpointConfig` construct, you can define a set of endpoint configuration which can be
used to provision one or more endpoints. In this configuration, you identify one or more models to
deploy and the resources that you want Amazon SageMaker to provision. You define one or more
production variants, each of which identifies a model. Each production variant also describes the
resources that you want Amazon SageMaker to provision. If you are hosting multiple models, you also
assign a variant weight to specify how much traffic you want to allocate to each model. For example,
suppose that you want to host two models, A and B, and you assign traffic weight 2 for model A and 1
for model B. Amazon SageMaker distributes two-thirds of the traffic to Model A, and one-third to
model B:

```python
import aws_cdk.aws_sagemaker_alpha as sagemaker

# model_a: sagemaker.Model
# model_b: sagemaker.Model


endpoint_config = sagemaker.EndpointConfig(self, "EndpointConfig",
    instance_production_variants=[sagemaker.InstanceProductionVariantProps(
        model=model_a,
        variant_name="modelA",
        initial_variant_weight=2
    ), sagemaker.InstanceProductionVariantProps(
        model=model_b,
        variant_name="variantB",
        initial_variant_weight=1
    )
    ]
)
```
