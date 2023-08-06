import logging
import time
from typing import Any, Dict, List, Optional, Set

from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests import HTTPError
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from resistant_documents_client.base import ApiClientBase, ResistantApiException
from resistant_documents_client.model import AnalysisFeedback

logger = logging.getLogger(__name__)


class ClientCredentialsSession(OAuth2Session):
    """The Resistant Documents API client session - see https://documents.resistant.ai/docs/v2.html#section/Authentication"""

    def __init__(self, client_id: str, client_secret: str, token_url: str, scope: List[str], num_retries_on_oauth_error: int = 5):
        super().__init__(client_id=client_id, client=BackendApplicationClient(client_id=client_id), scope=scope)
        self.token_url = token_url
        self.client_secret = client_secret
        self.num_retries_on_oauth_error = num_retries_on_oauth_error

    def request(self, method, url, data=None, headers=None, withhold_token=False, client_id=None, client_secret=None, **kwargs):
        for i in range(self.num_retries_on_oauth_error):
            try:
                if url != self.token_url:
                    if not self.token or self.token.get("expires_at", 0) < time.time():
                        self.fetch_token(
                            self.token_url,
                            auth=HTTPBasicAuth(client_id or self.client_id, client_secret or self.client_secret),
                            body=f'scope={" ".join(self.scope)}'
                        )
                return super().request(method, url, data, headers, withhold_token, client_id, client_secret, **kwargs)
            except TokenExpiredError:
                logger.debug("Token expired, retrying %d/%d", i, self.num_retries_on_oauth_error)
        else:
            raise RuntimeError("Cannot receive correct token.")


