#!/usr/bin/env python3
import json
import sys
from pathlib import Path

VALIDATION_STATUSES = {
    "VALIDATED",
    "PARTIALLY_VALIDATED",
    "INVALIDATED",
    "INCONCLUSIVE",
}

EXECUTION_STATUSES = {
    "not_run",
    "failed_to_run",
    "ran_and_failed",
    "ran_and_passed",
}

STOP_OR_CONTINUE = {"stop", "continue"}


def fail(message: str) -> None:
    print(f"INVALID: {message}", file=sys.stderr)
    sys.exit(1)


def require_obj(value, path: str) -> dict:
    if not isinstance(value, dict):
        fail(f"{path} must be an object")
    return value


def require_list(value, path: str) -> list:
    if not isinstance(value, list):
        fail(f"{path} must be a list")
    return value


def require_keys(obj: dict, path: str, keys: list[str]) -> None:
    for key in keys:
        if key not in obj:
            fail(f"{path} missing key: {key}")


def require_nonempty_string(value, path: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{path} must be a non-empty string")


def require_positive_int(value, path: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        fail(f"{path} must be a positive integer")


def validate_iteration(iteration: dict, index: int) -> None:
    path = f"iterations[{index}]"
    require_keys(
        iteration,
        path,
        ["iteration_number", "state", "propose", "implement", "run", "validate", "learn", "select"],
    )
    require_positive_int(iteration["iteration_number"], f"{path}.iteration_number")

    state = require_obj(iteration["state"], f"{path}.state")
    require_keys(
        state,
        f"{path}.state",
        [
            "current_uncertainty",
            "current_hypothesis",
            "predicted_observation",
            "experiment",
            "validation_method",
            "observed_result",
            "interpretation",
            "remaining_uncertainty",
            "next_action",
        ],
    )
    for key in (
        "current_uncertainty",
        "current_hypothesis",
        "predicted_observation",
        "experiment",
        "validation_method",
        "observed_result",
        "interpretation",
        "remaining_uncertainty",
        "next_action",
    ):
        require_nonempty_string(state[key], f"{path}.state.{key}")

    propose = require_obj(iteration["propose"], f"{path}.propose")
    require_keys(propose, f"{path}.propose", ["hypothesis", "reason_for_testing_it", "prediction", "disconfirming_evidence"])
    for key in ("hypothesis", "reason_for_testing_it", "prediction", "disconfirming_evidence"):
        require_nonempty_string(propose[key], f"{path}.propose.{key}")

    implement = require_obj(iteration["implement"], f"{path}.implement")
    require_keys(implement, f"{path}.implement", ["experiment", "controlled_variables", "changed_variable", "baseline", "expected_evidence"])
    require_list(implement["controlled_variables"], f"{path}.implement.controlled_variables")
    for key in ("experiment", "changed_variable", "baseline", "expected_evidence"):
        require_nonempty_string(implement[key], f"{path}.implement.{key}")

    run = require_obj(iteration["run"], f"{path}.run")
    require_keys(run, f"{path}.run", ["command_or_procedure", "inputs", "environment", "observed_output", "execution_status"])
    require_list(run["inputs"], f"{path}.run.inputs")
    for key in ("command_or_procedure", "environment", "observed_output"):
        require_nonempty_string(run[key], f"{path}.run.{key}")
    if run["execution_status"] not in EXECUTION_STATUSES:
        fail(f"{path}.run.execution_status has invalid value")

    validate = require_obj(iteration["validate"], f"{path}.validate")
    require_keys(validate, f"{path}.validate", ["validation_method", "validation_evidence", "alternative_explanations_considered", "validation_status", "confidence"])
    require_list(validate["alternative_explanations_considered"], f"{path}.validate.alternative_explanations_considered")
    for key in ("validation_method", "validation_evidence", "confidence"):
        require_nonempty_string(validate[key], f"{path}.validate.{key}")
    if validate["validation_status"] not in VALIDATION_STATUSES:
        fail(f"{path}.validate.validation_status has invalid value")

    learn = require_obj(iteration["learn"], f"{path}.learn")
    require_keys(
        learn,
        f"{path}.learn",
        [
            "supported_assumptions",
            "weakened_assumptions",
            "what_was_not_established",
            "new_information",
            "remaining_uncertainty",
            "confidence_update",
        ],
    )
    require_list(learn["supported_assumptions"], f"{path}.learn.supported_assumptions")
    require_list(learn["weakened_assumptions"], f"{path}.learn.weakened_assumptions")
    for key in ("what_was_not_established", "new_information", "remaining_uncertainty", "confidence_update"):
        require_nonempty_string(learn[key], f"{path}.learn.{key}")

    select = require_obj(iteration["select"], f"{path}.select")
    require_keys(select, f"{path}.select", ["candidate_next_actions", "selected_action", "reason", "expected_uncertainty_reduction", "stop_or_continue"])
    require_list(select["candidate_next_actions"], f"{path}.select.candidate_next_actions")
    for key in ("selected_action", "reason", "expected_uncertainty_reduction"):
        require_nonempty_string(select[key], f"{path}.select.{key}")
    if select["stop_or_continue"] not in STOP_OR_CONTINUE:
        fail(f"{path}.select.stop_or_continue has invalid value")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate-url-report.py <report.json>")

    path = Path(sys.argv[1])
    if not path.exists():
        fail(f"file does not exist: {path}")

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")

    require_obj(data, "report")
    require_keys(data, "report", ["objective", "budget", "iterations", "completion_record"])
    require_nonempty_string(data["objective"], "objective")

    budget = require_obj(data["budget"], "budget")
    require_keys(budget, "budget", ["maximum_iterations", "time_budget", "maximum_risky_changes"])
    require_positive_int(budget["maximum_iterations"], "budget.maximum_iterations")
    require_nonempty_string(budget["time_budget"], "budget.time_budget")
    if not isinstance(budget["maximum_risky_changes"], int) or isinstance(budget["maximum_risky_changes"], bool) or budget["maximum_risky_changes"] < 0:
        fail("budget.maximum_risky_changes must be a non-negative integer")

    iterations = require_list(data["iterations"], "iterations")
    if not iterations:
        fail("iterations must contain at least one iteration")
    if len(iterations) > budget["maximum_iterations"]:
        fail("iterations exceeds budget.maximum_iterations")
    for index, iteration in enumerate(iterations):
        validate_iteration(require_obj(iteration, f"iterations[{index}]"), index)

    completion = require_obj(data["completion_record"], "completion_record")
    require_keys(
        completion,
        "completion_record",
        ["final_conclusion", "evidence", "validation_status", "confidence", "known_limitations", "remaining_risks", "reproduction_instructions"],
    )
    require_list(completion["known_limitations"], "completion_record.known_limitations")
    require_list(completion["remaining_risks"], "completion_record.remaining_risks")
    for key in ("final_conclusion", "evidence", "confidence", "reproduction_instructions"):
        require_nonempty_string(completion[key], f"completion_record.{key}")
    if completion["validation_status"] not in VALIDATION_STATUSES:
        fail("completion_record.validation_status has invalid value")

    print("VALID: uncertainty loop report schema passed")


if __name__ == "__main__":
    main()
