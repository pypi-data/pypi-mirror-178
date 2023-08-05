from ikologikapi.domain.AbstractIkologikInstallationObject import AbstractIkologikInstallationObject


class MaintenanceTask(AbstractIkologikInstallationObject):

    def __init__(self, customer: str, installation: str):
        super().__init__(customer, installation)

        self.maintenanceType = None
        self.asset = None

        self.status = 'STATUS_2_PLANNED'
        self.startDate = None
        self.endDate = None
        self.description = None
        self.comment = None

        self.fields = {}
