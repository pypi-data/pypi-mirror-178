class Question:
    def __init__(self, question, quesnumber, answer):
        self.question = question,
        self.quesnumber = quesnumber,
        self.answer = answer


class Student:
    def __init__(self, name, major, gpa, age, is_on_probation):
        self.name = name,
        self.major = major,
        self.gpa = gpa,
        self.age = age,
        self.is_on_probation = is_on_probation


class Human:
    def __init__(self, dob, age, name, gender, iq, height, weight):
        self.dob = dob,
        self.age = age,
        self.name = name,
        self.gender = gender,
        self.iq = iq,
        self.height = height,
        self.weight = weight,


class Smart_Phone:
    def __init__(self, model, company, os, specification, color, is_broken):
        self.model = model,
        self.company = company,
        self.os = os,
        self.specification = specification
        self.color = color
        self.is_broken = is_broken


class Game:
    def __init__(self, name, version, game_type, author):
        self.name = name
        self.version = version
        self.game_type = game_type
        self.author = author

