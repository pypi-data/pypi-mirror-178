import base64
import json
import os
import shutil
import subprocess
import tempfile
from shutil import which

import chevron
import questionary
import rich_click as click
import yaml

from servicefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from servicefoundry.logger import logger


class Infra:
    def __init__(self, dry_run):
        self.config = create_config_object()
        self.kube_config_location = get_kube_location()
        self.dry_run = dry_run

    # TODO define logging level at the class entry point
    def clone_base_ubermold(self, temp_dir):
        clone_dir = os.path.join(temp_dir, "ubermold")
        username = self.config["base-ubermold"]["username"]
        password = base64.b64decode(
            self.config["base-ubermold"]["passwordBase64"].encode()
        ).decode()
        url = self.config["base-ubermold"]["url"]
        branch = self.config["base-ubermold"]["branch"]

        print(
            execute_git_command(
                [
                    "clone",
                    "-b",
                    branch,
                    f"https://{username}:{password}@{url}",
                    clone_dir,
                ]
            )
        )
        return clone_dir

    def clone_target_ubermold(self, temp_dir):
        clone_dir = os.path.join(temp_dir, "target-ubermold")
        username = self.config["base-ubermold"]["username"]
        password = base64.b64decode(
            self.config["base-ubermold"]["passwordBase64"].encode()
        ).decode()
        url = self.config["target-ubermold"]["url"]
        branch = self.config["target-ubermold"]["branch"]

        print(
            execute_git_command(
                [
                    "clone",
                    "-b",
                    branch,
                    f"https://{username}:{password}@{url}",
                    clone_dir,
                ]
            )
        )
        return clone_dir

    def get_provider(self):
        answer = questionary.select(
            "select your provider ", choices=["gcp", "aws"]
        ).ask()
        self.config["cluster"] = {}
        self.config["cluster"]["provider"] = answer

    def execute_shell_command(self, command, ip=None):
        if self.dry_run:
            return
        logger.debug(f"executing command: {command}")
        try:
            p = subprocess.run(command, check=True, stdout=subprocess.PIPE, input=ip)
            return p.stdout.decode("UTF-8")
        except subprocess.CalledProcessError as err:
            raise Exception(f"failed to execute: {command}, error: {err}") from err

    def execute_helm_command(self, args):
        return self.execute_shell_command([which("helm"), *args])

    def execute_kubectl_apply(self, manifest):
        return self.execute_shell_command(
            [
                which("kubectl"),
                "apply",
                f"--kubeconfig={self.kube_config_location}",
                "-f",
                "-",
            ],
            ip=json.dumps(manifest).encode(),
        )

    def execute_kubectl_command(self, args):
        return self.execute_shell_command(
            [which("kubectl"), f"--kubeconfig={self.kube_config_location}", *args]
        )

    # TODO : create separate functions fir diff stages to improve readability
    def bootstrap(self):
        # Assuming cluster is already there
        # Check if kubectl, helm cli, istioctl is installed
        # Ask for location of kubeconfig, use ~/.kube/config by default
        # Install argocd using helm
        # Create the secrets using the config values
        # Initialize istio - Helm installation
        # Clone the supplied ubermold-repo and check out the correct branch
        # Convert installation section to ubermold values file
        # Install ubermold with values.yaml + patch.yaml as values files
        ubermold_clones_dir = os.path.join(tempfile.gettempdir(), "ubermold-clones")
        try:
            get_all_values(self.config)
            self.get_provider()
            validate_dependencies()

            # Checking for cluster connectivity
            cluster_version_json = self.execute_kubectl_command(["version", "-ojson"])
            cluster_version = json.loads(cluster_version_json)
            print("Cluster connected successfully :)")
            print(f'Cluster version: {cluster_version["serverVersion"]["gitVersion"]}')

            cluster_version_major = int(cluster_version["serverVersion"]["major"])
            cluster_version_minor = int(cluster_version["serverVersion"]["minor"])
            if (
                cluster_version_major != 1
                or cluster_version_minor < 22
                or cluster_version_minor > 23
            ):
                raise Exception("Only cluster versions 1.22 to 1.23 are supported")

            # stage 1 & 2 implementation

            base_ubermold_dir = self.clone_base_ubermold(ubermold_clones_dir)
            base_ubermold_path = os.path.join(
                base_ubermold_dir, self.config["base-ubermold"]["path"]
            )

            installation_config = {}
            with open(
                os.path.join(base_ubermold_path, "input.yaml"), "r"
            ) as installation_config_file:
                installation_config = yaml.safe_load(installation_config_file)
            get_all_values(installation_config)

            generated_values_yaml = None
            with open(
                os.path.join(base_ubermold_path, "template.mustache"), "r"
            ) as mustache_template_file:
                generated_values_yaml = chevron.render(
                    mustache_template_file, installation_config
                )
            with open(
                os.path.join(base_ubermold_path, "values.yaml"), "w"
            ) as base_values:
                base_values.write(generated_values_yaml)

            # TODO: We are assuming that a remote target repo already exists
            target_ubermold_dir = self.clone_target_ubermold(ubermold_clones_dir)
            target_ubermold_path = os.path.join(
                target_ubermold_dir, self.config["target-ubermold"]["path"]
            )

            current_dir = os.getcwd()
            os.chdir(target_ubermold_dir)

            target_branch = self.config["target-ubermold"]["branch"]
            execute_git_command(["checkout", target_branch])
            execute_git_command(["fetch"])

            os.makedirs(target_ubermold_path, exist_ok=True)

            overwrite_file(
                os.path.join(base_ubermold_path, "Chart.yaml"),
                os.path.join(target_ubermold_path, "Chart.yaml"),
            )
            shutil.copytree(
                os.path.join(base_ubermold_path, "templates"),
                os.path.join(target_ubermold_path, "templates"),
            )
            overwrite_file(
                os.path.join(base_ubermold_path, "values.yaml"),
                os.path.join(target_ubermold_path, "values.yaml"),
            )

            execute_git_command(["add", "."])
            diff_check = execute_git_command(["diff"])
            if not diff_check:
                print(
                    "No changes detcted in target ubermold\n Moving on to the next stage"
                )
            else:
                execute_git_command(["commit", "-m", "bootstrap workload commit"])
                execute_git_command(["push", "-f", "origin", target_branch])
            os.chdir(current_dir)

            # stage 3 implementation
            # ARGOCD
            # Adding the private repo
            private_helm_repo_name = "private-helm-tf-apply"
            private_helm_repo_url = self.config["argocd"]["repoCreds"][
                "privateHelmChart"
            ]["url"]
            private_helm_repo_password = base64.b64decode(
                self.config["argocd"]["repoCreds"]["privateHelmChart"]["passwordBase64"]
            )

            repo_list_json = self.execute_helm_command(["repo", "list", "-ojson"])
            repo_list = json.loads(repo_list_json)
            for repo in repo_list:
                if repo["name"] == private_helm_repo_name:
                    print(f"{private_helm_repo_name} already exists, removing it...")
                    print(
                        self.execute_helm_command(
                            ["repo", "remove", private_helm_repo_name]
                        )
                    )
                    break

            print(
                self.execute_helm_command(
                    [
                        "repo",
                        "add",
                        private_helm_repo_name,
                        private_helm_repo_url,
                        "--username",
                        private_helm_repo_password,
                        "--password",
                        private_helm_repo_password,
                    ]
                )
            )
            print(self.execute_helm_command(["repo", "update", private_helm_repo_name]))

            # Installing argocd
            repo_server_annotation_key = '"eks\.amazonaws\.com/role-arn"'
            if self.config["cluster"]["provider"] == "gcp":
                repo_server_annotation_key = '"iam\.gke\.io/gcp-service-account"'
            argocd_installation_args = [
                "upgrade",
                "--install",
                "--namespace",
                "argocd",
                "--create-namespace",
                "--set",
                'controller.enableStatefulSet="true"',
                "--set",
                'server.extraArgs="{--insecure}"',
                "--set",
                f'argo-cd.repoServer.serviceAccount.annotations.{repo_server_annotation_key}={self.config["argocd"]["iamRole"]}',
                "--kubeconfig",
                self.kube_config_location,
                "argocd",
                "private-helm-tf-apply/argocd",
            ]
            print(self.execute_helm_command(argocd_installation_args))
            print(self.execute_helm_command(["repo", "remove", private_helm_repo_name]))

            # Connecting repos
            secrets = create_repo_secrets_object()

            for secret in secrets["items"]:
                if secret["metadata"]["name"] == "argocd-application-helm-charts":
                    secret["data"]["githubAppID"] = as_b64(
                        self.config["argocd"]["repoCreds"]["applicationHelmCharts"][
                            "appId"
                        ]
                    )
                    secret["data"]["githubAppInstallationID"] = as_b64(
                        self.config["argocd"]["repoCreds"]["applicationHelmCharts"][
                            "appInstallationId"
                        ]
                    )
                    secret["data"]["githubAppPrivateKey"] = self.config["argocd"][
                        "repoCreds"
                    ]["applicationHelmCharts"]["appPrivateKeyBase64"]
                    secret["data"]["url"] = as_b64(
                        self.onfig["argocd"]["repoCreds"]["applicationHelmCharts"][
                            "url"
                        ]
                    )

                if secret["metadata"]["name"] == "argocd-infra-ubermold":
                    secret["data"]["password"] = self.config["argocd"]["repoCreds"][
                        "ubermold"
                    ]["passwordBase64"]
                    secret["data"]["url"] = as_b64(
                        self.config["argocd"]["repoCreds"]["ubermold"]["url"]
                    )
                    secret["data"]["username"] = as_b64(
                        self.config["argocd"]["repoCreds"]["ubermold"]["username"]
                    )

                if secret["metadata"]["name"] == "argocd-private-helm-charts":
                    secret["data"]["url"] = as_b64(
                        self.config["argocd"]["repoCreds"]["privateHelmChart"]["url"]
                    )

                if secret["metadata"]["name"] == "argocd-private-helm-charts-creds":
                    secret["data"]["url"] = as_b64(
                        self.config["argocd"]["repoCreds"]["privateHelmChart"]["url"]
                    )
                    secret["data"]["username"] = as_b64(
                        self.config["argocd"]["repoCreds"]["privateHelmChart"][
                            "username"
                        ]
                    )
                    secret["data"]["password"] = self.config["argocd"]["repoCreds"][
                        "privateHelmChart"
                    ]["passwordBase64"]
            print(self.execute_kubectl_apply(secrets))

            ubermold_manifest = create_ubermold_object()

            ubermold_manifest["spec"]["source"]["path"] = self.config[
                "target-ubermold"
            ]["path"]
            ubermold_manifest["spec"]["source"][
                "repoURL"
            ] = f'https://{self.config["target-ubermold"]["url"]}'
            ubermold_manifest["spec"]["source"]["targetRevision"] = self.config[
                "target-ubermold"
            ]["branch"]

            print(self.execute_kubectl_apply(ubermold_manifest))
        finally:
            if os.path.isdir(ubermold_clones_dir):
                shutil.rmtree(ubermold_clones_dir)


