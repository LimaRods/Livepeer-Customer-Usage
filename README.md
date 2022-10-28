# Livepeer-Customer-Usage
 My Take Home for the recruitment process of Livepeer

## 1. Introduction

This is the take-home for the recruitment process of Livepeer. The main purpose of this dashboard is to show my skills in Python, and analytics and answer the following questions 
given the daily customer usage data:

* What are some high-level KPIs that you would recommend?
* Who are our most valuable customers and why?
* What customers have the most future potential and how did you target them?

## 2. Methodologies

### 2.1 KPIs

I used a personal framework to convert stakeholders' needs and statements into metrics. I set up 3  global metrics: Lenght of Transcoded Video per Period,  Length of Video Streamed per Period, and Length of Video Uploaded per Period.

![screenshot](screenshots/voc.png)

It's possible to see the data from multiple angles such as total runnings, accumulated value, percent variation, histogram, and customer rankings.
There are two types of ranking charts: an overall ranking considering all customers and another considering customer who created an account within the last 3 months from the end date of the filter. 

### 2.2 Filters

The filters available are date range, date granularity, and ranking filter. The date range controls all dashboard elements, the date granularity change all charts and the ranking filter only affects the top customer's chart. In this way, it allows us to look at top customers within a date range.	

![screenshot](screenshots/filter.png)

## 3. Data Analysis

You can switch among the metrics using tabs. Each tab view contains 6 charts,  resulting in 18 total charts plus big numbers.

![screenshot](screenshots/dash_img.png)

## 4. Conclusions

* Looking at the histogram for the transcoded duration, we can notice that few daily usages account for most of the total duration, and hence, few customers generate a relevant part of the total revenue from the streaming service.
![screenshot](screenshots/hist.png)

* Between 1st Jan 22 and 21th Oct 22 the top customer when it comes to transcoded duration is **5ef4**. The top new customer is **a0c2** and represents almost 10% of the top 10 customers in terms of duration. We assumed the top new customers as future potentials.
![screenshot](screenshots/top_trans.png)

For Video Uploaded we had **3fcf** and **5b59** as the top customer and top new customers respectively
![screenshot](screenshots/top_video.png)

