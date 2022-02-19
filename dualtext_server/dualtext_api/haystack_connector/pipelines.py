import yaml
from .indexing_pipeline import IndexingPipeline
from .query_pipeline import QueryPipeline
from dualtext_api.haystack_connector import custom_pipelines
import os


def init_pipeline(pipeline_name, pipeline_cfg, pipeline_type, initialized_pipelines):
    if pipeline_cfg.get('url', None) is None:
        pipeline = getattr(custom_pipelines, pipeline_name)
    else:
        pipeline = None

    if pipeline_type == 'indexing':
        initialized_pipelines['indexing'][pipeline_name] = IndexingPipeline(pipeline_name, pipeline, **pipeline_cfg)
    elif pipeline_type == 'query':
        initialized_pipelines['query'][pipeline_name] = QueryPipeline(pipeline_name, pipeline, **pipeline_cfg)

    return initialized_pipelines

module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'pipeline_config.yml')
with open(file_path, 'r') as f:
    pipelines = yaml.safe_load(f) or {}

initialized_pipelines = {
    'indexing': {},
    'query': {}
}


for pipeline_name, pipeline_cfg in pipelines.items():
    pipeline_type = pipeline_cfg.pop('type')
    initialized_pipelines = init_pipeline(pipeline_name, pipeline_cfg, pipeline_type, initialized_pipelines)