def get_kube_location():
    default_kube_config_location = os.path.join(os.path.expanduser("~"), ".kube/config")
    kube_config_location = questionary.path(
        "Please provide the location of kube config file to use",
        default=default_kube_config_location,
    ).ask()
    return kube_config_location


def create_config_object():
    config = {
        "argocd": {
            "iamRole": "aws:arn:iam::12321312:asdasdasd",
            "repoCreds": {
                "applicationHelmCharts": {
                    "url": "https://github.com/truefoundry/helm-charts.git",
                    "appId": "<appId>",
                    "appInstallationId": "<appInstallationId>",
                    "appPrivateKeyBase64": "<appPrivateKey>",
                },
                "ubermold": {
                    "url": "https://github.com/truefoundry/ubermold-truefoundry.git",
                    "username": "github",
                    "passwordBase64": "<passwordBase64>",
                },
                "privateHelmChart": {
                    "url": "https://raw.githubusercontent.com/truefoundry/helm-charts/gh-pages",
                    "username": "github",
                    "passwordBase64": "<passwordBase64>",
                },
            },
        },
        "target-ubermold": {
            "url": "github.com/truefoundry/ubermold-truefoundry.git",
            "branch": "main",
            "path": "new-cluster",
        },
        "base-ubermold": {
            "url": "github.com/truefoundry/ubermold-truefoundry.git",
            "branch": "sunanda",
            "path": "base-ubermold",
            "username": "github",
            "passwordBase64": "<passwordBase64>",
        },
    }
    return config


