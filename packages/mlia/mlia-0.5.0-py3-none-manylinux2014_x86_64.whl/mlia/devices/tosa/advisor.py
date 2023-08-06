# SPDX-FileCopyrightText: Copyright 2022, Arm Limited and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0
"""TOSA advisor."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from mlia.core.advice_generation import AdviceCategory
from mlia.core.advice_generation import AdviceProducer
from mlia.core.advisor import DefaultInferenceAdvisor
from mlia.core.advisor import InferenceAdvisor
from mlia.core.context import Context
from mlia.core.context import ExecutionContext
from mlia.core.data_analysis import DataAnalyzer
from mlia.core.data_collection import DataCollector
from mlia.core.events import Event
from mlia.core.typing import PathOrFileLike
from mlia.devices.tosa.advice_generation import TOSAAdviceProducer
from mlia.devices.tosa.config import TOSAConfiguration
from mlia.devices.tosa.data_analysis import TOSADataAnalyzer
from mlia.devices.tosa.data_collection import TOSAOperatorCompatibility
from mlia.devices.tosa.events import TOSAAdvisorStartedEvent
from mlia.devices.tosa.handlers import TOSAEventHandler


class TOSAInferenceAdvisor(DefaultInferenceAdvisor):
    """TOSA inference advisor."""

    @classmethod
    def name(cls) -> str:
        """Return name of the advisor."""
        return "tosa_inference_advisor"

    def get_collectors(self, context: Context) -> list[DataCollector]:
        """Return list of the data collectors."""
        model = self.get_model(context)

        collectors: list[DataCollector] = []

        if AdviceCategory.OPERATORS in context.advice_category:
            collectors.append(TOSAOperatorCompatibility(model))

        return collectors

    def get_analyzers(self, context: Context) -> list[DataAnalyzer]:
        """Return list of the data analyzers."""
        return [
            TOSADataAnalyzer(),
        ]

    def get_producers(self, context: Context) -> list[AdviceProducer]:
        """Return list of the advice producers."""
        return [
            TOSAAdviceProducer(),
        ]

    def get_events(self, context: Context) -> list[Event]:
        """Return list of the startup events."""
        model = self.get_model(context)
        target_profile = self.get_target_profile(context)

        return [
            TOSAAdvisorStartedEvent(model, TOSAConfiguration(target_profile)),
        ]


def configure_and_get_tosa_advisor(
    context: ExecutionContext,
    target_profile: str,
    model: str | Path,
    output: PathOrFileLike | None = None,
    **_extra_args: Any,
) -> InferenceAdvisor:
    """Create and configure TOSA advisor."""
    if context.event_handlers is None:
        context.event_handlers = [TOSAEventHandler(output)]

    if context.config_parameters is None:
        context.config_parameters = _get_config_parameters(model, target_profile)

    return TOSAInferenceAdvisor()


def _get_config_parameters(model: str | Path, target_profile: str) -> dict[str, Any]:
    """Get configuration parameters for the advisor."""
    advisor_parameters: dict[str, Any] = {
        "tosa_inference_advisor": {
            "model": str(model),
            "target_profile": target_profile,
        }
    }

    return advisor_parameters
