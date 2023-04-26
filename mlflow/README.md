# MLflow

Source: https://www.run.ai/guides/machine-learning-operations/mlflow

There are two other key concepts in MLflow:

- **A run** is a collection of parameters, metrics, labels, and artifacts related to the training process of a machine learning model.
- **An experiment** is the basic unit of MLflow organization. All MLflow runs belong to an experiment. For each experiment, you can analyze and compare the results of different runs, and easily retrieve metadata artifacts for analysis using downstream tools. Experiments are maintained on an MLflow tracking server hosted on Azure Databricks.

### MLflow Tracking

- **Source**—can be the name of the file that launches the run. Alternatively, if you are using an MLflow project, it can be the name of the project and entry point of the run.
- **Code version**—when using an MLflow Project, this would be the Git commit hash.
- **Parameters**—can be any key-value input parameters you choose, as long as the values and the keys are both strings.
- **Artifacts**—are output files (in all formats). Artifacts let you record images, PNGs for example, models (such as pickled scikit-learn models), and data files such as Parquet files.
- **Start and end time**—lets you record the start and end time of your run.
- **Metrics**—let you record key-value metrics containing numeric values. It is possible to update each metric throughout the duration of a run. This lets you, for example, track how the loss function of the model is converging. Additionally, MLflow lets you visualize the full history of each metric.

### MLflow Projects

- **System environment**—you can run projects directly in your existing system environment. To do this, you need to install all project dependencies on the system before executing the project. Note that the system environment is not part of the contents directory or the MLproject file. Rather, it is supplied at runtime.
- **Conda environment**—offers support for native libraries like Intel MKL or CuDNN as well as python packages. If you specify a Conda environment for your project, it will be activated before the project code starts running.
- **Docker container environment**—a container lets you capture non-Python dependencies like Java libraries. MLflow projects that use Docker images get an added Docker layer that copies the contents of the project into a directory called /mlflow/projects/code. Once this happens, a new container image is produced. Next, MLflow runs the image and invokes the project entry point in the resulting container.

### MLflow Models

MLflow models let you package machine learning models in a format supported by many downstream tools. You can add metadata to your MLflow models, including:

- **Model signature**—defines the schema of the inputs and outputs of your model. You can use either tensor-based or column-based model inputs and outputs. You can describe column-based inputs and outputs as a sequence of named columns and specify the MLflow data type. You can do the same for tensor-based inputs and outputs, and specify a numpy data type. Note that signatures are stored as JSON in the MLmodel file, along with additional model metadata.
- **Model input example**—this is an artifact that is an instance of a model input, stored together with your model. You can use either column-based or tensor-based inputs.

### MLflow Model Registry

MLflow Model Registry provides an API and UI for centrally managing your models and their lifecycle. The registry provides model lineage, model versioning, annotations, and stage transitions.

Here are key features and concepts to know when using the model registry:

**Registered model**

In MLflow, a registered model is one that has a unique name and metadata, contains model versions and transitional stages, and has a model lineage.

**Model version**

A registered model can contain one or more model versions. When you register a new model in the registry, it is considered version 1. Any new model using the same name is added as a subsequent version.

**Model stage**

For each model version, you can assign one stage, at any time. However, stages must be assigned according to the officially determined MLflow stages, such as staging, production, and archived. It is possible to transition a model version from one stage to another.

**Annotations and descriptions**

MLflow lets you annotate the top-level model as well as each individual version, using markdown. You can add descriptions and any relevant information, such as algorithm descriptions, methodology, and dataset employed.

### MLflow Plugins

The MLflow Python API comes with APIs that let you write plugins you can integrate with other ML frameworks and backends. You can use these plugins to integrate with third party storage solutions, as well as third party authentication providers.

You can also use plugins to customize the behavior of the MLflow Python client. This can help you, for example, use the client to communicate with other REST APIs. Additionally, you can use plugins to automatically capture metadata as run tags, and add a new backend designed to execute entry points.

Here are key types of plugins supported by the MLflow Python API:

- **Run context providers**—this plugin lets you define context tags for runs created through the mlflow.start_run() fluent API.
- **ArtifactRepository**—lets you override the logic of artifact logging.
- **Tracking store**—helps you override the logic of your tracking backend.
- **MLFlow project backend**—lets you override the local execution backend and instead execute a project on your own cluster.
- **Model registry store**—enables you to override the logic of the model registry backend.

