from ikologikapi.IkologikApiCredentials import IkologikApiCredentials
from ikologikapi.services.AbstractIkologikInstallationService import AbstractIkologikInstallationService


class ReportTypeService(AbstractIkologikInstallationService):

    def __init__(self, jwtHelper: IkologikApiCredentials):
        super().__init__(jwtHelper)

    # CRUD actions

    def get_url(self, customer: str, installation: str) -> str:
        return f'{self.jwtHelper.get_url()}/api/v2/customer/{customer}/installation/{installation}/reporttype'
