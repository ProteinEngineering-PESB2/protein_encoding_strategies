import logging

from copy import deepcopy
from os import path
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Tuple, List, Dict, Any

from ruamel import yaml

from webserver.database import write_file
from webserver.tasks import task_keeper
from webserver.utilities.configuration import configuration

logger = logging.getLogger(__name__)


def read_config_file(config_path: Path) -> Dict[str, Any]:
    with config_path.open("r") as fp:
        return yaml.load(fp, Loader=yaml.RoundTripLoader)


_module_dir: Path = Path(path.dirname(path.abspath(__file__)))

# Template configs: these will be the "job types" available
_annotations_from_bert: Dict[str, Dict[str, str]] = read_config_file(_module_dir / "template_configs" / 'annotations_from_bert.yml')
_annotations_from_seqvec: Dict[str, Dict[str, str]] = read_config_file(_module_dir / "template_configs" / 'annotations_from_seqvec.yml')

# Enrich templates with execution specific parameters: location of weights & optionable max_aa

# BERT
_annotations_from_bert['bert_embeddings']['model_directory'] = configuration['prottrans_bert_bfd']['model_directory']
_annotations_from_bert['bert_embeddings']['max_amino_acids'] = configuration['prottrans_bert_bfd']['max_amino_acids']
_annotations_from_bert['annotations_from_bert']['secondary_structure_checkpoint_file'] = configuration['prottrans_bert_bfd']['secondary_structure_checkpoint_file']
_annotations_from_bert['annotations_from_bert']['subcellular_location_checkpoint_file'] = configuration['prottrans_bert_bfd']['subcellular_location_checkpoint_file']


# SEQVEC
_annotations_from_seqvec['seqvec_embeddings']['weights_file'] = configuration['seqvec']['weights_file']
_annotations_from_seqvec['seqvec_embeddings']['options_file'] = configuration['seqvec']['options_file']
_annotations_from_seqvec['seqvec_embeddings']['max_amino_acids'] = configuration['seqvec']['max_amino_acids']
_annotations_from_seqvec['annotations_from_seqvec']['secondary_structure_checkpoint_file'] = configuration['seqvec']['secondary_structure_checkpoint_file']
_annotations_from_seqvec['annotations_from_seqvec']['subcellular_location_checkpoint_file'] = configuration['seqvec']['subcellular_location_checkpoint_file']


_CONFIGS = {
    'annotations_from_seqvec': _annotations_from_seqvec,
    'annotations_from_bert': _annotations_from_bert,
}

_FILES_TO_STORE = [
    "embeddings_file",
    "reduced_embeddings_file",
    "sequence_file",
    "DSSP3_predictions_file",
    "DSSP8_predictions_file",
    "disorder_predictions_file",
    "per_sequence_predictions_file",
    "mapping_file",
    "plot_file"
]


@task_keeper.task()
def run_pipeline(job_identifier: str, sequences: List[Tuple[str, str]], pipeline_type: str):
    from bio_embeddings.utilities.pipeline import execute_pipeline_from_config

    config = deepcopy(_CONFIGS[pipeline_type])

    def _post_stage_save(stage_out_config):
        for file_name in _FILES_TO_STORE:
            if stage_out_config.get(file_name):
                logger.info(f"Copying {file_name} to database.")
                write_file(job_identifier, file_name, stage_out_config[file_name])

    with TemporaryDirectory() as workdir:
        with Path(workdir).joinpath("sequences.fasta").open("w") as fp:
            for seq_id, sequence in sequences:
                fp.write(f">{seq_id}\n{sequence}\n")

        # Add last job details
        config['global']['prefix'] = str(Path(workdir) / "bio_embeddings_job")
        config['global']['sequences_file'] = str(Path(workdir) / "sequences.fasta")

        logger.info("------ Starting pipeline execution...")
        execute_pipeline_from_config(config, post_stage=_post_stage_save)
        logger.info("------ Finished pipeline execution.")
