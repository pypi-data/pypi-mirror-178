# Models for PowerschoolPy
from dataclasses import dataclass
from typing import Any, Dict, List
from attr import dataclass

@dataclass
class Student:
    """ Defines a student """
    studentId: int
    studentDcid: int
    firstName: str
    middleName: str
    lastName: str
    gradeLevel: int
    currentMealBalance: float
    currentGPA: float
    courses: List

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """ Return a student object from PowerSchool """
        return Student(
            studentId = data["studentId"],
            studentDcid = data["studentDcid"],
            firstName = data["student"]["firstName"],
            middleName = data["student"]["middleName"],
            lastName = data["student"]["lastName"],
            gradeLevel = data["student"]["gradeLevel"],
            currentMealBalance = data["student"]["currentMealBalance"],
            currentGPA = data["student"]["currentGPA"],
            courses = []
        )

@dataclass
class Course:
    """ Defines a course """
    id: int
    dcid: int
    courseName: str
    courseCode: str
    roomNumber: int
    period: int
    teacherId: int

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        """ Return a student object from PowerSchool """
        return Course(
            id = data["sections"]["id"],
            dcid = data["sections"]["dcid"],
            courseName = data["sections"]["schoolCourseTitle"],
            courseCode = data["sections"]["courseCode"],
            roomNumber = data["sections"]["roomName"],
            period = data["sections"]["periodSort"],
            teacherId = data["sections"]["teacherID"]
        )

# @dataclass
# class Assignment:
#     """ Defines an assignment"""
#     assignmentID: int
#     name: str
#     grade: str
#     percent: str
#     isMissing : bool
#     wasLate: bool
#     duedate: str

#     def from_dict(data: Dict[str, Any]):
#         """ Return a student object from PowerSchool """
#         return Assignment(
#             assignmentID = data["assignmentScores"]["assignmentId"],
#             name = data["assignmentScores"]["name"],
#             grade = data["assignmentScores"]["grade"],
#             percent = data["assignmentScores"]["percent"],
#             isMissing = data["assignmentScores"]["isMissing"],
#             wasLate = data["assignmentScores"]["wasLate"],
#             duedate = data["assignmentScores"]["duedate"]
#         )

    # 'finalGrades': [
    #     {
    #         'commentValue': 'Works diligently and cares to complete work to the best quality. Shows positive character.',
    #         'dateStored': None,
    #         'grade': 'A',
    #         'id': 546481,
    #         'percent': 100.0,
    #         'reportingTermId': 1002352,
    #         'sectionid': 48013,
    #         'storeType': 2
    #     },


            # assignments
    # 'assignmentScores': [
    #     {
    #         'assignmentId': 140279,
    #         'collected': False,
    #         'comment': None,
    #         'exempt': False,
    #         'gradeBookType': 2,
    #         'id': 2023294,
    #         'incomplete': False,
    #         'late': False,
    #         'letterGrade': 'A',
    #         'missing': False,
    #         'percent': '100.0',
    #         'score': '3.0',
    #         'scoretype': 0
    #     },

    #   'assignments': [
    #     {
    #         'abbreviation': None,
    #         'additionalCategoryIds': [],
    #         'assignmentid': 111692,
    #         'categoryId': 743,
    #         'description': None,
    #         'dueDate': datetime.datetime(2022, 9, 16, 7, 0, tzinfo=<isodate.tzinfo.Utc object at 0x0000022CC98C27A0>),
    #         'gradeBookType': 2,
    #         'id': 140279,
    #         'includeinfinalgrades': 1,
    #         'name': 'Daily Health #1',
    #         'pointspossible': 3.0,
    #         'publishDaysBeforeDue': 0,
    #         'publishState': 0,
    #         'publishonspecificdate': datetime.datetime(2022, 11, 4, 7, 0, tzinfo=<isodate.tzinfo.Utc object at 0x0000022CC98C27A0>),
    #         'publishscores': 1,
    #         'sectionDcid': 46758,
    #         'sectionid': 47884,
    #         'type': 0,
    #         'weight': 1.0
    #     },      