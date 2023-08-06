from typing import List
import requests
from .error import AuthenticationError, ArgumentValidationError, ServerError, OutOfLimitError

UNKNOWN_ERROR = ServerError(
    message="Unknown error.", code=500, status="Internal server error"
)


class Options:
    def __init__(
        self,
        temperature: float = 0.7,
        max_tokens: int = 100,
        top_p: float = 1,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        stop: [str] = ["Q:"],
        best_of: int = 1
    ):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop
        self.best_of = best_of


class Cerebrate:
    def __init__(self, api_key: str, url: str = "https://app.cerebrate.ai/api/predict"):
        self._api_key = api_key
        self._url = url

    def predict(
        self, task: str, examples: [str], query: str, options: Options = None
    ) -> List[str]:
        prompt = task
        if len(examples):
            examples_string = "\n".join(examples)
            prompt += f"\n\nexamples:\n{examples_string}"
        prompt += f"\n\n{query}"

        response = self.__send_request(prompt, options)
        return list(response)

    def raw(self, prompt: str, options: Options = None) -> List[str]:
        response = self.__send_request(prompt, options)

        return list(response)

    def preset_predict(self, preset_id: str, variables=None, options: Options = None):
        if variables is None:
            variables = {}

        response = self.__send_request("default", options, preset_id, variables)

        return list(response)

    def __send_request(self, prompt: str, options: Options = None, preset_id: str = "", variables=None):
        params = dict()
        body = dict()

        if preset_id:
            body["presetId"] = preset_id
            if options:
                params['options'] = 'true'

        if not options:
            options = Options()

        body["data"] = {
                "prompt": prompt,
                "temperature": options.temperature,
                "maxTokens": options.max_tokens,
                "topP": options.top_p,
                "frequencyPenalty": options.frequency_penalty,
                "presencePenalty": options.presence_penalty,
                "stop": options.stop,
                "bestOf": options.best_of,
                "source": "SDK_PYTHON"
            }
        body["parameters"] = variables

        response = requests.post(
            self._url,
            json=body,
            params=params,
            headers={
                "Authorization": self._api_key,
                "Content-Type": "application/json",
            },
        )
        if response.status_code == 200:
            return response.json()

        resp_json = response.json()
        if not resp_json:
            raise UNKNOWN_ERROR

        extensions = resp_json.get("extensions")
        if not extensions:
            raise UNKNOWN_ERROR

        err_code = extensions.get("code")

        if err_code == "UNAUTHENTICATED":
            raise AuthenticationError(
                message=resp_json.get("message"), code=401, status="Unauthorized"
            )

        if err_code == "OUT_OF_LIMIT":
            raise OutOfLimitError(
                message=resp_json.get("message"), code=401, status="Out of limit"
            )

        if err_code == "BAD_USER_INPUT":
            raise ArgumentValidationError(
                message=resp_json.get("message"), code=400, status="Bad request"
            )

        raise ServerError(
            message=resp_json.get("message"), code=500, status="Internal server error"
        )
