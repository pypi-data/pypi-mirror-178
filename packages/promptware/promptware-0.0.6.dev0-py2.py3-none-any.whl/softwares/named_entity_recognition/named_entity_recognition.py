from __future__ import annotations

from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.licenses import LicenseType
from promptware.promptware import PromptConfig, Promptware
from promptware.tasks import TaskType


class NamedEntityRecognitionPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to extract entity in the text",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            task=TaskType.named_entity_recognition,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=64,
                temperature=0,
            )
        }

    def _software_configs(self):
        return {
            "sentiment_classification": PromptConfig(
                name="named-entity-recognition",
                description="This promptware is used to extract entities in the text",
                instruction="",
                demonstration=[
                    "I will go to Beijing on Saturday.\n"
                    "Entity: Beijing.\n\n"
                    "He is a student in Peking University.\n"
                    "Entity: Peking University\n\n",
                ],
                prompt_template=lambda input: f"{input['text']}\nEntity:",
                task=TaskType.named_entity_recognition,
            )
        }
