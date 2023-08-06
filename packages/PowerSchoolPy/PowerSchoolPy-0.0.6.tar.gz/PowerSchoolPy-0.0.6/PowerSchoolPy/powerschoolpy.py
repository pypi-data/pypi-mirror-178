#!/usr/bin/env python3
import zeep, requests, logging
import zeep.helpers
from .exceptions import PowerschoolPyError
from .models import Student, Course


class PowerschoolPy:
    """The client for connecting to powerschool

    Client(base_url, api_username="pearson", api_password="m0bApP5")

    A client for using powerschool methods"""

    def __init__(self, host, api_username="pearson", api_password="m0bApP5"):
        self._api_username = api_username
        self._api_password = api_password
        self._host = host
        # logging.basicConfig(level=logging.CRITICAL)
        # session = requests.session()
        # session.auth = requests.auth.HTTPDigestAuth(api_username, api_password)
        # if host[:-1] != "/":
        #     host += "/"
        # self.url = host + "pearson-rest/services/PublicPortalServiceJSON"
        # try:
        #     self.client = zeep.Client(
        #         wsdl=self.url + "?wsdl",
        #         transport=zeep.transports.Transport(session=session),
        #     )
        # except requests.exceptions.ConnectionError:
        #     raise PowerschoolPyError(f"Could not connect to {host}.")
        # except requests.exceptions.HTTPError:
        #     raise PowerschoolPyError(
        #         f"Incorrect api credentials {api_username}, {api_password}"
        #     )

    async def login(self):
        logging.basicConfig(level=logging.CRITICAL)
        session = requests.session()
        session.auth = requests.auth.HTTPDigestAuth(
            self._api_username, self._api_password
        )
        if self._host[:-1] != "/":
            self._host += "/"
        self._url = self._host + "pearson-rest/services/PublicPortalServiceJSON"
        try:
            self.client = zeep.Client(
                wsdl=self._url + "?wsdl",
                transport=zeep.transports.Transport(session=session),
            )
        except requests.exceptions.ConnectionError:
            raise PowerschoolPyError(f"Could not connect to {host}.")
        except requests.exceptions.HTTPError:
            raise PowerschoolPyError(
                f"Incorrect api credentials {api_username}, {api_password}"
            )
        return True

    async def getStudent(self, username, password, studentIDToFind=None):
        studentCounter = 0

        service = self.client.create_service(
            "{http://publicportal.rest.powerschool.pearson.com}PublicPortalServiceJSONSoap12Binding",
            self._url,
        )
        result = service.loginToPublicPortal(username, password)["userSessionVO"]

        if result["userId"] == None:
            raise PowerschoolPyError(
                "Could not log in to ({}, {})".format(username, password)
            )

        userSessionVO = {
            "userId": result["userId"],
            "serviceTicket": result["serviceTicket"],
            "serverInfo": {"apiVersion": result["serverInfo"]["apiVersion"]},
            "serverCurrentTime": result["serverCurrentTime"],
            "userType": result["userType"],
        }

        for studentID in result["studentIDs"]:
            if studentIDToFind == None:
                student = Student.from_dict(
                    service.getStudentData(
                        userSessionVO, result["studentIDs"][0], {"includes": "1"}
                    )["studentDataVOs"][0]
                )
                # sections = result["studentIDs"][0]["sections"]
                # for course in sections:
                #     student.courses.append(Course.from_dict(course))
            elif studentID == studentIDToFind:
                student = service.getStudentData(
                    userSessionVO,
                    result["studentIDs"][studentCounter],
                    {"includes": "1"},
                )["studentDataVOs"][0]
                # for course in result["studentIDs"][studentCounter]["sections"]:
                #     student.courses.append(Course.from_dict(course))

            studentCounter = studentCounter + 1

            # for course in result["sections"]:
            #     courses.append(Course.from_dict(course))

        # return Student.from_dict(student)
        return student

    async def getStudents(self, username, password):
        students = []
        studentCounter = 0

        service = self.client.create_service(
            "{http://publicportal.rest.powerschool.pearson.com}PublicPortalServiceJSONSoap12Binding",
            self._url,
        )
        result = service.loginToPublicPortal(username, password)["userSessionVO"]

        if result["userId"] == None:
            raise PowerschoolPyError(
                "Could not log in to ({}, {})".format(username, password)
            )

        userSessionVO = {
            "userId": result["userId"],
            "serviceTicket": result["serviceTicket"],
            "serverInfo": {"apiVersion": result["serverInfo"]["apiVersion"]},
            "serverCurrentTime": result["serverCurrentTime"],
            "userType": result["userType"],
        }

        for studentID in result["studentIDs"]:
            # students.append(service.getStudentData(userSessionVO, result["studentIDs"][studentCounter], {"includes": "1"})["studentDataVOs"][0])
            student = Student.from_dict(
                service.getStudentData(
                    userSessionVO,
                    result["studentIDs"][studentCounter],
                    {"includes": "1"},
                )["studentDataVOs"][0]
            )
            students.append(student)
            studentCounter = studentCounter + 1

        return students
