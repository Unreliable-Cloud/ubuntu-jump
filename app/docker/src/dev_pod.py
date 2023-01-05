from avionix import ChartBuilder, ChartDependency, ChartInfo
import yaml

def deploy_dev_pod(namespace=str, deploymentName=str, backupState=bool):
  valuesFile = "static/dev-pod-values.yaml"
  namespace = namespace
  deploymentName = deploymentName
  backupState = backupState

  with open(valuesFile) as f:
      values = yaml.load(f.read(), Loader=yaml.FullLoader)

  builder = ChartBuilder(
      ChartInfo(
          api_version="3.2.4",
          name=deploymentName,
          version="0.0.3",
          app_version="v1",
          dependencies=[
              ChartDependency(
                  name="dev-pod",
                  version="0.0.3",
                  repository="file:///home/devpod/helm",
                  local_repo_name="dev-pod",
                  is_local=True,
                  values=values,
              ),
          ],
      ),
      [],
  )

  builder.install_chart(options={"namespace": namespace, "create-namespace": None, "dependency-update": None, "debug": None})
  return print(values)
  f.close()