def create_ubermold_object():
    ubermold_manifest = {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Application",
        "metadata": {"name": "ubermold", "namespace": "argocd"},
        "spec": {
            "destination": {
                "namespace": "argocd",
                "server": "https://kubernetes.default.svc",
            },
            "project": "default",
            "source": {
                "plugin": {
                    "env": [
                        {"name": "RELEASE_NAME", "value": "ubermold"},
                        {"name": "VALUES_FILE", "value": "values.yaml"},
                    ]
                },
                "name": "secretsfoundry-plugin",
                "path": "<path>",
                "repoURL": "<repo-url>",
                "targetRevision": "<target-revision>",
            },
            "syncPolicy": {
                "automated": None,
                "prune": True,
                "syncOptions": ["CreateNamespace=true"],
            },
        },
    }
    return ubermold_manifest


def create_repo_secrets_object():
    secrets = {
        "apiVersion": "v1",
        "kind": "List",
        "items": [
            {
                "apiVersion": "v1",
                "data": {
                    "githubAppID": "<githubAppId>",
                    "githubAppInstallationID": "<githubAppInstallationID>",
                    "githubAppPrivateKey": "<githubAppPrivateKey>",
                    "url": "<applicationHelmChartsUrl>",
                },
                "kind": "Secret",
                "metadata": {
                    "labels": "argocd.argoproj.io/secret-type: repository",
                    "name": "argocd-application-helm-charts",
                    "namespace": "argocd",
                },
                "type": "Opaque",
            },
            {
                "apiVersion": "v1",
                "data": {
                    "password": "<ubermoldPassword>",
                    "url": "<ubermoldUrl>",
                    "username": " <ubermoldUsername>",
                },
                "kind": "Secret",
                "metadata": {
                    "labels": "argocd.argoproj.io/secret-type: repository",
                    "name": "argocd-infra-ubermold",
                    "namespace": "argocd",
                },
                "type": "Opaque",
            },
            {
                "apiVersion": "v1",
                "data": {"type": "aGVsbQ==", "url": "<privateHelmChartUrl>"},
                "kind": "Secret",
                "metadata": {
                    "labels": "argocd.argoproj.io/secret-type: repository",
                    "name": "argocd-private-helm-charts",
                    "namespace": "argocd",
                },
                type: "Opaque",
            },
            {
                "apiVersion": "v1",
                "data": {
                    "password": "<privateHelmChartCredsPassword>",
                    "type": "aGVsbQ==",
                    "url": "<privateHelmChartCredsUrl>",
                    "username": "<privateHelmChartCredsUsername>",
                },
                "kind": "Secret",
                "metadata": {
                    "labels": "argocd.argoproj.io/secret-type: repo-creds",
                    "name": "argocd-private-helm-charts-creds",
                    "namespace": "argocd",
                },
                type: "Opaque",
            },
        ],
    }
    return secrets


