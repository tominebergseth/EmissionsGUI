# Tomine Bergseth, bergseth@usc.edu
# ITP 116, Spring 2022, 11-11.50am
# Final Project
# Description:
# Appearing as a GUI to the user, this program will ask the user to input the names of two countries
# It will then connect to the Climatiq API and output data on CO2 emissions for electricity generation - WWT

from tkinter import *
import requests
import json
from PIL import Image, ImageTk


class EmissionTracker:
    def __init__(self):

        root = Tk()
        root.title("The Global CO2 Tracker")
        root.geometry("600x600")
        root.configure(bg="#F0F8FF")
        self.myFrame = Frame(root)
        self.myFrame.config(bg="#F0F8FF")
        self.myFrame.grid()

        self.main_title = Label(self.myFrame, text="The Global CO2 Tracker")
        self.main_title.config(font="Arial 20 bold", fg="black", bg="#F0F8FF", anchor="n")
        self.main_title.grid(sticky="n")

        self.welcomeText = Label(self.myFrame,
                                 text="Welcome! Please enter two countries below to compare their emissions for electrity generation.")
        self.welcomeText.config(font="Arial 10", fg="black", bg="#F0F8FF")
        self.welcomeText.grid(sticky="n")

        self.resultLabel = Label(self.myFrame)
        self.resultLabel.grid(sticky="n")

        self.country1Label = Label(self.myFrame, text="Enter the name of a country:")
        self.country1Label.config(bg="black", fg="white")
        self.country1Label.grid(sticky="n")
        self.enterCountry1 = Entry(self.myFrame, highlightthickness=6)
        self.enterCountry1.config(highlightcolor="black", highlightbackground="black")
        self.enterCountry1.grid(sticky="n")

        self.country2Label = Label(self.myFrame, text="Enter the name of a second country:")
        self.country2Label.config(bg="black", fg="white")
        self.country2Label.grid(sticky="n")
        self.enterCountry2 = Entry(self.myFrame, highlightthickness=6)
        self.enterCountry2.config(highlightcolor="black", highlightbackground="black")
        self.enterCountry2.grid(sticky="n")

        self.retrieveEmissionsButton = Button(self.myFrame, text="Retrieve emission data", command=self.buttonClicked)
        self.retrieveEmissionsButton.config(font="Arial 10", fg="white", bg="black")
        self.retrieveEmissionsButton.grid(sticky="n")

        self.blankLabel = Label(self.myFrame)
        self.blankLabel.grid()

        self.restartButton = Button(self.myFrame, text="Restart", command=self.restartProgram)
        self.restartButton.config(font="Arial 10", fg="white", bg="black")

        self.statusMessageLabel = Label(self.myFrame)

        self.globe = Image.open("globe.png")
        self.resizedGlobe = self.globe.resize((200, 200))
        self.globeImage = ImageTk.PhotoImage(self.resizedGlobe)
        self.imageLabel = Label(self.myFrame, image=self.globeImage)
        self.imageLabel.config(bg="#F0F8FF", anchor="n")
        self.imageLabel.grid(sticky="n")

        self.blankLabel2 = Label(self.myFrame)
        self.blankLabel2.grid()
        self.exitButton = Button(self.myFrame, text="Exit", command=self.exitProgram)
        self.exitButton.config(font="Arial 10", fg="white", bg="black")
        self.exitButton.grid(sticky="n")

        # define values/member variables
        self.country1 = ""
        self.country2 = ""
        self.base = "https://beta3.api.climatiq.io"
        self.headers = {'Authorization': 'API key'}
        self.query = "/search?query=&year=2021&category=Electricity&source=BEIS"
        self.countryDict = {}
        self.co2Dict = {}
        self.regionList = []
        self.resultList = []

        self.formattedCountry = ""
        self.firstUpper = ""

        self.co2_1 = 0
        self.co2_2 = 0
        self.biggestContributor = ""
        self.diff = 0
        self.percentageDiff = 0

        self.countryDict = self.callAPIcountry()
        self.co2Dict = self.callAPIco2()

    def buttonClicked(self, event=None):
        self.country1 = self.enterCountry1.get()
        self.country1 = self.country1.strip()

        self.country2 = self.enterCountry2.get()
        self.country2 = self.country2.strip()

        """
        if not self.country1.isalpha():
            self.welcomeText.config(text="Error: invalid country name. Please only enter alphabetic characters.",
                                    fg="red")
        elif not self.country2.isalpha():
            self.welcomeText.config(text="Error: invalid country name. Please only enter alphabetic characters.",
                                    fg="red")
        else:
        """

        self.country1 = self.formatCountry(self.country1)
        self.country2 = self.formatCountry(self.country2)
        if self.country1 not in self.countryDict:
            self.welcomeText.config(text="                               Sorry, we do not have data on \"" + self.country1 + "\". Please try again.                               ", fg="red")
        elif self.country2 not in self.countryDict:
            self.welcomeText.config(text="                               Sorry, we do not have data on \"" + self.country2 + "\". Please try again.                               ", fg="red")
        else:
            self.co2_1 = self.co2Dict[self.country1][1]
            self.co2_2 = self.co2Dict[self.country2][1]

            self.welcomeText.config(text="")
            self.enterCountry1.grid_remove()
            self.enterCountry2.grid_remove()
            self.retrieveEmissionsButton.grid_remove()
            self.imageLabel.grid_remove()
            self.blankLabel.grid_remove()
            self.exitButton.grid_remove()

            if self.co2_1 > self.co2_2:
                self.biggestContributor = self.country1
                self.diff = self.co2_1 - self.co2_2
                self.percentageDiff = self.diff / 100
                self.resultLabel.config(text=self.country1 + " emitted " + str(
                self.co2_1) + " kg/kWh CO2 for elecrtricity generation - WWT in 2021.", fg="red", bg="#F0F8FF",
                                            anchor="n", font="Arial 10 bold")
                self.resultLabel.grid(sticky="n")
                self.country1Label.config(text=self.country2 + " emitted " + str(
                        self.co2_2) + " kg/kWh CO2 for elecrtricity generation - WWT in 2021.", fg="green",
                                              bg="#F0F8FF", anchor="n", font="Arial 10 bold")
                self.country2Label.config(
                        text=self.biggestContributor + "'s emissions were " + str(self.percentageDiff) + " % higher.",
                        bg="#F0F8FF", anchor="n", fg="black", font="Arial 10 bold")
            elif self.co2_1 < self.co2_2:
                self.biggestContributor = self.country2
                self.diff = self.co2_2 - self.co2_1
                self.percentageDiff = self.diff / 100
                self.resultLabel.config(text=self.country1 + " emitted " + str(
                        self.co2_1) + " kg/kWh CO2 for elecrtricity generation - WWT in 2021.", fg="green",
                                            bg="#F0F8FF", anchor="n", font="Arial 10 bold")
                self.resultLabel.grid(sticky="n")
                self.country1Label.config(text=self.country2 + " emitted " + str(
                        self.co2_2) + " kg/kWh CO2 for elecrtricity generation - WWT in 2021.", fg="red", bg="#F0F8FF",
                                              font="Arial 10 bold")
                self.country2Label.config(
                        text=self.biggestContributor + "'s emissions were " + str(self.percentageDiff) + " % higher.",
                        bg="#F0F8FF", anchor="n", fg="black", font="Arial 10 bold")
            else:
                self.resultLabel.config(text=self.country1 + " emitted " + str(
                        self.co2_1) + " kg/kWh CO2 for elecrtricity generation - WWT in 2021.", fg="yellow",
                                            bg="#F0F8FF", anchor="n", font="Arial 10 bold")
                self.resultLabel.grid(sticky="n")
                self.country1Label.config(text=self.country2 + " emitted " + str(
                        self.co2_2) + " kg/kWh CO2 for elecrtricity generation - WWT in 2021.", fg="yellow",
                                              bg="#F0F8FF", anchor="n", font="Arial 10 bold")
                self.country2Label.config(
                        text=self.country1 + " and " + self.country2 + " emitted the same amount of CO2 for electricity generation - WWT in 2021",
                        bg="#F0F8FF", anchor="n", fg="black", font="Arial 10 bold")

        self.blankLabel.grid()
        self.imageLabel.grid(sticky="n")
        self.statusMessageLabel.grid()
        self.restartButton.grid(sticky="n")
        self.exitButton.grid(sticky="n")

    def callAPIcountry(self):
        response = requests.get(self.base + self.query, headers=self.headers)

        if response.status_code == 200:
            # Get from - to page
            jsonRes = json.loads(response.content)
            countryDict = self.getCountryDict(jsonRes)

        else:
            print(
                f"Error - not abe to run query {self.query} - code : {response.status_code} - error : {response.reason}")

        return countryDict

    def callAPIco2(self):
        co2Dict = {}
        response = requests.get(self.base + self.query, headers=self.headers)

        lastPage = 1
        if response.status_code == 200:
            # Get from - to page
            jsonRes = json.loads(response.content)
            lastPage = int(jsonRes["last_page"])

            # Get res for first page
            co2Dict = self.getCO2Dict(co2Dict, jsonRes)

        else:
            print(
                f"Error - not abe to run query {self.query} - code : {response.status_code} - error : {response.reason}")

        if lastPage > 1:
            for num in range(2, lastPage):
                pageQuery = f"{self.query}&page={num}"

                response = requests.get(self.base + pageQuery, headers=self.headers)
                if response.status_code == 200:
                    jsonRes = json.loads(response.content)
                    co2Dict = self.getCO2Dict(co2Dict, jsonRes)

                else:
                    print(
                        f"Error - not abe to run query {self.query} - code : {response.status_code} - error : {response.reason}")

        return co2Dict

    def getCountryDict(self, jsonRes):
        countryDict = {}

        regionList = jsonRes["possible_filters"]["region"]
        for region in regionList:
            countryDict[region["name"]] = region["id"]

        return countryDict

    def getCO2Dict(self, co2Dict, jsonRes):

        resultList = jsonRes["results"]
        for result in resultList:
            co2Dict[result["region_name"]] = [result["region"], result["constituent_gases"]["co2e_total"],
                                              result["name"], result["category"], result["source"], result["unit"]]

        return co2Dict

    def formatCountry(self, country):
        self.formattedCountry = ""
        if len(country) > 0:
            for word in country.split(' '):
                # lowercase = word.lower()
                # firstUpper = lowercase[0].upper() + lowercase[1:]
                self.firstUpper = word.title()
                if len(self.formattedCountry) > 0:
                    self.formattedCountry = self.formattedCountry + " " + self.firstUpper
                else:
                    self.formattedCountry = self.firstUpper
        return self.formattedCountry

    def restartProgram(self):
        self.welcomeText.config(
            text="Welcome! Please enter two countries below to compare their emissions for electrity generation.",
            font="Arial 10", fg="black", bg="#F0F8FF")
        self.welcomeText.grid(sticky="n")
        self.resultLabel.grid_remove()
        self.country1Label.config(text="Enter the name of a country:", bg="black", fg="white")
        self.country1Label.grid()
        self.enterCountry1.config(highlightthickness=6, highlightcolor="black", highlightbackground="black")
        self.enterCountry1.grid()
        self.country2Label.config(text="Enter the name of a second country:", bg="black", fg="white")
        self.country2Label.grid()
        self.enterCountry2.config(highlightthickness=6, highlightcolor="black", highlightbackground="black")
        self.enterCountry2.grid()
        self.retrieveEmissionsButton.config(state=ACTIVE, text="Retrieve emission data", font="Arial 10", fg="white",
                                            bg="black", command=self.buttonClicked)
        self.retrieveEmissionsButton.grid()
        self.restartButton.grid_remove()

    def exitProgram(self):
        self.myFrame.destroy()


def main():
    e = EmissionTracker()
    e.myFrame.mainloop()


main()

