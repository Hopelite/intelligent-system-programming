from abc import ABC, abstractmethod
from datetime import date, datetime
import xml.sax
from typing import TypeVar, Generic
from src.persistence.models import ViewAppointment

T = TypeVar('T')

class IXMLReader(ABC, Generic[T]):
    """Contains method for reading XML files."""
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    @abstractmethod
    def read(self) -> list[T]:
        """Reads data from specified XML file."""
        pass

class XMLReader(IXMLReader[ViewAppointment], xml.sax.ContentHandler):
    """Implements method for reading XML files and parses it to ViewAppointment models."""
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.__read_data = []
        self.parser = xml.sax.make_parser()

    def startElement(self, tag, attributes):
        self.current = tag
        if tag == "appointment":
            self.__current_model = ViewAppointment()
            self.__read_data.append(self.__current_model)
            pass

    def characters(self, content):
        if self.current == "patient_name":
            self.__current_model.patient_name = content
        elif self.current == "patient_address":
            self.__current_model.patient_address = content
        elif self.current == "patient_date_of_birth":
            self.__current_model.patient_date_of_birth = datetime.strptime(content, '%m-%d-%Y').date()
        elif self.current == "appointent_date":
            self.__current_model.appointent_date = datetime.strptime(content, '%m-%d-%Y').date()
        elif self.current == "doctor_name":
            self.__current_model.doctor_name = content
        elif self.current == "conclusion":
            self.__current_model.conclusion = content

    def endElement(self, tag):
        self.current = ""

    def read(self) -> list[T]:
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        parser.setContentHandler(self)
        parser.parse(self._file_path)

        return self.__read_data
