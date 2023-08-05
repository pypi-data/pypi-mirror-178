from ikologikapi.domain.AbstractIkologikInstallationObject import AbstractIkologikInstallationObject


class Report(AbstractIkologikInstallationObject):

    def __init__(self, customer: str, installation: str):
        super().__init__(customer, installation)

        self.batch = None
        self.maintenanceTask = None
        self.type = None
        self.lastProcessing = None
        self.nextProcessing = None
        self.lockedUntil = None
        self.reportType = None
        self.startDate = None
        self.endDate = None
        self.title = None
        self.fileName = None
        self.contentType = None
        self.comment = None
        self.sendReviewNotifications = None
        self.sendNotifications = None
        self.user = None
        self.status = None
        self.fields = None