class ResistantDocumentsClient(ApiClientBase):
    """The Resistant Documents API client - see https://documents.resistant.ai/docs/v2.html"""
    SUBMISSIONS_SCOPES = ("submissions.read", "submissions.write")
    PROD_API_URL = "https://api.documents.resistant.ai"
    PROD_TOKEN_URL = "https://eu.id.resistant.ai/oauth2/aus2un1hkrKhPjir4417/v1/token"

    _SUBMIT_ENDPOINT = "/v2/submission"
    _DELETE_ENDPOINT = "/v2/submission/{submission_id}"
    _FRAUD_ENDPOINT = "/v2/submission/{submission_id}/fraud"
    _CONTENT_ENDPOINT = "/v2/submission/{submission_id}/content"
    _QUALITY_ENDPOINT = "/v2/submission/{submission_id}/quality"
    _DECISION_ENDPOINT = "/v2/submission/{submission_id}/decision"
    _FEEDBACK_ENDPOINT = "/v2/submission/{submission_id}/feedback"
    _CHARACTERISTICS_ENDPOINT = "/v2/submission/{submission_id}/characteristics"
    _CLASSIFICATION_ENDPOINT = "/v2/submission/{submission_id}/classification"

    def __init__(self, client_id: str, client_secret: str, token_url: str = PROD_TOKEN_URL,
                 api_url: str = PROD_API_URL,
                 scopes: List[str] = SUBMISSIONS_SCOPES,
                 proxy: Optional[str] = None,
                 **kwargs
                 ) -> None:
        self.api_url = api_url if api_url[-1] != "/" else api_url[:-1]
        if not client_id or not client_secret:
            raise ValueError("Fill client id and client secret properly, at least one of them is empty or None.")

        api_session = ClientCredentialsSession(client_id, client_secret, token_url, scopes)
        super().__init__(api_session, proxy=proxy, **kwargs)

    @property
    def _submit_url(self) -> str:
        return f"{self.api_url}{ResistantDocumentsClient._SUBMIT_ENDPOINT}"

    @property
    def _delete_url(self) -> str:
        return f"{self.api_url}{ResistantDocumentsClient._DELETE_ENDPOINT}"

    @property
    def _fraud_url(self):
        return f"{self.api_url}{ResistantDocumentsClient._FRAUD_ENDPOINT}"

    @property
    def _content_url(self):
        return f"{self.api_url}{ResistantDocumentsClient._CONTENT_ENDPOINT}"

    @property
    def _quality_url(self):
        return f"{self.api_url}{ResistantDocumentsClient._QUALITY_ENDPOINT}"

    @property
    def _decision_url(self):
        return f"{self.api_url}{ResistantDocumentsClient._DECISION_ENDPOINT}"

    @property
    def _feedback_url(self) -> str:
        return f"{self.api_url}{ResistantDocumentsClient._FEEDBACK_ENDPOINT}"

    @property
    def _characteristics_url(self) -> str:
        return f"{self.api_url}{ResistantDocumentsClient._CHARACTERISTICS_ENDPOINT}"

    @property
    def _classification_url(self) -> str:
        return f"{self.api_url}{ResistantDocumentsClient._CLASSIFICATION_ENDPOINT}"

    def submit(self,
               data: bytes,
               query_id: str = "",
               pipeline_configuration: Optional[str] = None,
               enable_decision: bool = False,
               enable_submission_characteristics: bool = False):
        """Create a new submission for a document to be analyzed and get its submission ID."""
        return self._submit(self._submit_url, data, query_id, pipeline_configuration, enable_decision=enable_decision,
                            enable_submission_characteristics=enable_submission_characteristics)

    def fraud(self, submission_id: str, max_num_retries: int = ApiClientBase.MAX_NUM_RETRIES_POLL, with_metadata: Optional[bool] = None) -> dict:
        """Fetch fraud analysis result for given submission ID."""
        try:
            query_params = {"with_metadata": with_metadata} if with_metadata is not None else None
            return self._poll(self._fraud_url, submission_id, max_num_retries, query_params)
        except HTTPError as e:
            if e.response.status_code == 400:
                presign_response = self._api_session.get(self._fraud_url.format(submission_id=submission_id), params={"presign": True})
                presign_response.raise_for_status()
                data_response = self._s3_session.get(presign_response.json()["download_url"])
                data_response.raise_for_status()
                return data_response.json()
            else:
                raise e

    def content(self, submission_id: str, max_num_retries: int = ApiClientBase.MAX_NUM_RETRIES_POLL) -> dict:
        """Fetch document content extraction result for given submission ID."""
        return self._poll(self._content_url, submission_id, max_num_retries)

    def quality(self, submission_id: str, max_num_retries: int = ApiClientBase.MAX_NUM_RETRIES_POLL) -> dict:
        """Fetch document quality analysis result for given submission ID."""
        return self._poll(self._quality_url, submission_id, max_num_retries)

    def analyze(self, data: bytes, query_id: str = "", max_num_retries: int = ApiClientBase.MAX_NUM_RETRIES_POLL) -> dict:
        """Get the provided fraud document analyzed and fetch the result."""
        submission_id = self.submit(data, query_id)
        return self.fraud(submission_id, max_num_retries)

    def decision(self, submission_id: str, embed: Optional[Set[str]] = None, max_num_retries: int = ApiClientBase.MAX_NUM_RETRIES_POLL) -> dict:
        """Fetch the Adaptive Decision result for given submission ID."""
        query_params = {}
        if embed:
            query_params["embed"] = ",".join(embed)
        return self._poll(self._decision_url, submission_id, max_num_retries, query_params=query_params)

    def feedback(self, submission_id: str) -> Optional[dict]:
        """Get custom feedback for the document analysis result previously stored with a PUT request to this endpoint"""
        response = self._api_session.get(self._feedback_url.format(submission_id=submission_id))
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()

    def add_feedback(self, submission_id: str, analysis_feedback: AnalysisFeedback, comment: Optional[str] = None) -> dict:
        """Add custom feedback for the document analysis result. Comment value is sanitized."""
        body = {"analysis_feedback": analysis_feedback, "comment": comment}
        response = self._api_session.put(self._feedback_url.format(submission_id=submission_id), json=body)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise ResistantApiException(f"Add feedback failed, submission {submission_id} not found")
        else:
            response.raise_for_status()

    def add_characteristics(self, submission_id: str, submission_characteristics: Dict[str, Any]) -> None:
        """Attach submission characteristics to the submission."""
        response = self._api_session.put(self._characteristics_url.format(submission_id=submission_id), json=submission_characteristics)
        if response.status_code == 404:
            raise ResistantApiException(f"Add submission characteristics failed, submission {submission_id} not found")
        else:
            response.raise_for_status()

    def delete(self, submission_id: str) -> None:
        """Permanently deletes the submission. E.g. to remove a document before the configured retention period."""
        response = self._api_session.delete(self._delete_url.format(submission_id=submission_id))
        if response.status_code == 404:
            raise ResistantApiException(f"Delete submission failed, submission {submission_id} not found")
        elif response.status_code == 409:
            raise ResistantApiException(f"Delete submission failed, submission {submission_id} not ready")
        else:
            response.raise_for_status()

    def classification(self, submission_id: str) -> Optional[dict]:
        """Fetch classification of the type of the submitted document."""
        response = self._api_session.get(self._classification_url.format(submission_id=submission_id))
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()
