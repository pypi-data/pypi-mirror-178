from dataclasses import asdict

from coiote.utils import ApiEndpoint, api_call
from coiote.v3.model.cert_auth import CertificateData


class CertAuth(ApiEndpoint):
    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs, api_url="auth/certificates")

    @api_call()
    def add_certificate(self, certificate: CertificateData):
        return self.session.post(self.get_url(), json=asdict(certificate))

    @api_call()
    def delete_certificate(self):
        return self.session.delete(self.get_url())
