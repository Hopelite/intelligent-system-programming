from abc import ABC, abstractmethod
from datetime import datetime
import xml.sax
from typing import TypeVar, Generic
from src.persistence.models import ViewAppointment
from xml.dom.minidom import Document

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
            self.__current_model.patient_date_of_birth = datetime.strptime(content, '%d-%m-%Y').date()
        elif self.current == "appointent_date":
            self.__current_model.appointent_date = datetime.strptime(content, '%d-%m-%Y').date()
        elif self.current == "doctor_name":
            self.__current_model.doctor_name = content
        elif self.current == "conclusion":
            self.__current_model.conclusion = content

    def endElement(self, tag):
        self.current = ""

    def read(self) -> list[ViewAppointment]:
        self.__read_data = []
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        parser.setContentHandler(self)
        parser.parse(self._file_path)

        return self.__read_data

class IXMLWriter(ABC, Generic[T]):
    """Contains method for writing to XML files."""
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    @abstractmethod
    def write(self, data: list[T]) -> None:
        """Writes data to specified XML file."""
        pass

class XMLWriter(IXMLWriter[ViewAppointment]):
    """Implements method for writing to XML files ViewAppointment models."""
    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path
        self.xml_document = Document()

    def write(self, appointments: list[ViewAppointment]) -> None:
        xml_document_data = self.xml_document.createElement("appointments")

        for appointment in appointments:
            xml_document_data.appendChild(self.__parse_appointment(appointment))

        self.xml_document.appendChild(xml_document_data)
        self.xml_document.writexml(open(self.__file_path, 'w'), indent = "  ", addindent = "  ", newl = '\n')
        self.xml_document.unlink()

    def __parse_appointment(self, appointment: ViewAppointment):
        xml_appointment = self.xml_document.createElement("appointment")
        
        xml_appointment.appendChild(self.__parse_property("patient_name", appointment.patient_name))
        xml_appointment.appendChild(self.__parse_property("patient_address", appointment.patient_address))
        xml_appointment.appendChild(self.__parse_property("patient_date_of_birth", appointment.patient_date_of_birth.strftime('%d-%m-%Y')))
        xml_appointment.appendChild(self.__parse_property("appointent_date", appointment.appointent_date.strftime('%d-%m-%Y')))
        xml_appointment.appendChild(self.__parse_property("doctor_name", appointment.doctor_name))
        xml_appointment.appendChild(self.__parse_property("conclusion", appointment.conclusion))

        return xml_appointment

    def __parse_property(self, attribute_name: str, value: str):
        temp_child = self.xml_document.createElement(attribute_name)
        node_text = self.xml_document.createTextNode(value)
        temp_child.appendChild(node_text)
        
        return temp_child