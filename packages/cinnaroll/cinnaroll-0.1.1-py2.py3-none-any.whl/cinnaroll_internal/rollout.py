import __main__
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

from unittest import mock

from cinnaroll_internal import (
    environment_info,
    model,
    post_training_validation,
    pre_training_validation,
    rollout_config,
    utils, jupyter_notebook,
)

from cinnaroll_internal.infer_func_deps_finder.deps_finder import build_deps_finder

from cinnaroll_internal.model_upload import (
    check_size_limits,
    prepare_artifact,
    send_rollout_data,
    upload_artifact,
    notify_server,
)


CACHE_DIR_NAME = ".cinnaroll_cache"
# for tf/keras it's a dir, otherwise file
MODEL_SAVE_FILE_OR_DIR_NAME = "saved_model"
ARTIFACT_FILE_NAME = "artifact.tar.gz"


class RolloutConfigurationError(Exception):
    ...


# todo: if dict config is chosen, refactor this to return RolloutConfig and errors
# get stuff, don't transform data but return errors if something besides metrics is missing (key errors and None values)
# try to create RolloutConfig out of what's in dict
# catch type errors and reformat them to make them easier to understand
# return RolloutConfig and errors
def get_config_from_dict(
    config: Dict[str, Any]
) -> Tuple[rollout_config.RolloutConfig, List[Exception]]:
    pass


# todo: e2es on real filesystem to check multiplatform compatibility
def get_cache_dir_path(notebook_path: Optional[Path]) -> Path:
    if not notebook_path:
        return Path(__main__.__file__).parent / CACHE_DIR_NAME
    else:
        return Path(notebook_path).parent / CACHE_DIR_NAME


def create_cache_dir_if_not_exists(cache_dir_path: Path) -> None:
    if not cache_dir_path.exists():
        cache_dir_path.mkdir()


@mock.patch("requests.get", utils.mock_request)
@mock.patch("requests.post", utils.mock_request)
@mock.patch("requests.put", utils.mock_request)
def rollout(config: rollout_config.RolloutConfig) -> None:
    print("Validating config pre-training...")
    pre_training_errors = pre_training_validation.find_config_pre_training_errors(
        config
    )

    if len(pre_training_errors):
        for e in pre_training_errors:
            print(repr(e))
        raise RolloutConfigurationError
    print("Pre-training validation OK! Great!")

    notebook_path = jupyter_notebook.get_main_notebook_path_if_run_in_one()

    cache_dir_path = get_cache_dir_path(notebook_path)
    create_cache_dir_if_not_exists(cache_dir_path)

    model_save_path = cache_dir_path / MODEL_SAVE_FILE_OR_DIR_NAME
    artifact_path = cache_dir_path / ARTIFACT_FILE_NAME

    print("Inferring framework...")
    framework = model.infer_framework(config.model_object)
    cinnaroll_model = model.create_model(config.model_object, framework, model_save_path)

    trained_in_script = model.is_trained_in_script(config.train_eval)

    # if train_eval it not empty by default we want to train model
    train_model = trained_in_script

    if cinnaroll_model.should_be_loaded():
        train_model = False

        print("Loading saved model...")
        try:
            # if model exists and can be loaded we do not want to train it
            cinnaroll_model.load()
        except model.ModelLoadingError as e:
            # if model exists but loading fails and train_val is not empty, we ask the user to decide
            if trained_in_script:
                user_input = ""

                while user_input not in ("y", "yes", "n", "no"):
                    user_input = input(
                        f"Loading the model failed with the following error: {repr(e)} Train? y/n "
                    )
                    if user_input in ("y", "yes"):
                        train_model = True
        else:
            print("Loaded successfully!")

    if train_model:
        print("Training model...")
        config.metrics = config.train_eval(config.model_object)
        print("Model trained!")

    print("Saving model...")
    try:
        cinnaroll_model.save()
    except model.ModelSavingError as e:
        print(f"Saving the model failed with the following error: {repr(e)}")
    else:
        print("Model saved!")

    print("Validating config post-training...")

    post_training_errors = post_training_validation.find_config_post_training_errors(
        cinnaroll_model=cinnaroll_model,
        config=config,
    )

    if len(post_training_errors):
        for err in post_training_errors:
            print(repr(err))
        raise RolloutConfigurationError
    print("Post-training validation OK! Great!")

    print("Fetching model metadata...")
    model_metadata = cinnaroll_model.get_metadata()
    print("Fetching environment info...")
    user_environment_info = environment_info.EnvironmentInfo(framework)

    print("Creating model artifact...")
    deps_finder = build_deps_finder(config.infer, notebook_path)
    infer = deps_finder.get_infer_with_used_global_variables()

    size_limit_errors = check_size_limits(
        infer.file_content,
        config.model_input_sample,
        config.infer_func_input_sample,
        config.infer_func_input_format,
    )

    if len(size_limit_errors) > 0:
        for err in size_limit_errors:
            print(repr(err))
        raise RolloutConfigurationError
    print("Size limit checks of individual components passed.")

    artifact_preparation_errors = prepare_artifact(
        artifact_path,
        model_save_path,
        infer.file_content,
        infer.global_variables,
        user_environment_info.requirements,
        config.model_input_sample,
        config.infer_func_input_sample,
        config.infer_func_input_format,
    )

    if len(artifact_preparation_errors) > 0:
        for err in artifact_preparation_errors:
            print(repr(err))
        raise RolloutConfigurationError
    print("Artifact prepared correctly.")

    print("Sending rollout data to cinnaroll backend...")

    res = send_rollout_data(
        config=config,
        framework=framework,
        user_environment_info=user_environment_info,
        model_metadata=model_metadata,
    )

    if res.status_code != 201:
        raise RolloutConfigurationError("Sending rollout data failed.")

    res_json = res.json()
    upload_id = res_json["id"]
    upload_url = res_json["uploadUrl"]

    print("Uploading model and input samples...")
    res_upload_artifact = upload_artifact(artifact_path, upload_url)

    if res_upload_artifact.status_code == 200:
        status = "UPLOAD_SUCCESSFUL"
    else:
        status = "UPLOAD_FAILED"

    res_notify_server = notify_server(upload_id, status)

    if res_upload_artifact.status_code != 200:
        raise RolloutConfigurationError("Artifact upload failed.")

    if res_notify_server.status_code != 200:
        raise RolloutConfigurationError("Post-upload server notification failed.")

    print("Success!")
    print("Congratulations! You've configured cinnaroll rollout successfully!")

    utils.clean_path(cache_dir_path)
