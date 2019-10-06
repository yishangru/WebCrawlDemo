# -*- coding:utf-8 -*-
import time
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys # 回车，点击等鼠标键盘操作

"""setting the chrome driver for data crawling"""
chromeDriver = webdriver.Chrome(executable_path="chromedriver.exe")  # "chromedriver.exe" is a file put under the same directory


"""load required search condition from file"""
movieInfoHolder = [("Testament of Youth", "2014")]


"""url or link of the website to crawl"""
websiteCrawling = "https://www.imdb.com"


"""crawl data from website: we search three movie released on specific year based on its name and get its director info and country information"""
movieDirectorCrawled = list()
movieRatingCrawled = list()
for movie in movieInfoHolder:
    # visit the website
    chromeDriver.get(websiteCrawling)
    # locate and find search bar by xpath
    searchBar = chromeDriver.find_element_by_xpath(".//input[@type='text'][@name='q'][@id='navbar-query']")
    # input movie name, movie[0] + Keys.ENTER perform the same as following button click
    searchBar.send_keys(movie[0])
    # locate and find search button by xpath
    searchButton = chromeDriver.find_element_by_xpath(".//button[@id='navbar-submit-button'][@type='submit']")
    # click the search button
    searchButton.click()
    # sleep one seconds for loading the search results
    time.sleep(1)
    try:
        # locate the section for movies, there are multiple "table" element with class as "findList", we want the first one
        movieItemSection = chromeDriver.find_element_by_xpath(".//*[@id='main']/div/div[2]/table")
        # find all movie items related with the searching movie name
        movieItems = movieItemSection.find_elements_by_tag_name("tr")
        for movieRelated in movieItems:
            movieInfo = movieRelated.find_element_by_xpath(".//td[@class='result_text']")
            movieLink = movieInfo.find_element_by_tag_name("a").get_attribute("href")
            if movieInfo.text.find(movie[1]) >= 0:  # year is correct
                chromeDriver.get(movieLink)
                time.sleep(1)
                rating = chromeDriver.find_element_by_xpath(
                    ".//*[@id='title-overview-widget']/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span")
                directorInfoElements = chromeDriver.find_element_by_xpath(
                    ".//*[@id='title-overview-widget']/div[2]/div[1]").find_element_by_xpath(
                    ".//h4[contains(text(), 'Director')]/..").find_elements_by_tag_name("a")
                directorList = [info.text for info in directorInfoElements]
                movieDirectorCrawled.append(directorList)
                movieRatingCrawled.append(rating.text)
                break
    except Exception:
        movieDirectorCrawled.append(list())
        movieRatingCrawled.append("NA")
chromeDriver.quit()


"""data processing: we may want to do some operation to the crawled data (number add or change format)"""
dataAfterProcess = list()
# there might be multiple directors for each movie and we want to link them with ","
for movieCount in range(len(movieInfoHolder)):
    # movieName + movieYear + movieRating +
    dataProcess = movieInfoHolder[movieCount][0] + "+" + str(movieInfoHolder[movieCount][1]) + "+" + movieRatingCrawled[movieCount] + "+"
    for director in movieDirectorCrawled[movieCount]:
        dataProcess += (director + ",")
    dataAfterProcess.append(dataProcess)  # Name + Year + Rating + director1,director2,


"""write file for data storage"""
writeFileName = "dataCrawl.txt"  # store data to a file named "data.txt" under the same directory
# mode "a+" means append content in the end of the original file content, create file if file not exist
fileToWrite = open(file=writeFileName, encoding="utf-8", mode="a+")
dataToWrite = list()
for data in dataAfterProcess:
    dataToWrite.append(data + "\n")  # \n for start a new line
fileToWrite.writelines(dataToWrite)