def validate_dependencies():
    if not which("kubectl"):
        raise Exception("kubectl not found")

    if not which("helm"):
        raise Exception("helm not found")

    if not which("git"):
        raise Exception("git not found")


def as_b64(data: str) -> str:
    return base64.b64encode(data.encode(encoding="utf-8")).decode(encoding="utf-8")


def confirm_val(v, tree_path):
    v = questionary.text(f"Please Enter {tree_path} : ", default=str(v)).ask()
    return v


def confirm_list_val(v, tree_path):
    temp_v = questionary.text(f"Please Enter {tree_path} : ", default=str(v)).ask()
    temp_v = str(temp_v).replace("'", '"')
    v = json.loads(temp_v)
    print(type(v))
    return v


# TODO: add unit test for get_all_values function
def get_all_values(dicts, tree_path=""):
    if tree_path != "":
        tree_path += "."
    for k, v in dicts.items():
        if isinstance(v, dict):
            dicts[k] = get_all_values(v, tree_path + k)
        elif isinstance(v, list):
            if len(v) != 0 and isinstance(v[0], dict):
                for i, vi in enumerate(v):
                    get_all_values(vi, tree_path + k + "[" + i + "]")
            else:
                dicts[k] = confirm_list_val(v, tree_path + k)
        else:
            dicts[k] = confirm_val(v, tree_path + k)
    return dicts


def overwrite_file(src, dst):
    if os.path.isdir(dst):
        logger.warning(
            "file to be overwritten is a directory. removing the existing files"
        )
        shutil.rmtree(dst)

    shutil.copy(src, dst)


def execute_git_command(args):
    import git

    g = git.Git(os.path.join(os.path.expanduser("~"), "/git/GitPython"))
    try:
        result = g.execute(["git", *args])
        return result
    except Exception as e:
        raise Exception("Git command failed") from e


@click.group(
    name="infra",
    cls=GROUP_CLS,
)
def infra():
    pass


@click.command(
    name="bootstrap",
    cls=COMMAND_CLS,
    help="Bootstrap truefoundry platform on an existing Kubernetes cluster",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
)
def infra_bootstrap(dry_run: bool):
    infra_object = Infra(dry_run=dry_run)
    infra_object.bootstrap()


def get_infra_command():
    infra.add_command(infra_bootstrap)
    return infra
