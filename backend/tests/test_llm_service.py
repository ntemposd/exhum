import unittest
from types import SimpleNamespace

from backend.services.llm_service import LLMService


class LLMServicePromptRoleTests(unittest.IsolatedAsyncioTestCase):
    async def test_call_llm_api_sends_system_and_user_messages(self):
        service = LLMService(
            api_base_url="https://api.example.com/v1",
            api_key="test-key",
            model_id="demo-model",
            max_retries=0,
            throttle_seconds=0.0,
            execution_metrics_builder=lambda **kwargs: SimpleNamespace(**kwargs),
            extract_execution_metrics=lambda *args, **kwargs: SimpleNamespace(generation_duration_ms=1),
            build_stream_execution_metrics=lambda **kwargs: SimpleNamespace(**kwargs),
            logger=SimpleNamespace(error=lambda *args, **kwargs: None),
        )

        captured = {}

        class FakeResponse:
            headers = {}

            def raise_for_status(self):
                return None

            def json(self):
                return {"choices": [{"message": {"content": "Grounded answer."}}]}

        class FakeClient:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                return False

            async def post(self, url, json, headers):
                captured["request_url"] = url
                captured["payload"] = json
                return FakeResponse()

        async def fake_wait_for_provider_slot():
            return None

        service._wait_for_provider_slot = fake_wait_for_provider_slot
        service._http_client_context = lambda timeout: FakeClient()

        agent_config = SimpleNamespace(system_prompt="Speak as Socrates.", temperature=0.7, max_tokens=256)
        await service.call_llm_api("Discussion topic: justice", agent_config)

        messages = captured["payload"]["messages"]
        self.assertEqual(messages[0], {"role": "system", "content": "Speak as Socrates."})
        self.assertEqual(messages[1], {"role": "user", "content": "Discussion topic: justice"})

    def test_gpt_oss_request_uses_low_reasoning_and_token_floor(self):
        service = LLMService(
            api_base_url="https://api.groq.com/openai/v1",
            api_key="test-key",
            model_id="openai/gpt-oss-20b",
            max_retries=0,
            throttle_seconds=0.0,
            debate_max_tokens=768,
            execution_metrics_builder=lambda **kwargs: SimpleNamespace(**kwargs),
            extract_execution_metrics=lambda *args, **kwargs: SimpleNamespace(generation_duration_ms=1),
            build_stream_execution_metrics=lambda **kwargs: SimpleNamespace(**kwargs),
            logger=SimpleNamespace(error=lambda *args, **kwargs: None),
        )
        agent_config = SimpleNamespace(system_prompt="Speak as Socrates.", temperature=0.7, max_tokens=280)
        request = service.build_provider_request(
            messages=[{"role": "user", "content": "hello"}],
            agent_config=agent_config,
            stream=True,
        )

        self.assertEqual(request["body"]["model"], "openai/gpt-oss-20b")
        self.assertEqual(request["body"]["reasoning_effort"], "low")
        self.assertFalse(request["body"]["include_reasoning"])
        self.assertEqual(request["body"]["max_tokens"], 640)


if __name__ == "__main__":
    unittest.main()
