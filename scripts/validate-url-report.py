#!/usr/bin/env python3
import json
import sys
from pathlib import Path

VALIDATION_STATUSES = {
    "VALIDATED",
    "PARTIALLY_VALIDATED",
    "INVALIDATED",
    "INCONCLUSIVE",
    "VALIDATED|PARTIALLY_VALIDATED|INVALIDATED|INCONCLUSIVE",
}

EXECUTION_STATUSES = {
    "not_run",
    "failed_to_run",
    "ran_and_failed",
    "ran_and_passed",
    "not_run|failed_to_run|ran_and_failed|ran_and_passed",
}

STOP_OR_CONTINUE = {"stop", "continue", "stop|continue"}


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


def validate_iteration(iteration: dict, index: int) -> None:
    path = f"iterations[{index}]"
    require_keys(
        iteration,
        path,
        ["iteration_number", "state", "propose", "implement", "run", "validate", "learn", "select"],
    )

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

    propose = require_obj(iteration["propose"], f"{path}.propose")
    require_keys(propose, f"{path}.propose", ["hypothesis", "reason_for_testing_it", "prediction", "disconfirming_evidence"])

    implement = require_obj(iteration["implement"], f"{path}.implement")
    require_keys(implement, f"{path}.implement", ["experiment", "controlled_variables", "changed_variable", "baseline", "expected_evidence"])
    require_list(implement["controlled_variables"], f"{path}.implement.controlled_variables")

    run = require_obj(iteration["run"], f"{path}.run")
    require_keys(run, f"{path}.run", ["command_or_procedure", "inputs", "environment", "observed_output", "execution_status"])
    require_list(run["inputs"], f"{path}.run.inputs")
    if run["execution_status"] not in EXECUTION_STATUSES:
        fail(f"{path}.run.execution_status has invalid value")

    validate = require_obj(iteration["validate"], f"{path}.validate")
    require_keys(validate, f"{path}.validate", ["validation_method", "validation_evidence", "alternative_explanations_considered", "validation_status", "confidence"])
    require_list(validate["alternative_explanations_considered"], f"{path}.validate.alternative_explanations_considered")
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

    select = require_obj(iteration["select"], f"{path}.select")
    require_keys(select, f"{path}.select", ["candidate_next_actions", "selected_action", "reason", "expected_uncertainty_reduction", "stop_or_continue"])
    require_list(select["candidate_next_actions"], f"{path}.select.candidate_next_actions")
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

    budget = require_obj(data["budget"], "budget")
    require_keys(budget, "budget", ["maximum_iterations", "time_budget", "maximum_risky_changes"])

    iterations = require_list(data["iterations"], "iterations")
    if not iterations:
        fail("iterations must contain at least one iteration")
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
    if completion["validation_status"] not in VALIDATION_STATUSES:
        fail("completion_record.validation_status has invalid value")

    print("VALID: uncertainty loop report schema passed")


if __name__ == "__main__":
    main()
