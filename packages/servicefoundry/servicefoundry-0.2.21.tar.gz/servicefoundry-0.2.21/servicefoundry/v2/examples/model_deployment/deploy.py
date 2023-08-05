import argparse
import logging

from servicefoundry import ModelDeployment, Resources

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--workspace-fqn", type=str, required=True)
parser.add_argument("--model-fqn", type=str, required=True)
args = parser.parse_args()

service = ModelDeployment(
    name="from-cli",
    model_uri=args.model_fqn,
    resources=Resources(cpu_limit=1.0, memory_limit=600),
)
deployment = service.deploy(workspace_fqn=args.workspace_fqn)
