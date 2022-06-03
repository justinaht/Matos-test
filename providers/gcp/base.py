# -*- coding: utf-8 -*-
import os
import json
import structlog
from utils.encryption import Encryptor

from google.oauth2.service_account import Credentials

logger = structlog.get_logger(__file__)


class BaseGCPManager:
    _credentials = None
    _project_id = None
    _gcp_svc_account_file = None
    _account_info = None
    _cred_mode = 'file'

    def __init__(self, **kwargs):
        self.SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
        svc_account_filename = "google_service_account.json"
        gcp_svc_account_path = os.getenv("GCP_SVC_ACCOUNT_PATH", "credentials")
        self._gcp_svc_account_file = os.path.join(gcp_svc_account_path, svc_account_filename)
        try:
            self._account_info = json.load(open(self._gcp_svc_account_file))
            self._project_id = self._account_info.get('project_id', '')
        except:
            log = logger.bind()
            GCP_ACCOUNT_FILE_EXCEPTION = "Not found account service json for GCP - credentials/google_service_account.json"
            log.exception(GCP_ACCOUNT_FILE_EXCEPTION)
            raise Exception(GCP_ACCOUNT_FILE_EXCEPTION)

    @property
    def credentials(self):
        """
        """

        if self._credentials is not None:
            return self._credentials

        try:
            self._credentials = Credentials.from_service_account_info(
                self._account_info, scopes=self.SCOPES
            )
        except Exception as ex:
            log = logger.bind()
            log.exception(ex)
            raise Exception(ex)

        return self._credentials

    @property
    def projectId(self):
        if not self._project_id:
            raise Exception("No project ID found.")
        return self._project_id