***Now that you understand the basics of MLflow, you may want to check out our guides about key concepts in machine learning engineering:\***

- [*Machine learning automation*](https://www.run.ai/guides/machine-learning-engineering/machine-learning-automation)
- [*Machine learning workflow*](https://www.run.ai/guides/machine-learning-engineering/machine-learning-workflow)
- [*Machine learning infrastructure*](https://www.run.ai/guides/machine-learning-engineering/machine-learning-infrastructure)

### MLflow Tutorial

#### Training the Model

Ensure your current working directory is examples, and run the following command to train a linear regression model:

`python sklearn_elasticnet_wine/train.py <alpha> <l1_ratio>`

#### Evaluating Model Performance

```bash
mlflow ui
```

#### Packaging Training Code

Let’s package the training code so it can be reused by others. You do this using two files.

**MLproject file**

This file, located under the sklearn_elasticnet_wine example directory, specifies the parameters of the project, the command used to train it, and points to a conda configuration file which holds the project dependencies. It looks like this:

```yaml
name: tutorial

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      alpha: {type: float, default: 0.5}
      l1_ratio: {type: float, default: 0.1}
    command: "python 0_sklearn_elasticnet_wine_train.py {alpha} {l1_ratio}"
```

**Conda configuration file**

The `conda.yaml` file defines the dependencies of the project:

```yaml
name: tutorial
channels:
  - conda-forge
dependencies:
  - python=3.8
  - pip
  - pip:
      - scikit-learn==0.23.2
      - mlflow>=1.0
      - pandas
```

**Running the project**

Now that the project is packaged by MLflow, you can run it from any environment, including remote machines. MLflow runs your code in a Conda environment with the dependencies specified in conda.yaml.

To run this project, invoke 

`mlflow run sklearn_elasticnet_wine -P alpha=0.42`. or `mlflow run . -P alpha=0.42`

After running this command, MLflow runs your training code in a new Conda environment with the dependencies specified in `conda.yaml`.

If the repository has an `MLproject` file in the root you can also run a project directly from GitHub. This tutorial is duplicated in the https://github.com/mlflow/mlflow-example repository which you can run with `mlflow run https://github.com/mlflow/mlflow-example.git -P alpha=5.0`.

> Note: Run MLflow in local env: `mlflow run sklearn_elasticnet_wine -P alpha=0.42 --env-manager=local `
>
> or
>
> `mlflow run . --env-manager=local`

#### Deploying the Model

In the training code, each time you ran the model, it was saved as an artifact within a run. Open the MLflow UI and click the date or a specific run. You will see a screen like this:

![The MLflow UI](https://assets.website-files.com/62c4a9809a85693c49c4674f/62c4a9809a856914fcc46c48_61e95e54543a7c13826803a2_MLflow4.webp)

Image Source: MLflow

At the top, MLflow shows the ID of the run and its metrics. Below, you can see the artifacts generated by the run—an MLmodel file with metadata that allows MLflow to run the model, and model.pkl, a serialized version of the model which you can run to deploy the model.

To deploy an HTTP server running your model, run this command. Replace the {PATH} with the actual **Full Path** shown in the UI for the specific run you want to deploy:

`mlflow models serve -m {PATH} -p 1234`

You can now use the server to get predictions from your trained model. The following code shows how to run the model on common operating systems:

```bash
# On Linux and macOS
curl -X POST -H "Content-Type:application/json" --data '{"dataframe_split": {"columns":["fixed acidity", "volatile acidity", "citric acid", "residual sugar", "chlorides", "free sulfur dioxide", "total sulfur dioxide", "density", "pH", "sulphates", "alcohol"],"data":[[6.2, 0.66, 0.48, 1.2, 0.029, 29, 75, 0.98, 3.33, 0.39, 12.8]]}}' http://127.0.0.1:1234/invocations

# On Windows
curl -X POST -H "Content-Type:application/json" --data "{\"dataframe_split\": {\"columns\":[\"fixed acidity\", \"volatile acidity\", \"citric acid\", \"residual sugar\", \"chlorides\", \"free sulfur dioxide\", \"total sulfur dioxide\", \"density\", \"pH\", \"sulphates\", \"alcohol\"],\"data\":[[6.2, 0.66, 0.48, 1.2, 0.029, 29, 75, 0.98, 3.33, 0.39, 12.8]]}}" http://127.0.0.1:1234/invocations
```

