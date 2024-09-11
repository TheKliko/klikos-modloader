import logging
import notifypy

from modules.other.project import Project


class Notification:
    def __init__(self) -> None:
        self.notification = notifypy.Notify()
        self._default()
    
    def _default(self) -> None:
        self.notification.application_name = Project.NAME
        self.notification.icon = Project.ICON

    def send(self, title: str, message: str) -> None:
        logging.info(f'Sending notification: {title}')
        self.notification.title = title
        self.notification.message = message
        self.notification.send(block=False)