---
title: "reflection-milestone2"
author: "Baldeep Dhada, Somya Nagar, Eden Chen, Jade Yu"
date: "2024-03-04"
output: pdf_document
---

## Implemented Features:

In our **BnB Beacon** dashboard, we have 2 pages featuring 6 plots and 1 table.

On the first page, users can utilize a dropdown menu to select their desired city and neighborhood for visiting, alongside a slider to set their budget range. The chosen value will then be reflected on a map. Additionally, the page will show the number of listings available and a top 5 hosts table. Users can click on a link to view more detailed information.

On the second page, users can:

1.  Adjust a rating slider to visualize the price distribution based on room types (violin plot)
2.  Select room types checkboxes to observe the average price in different cities (line plot)
3.  Adjust a reviews slider to visualize the average price based on different ratings, with darker points indicating more reviews (scatter plot).
4.  Select room types from a dropdown menu to explore the relationship between reviews and ratings (scatter plot)
5.  Choose room types and cities in a heatmap, which will dynamically update a scatter plot showing the average price vs. minimum nights and a bar plot displaying the number of listings on Airbnb for the selected cities and room types It's important to note that users can hover their mouse over the plots to view additional details

## Features in Development:

We still work on

1.  Changing the line spacing in the `Neighbourhood` drop down menu
2.  Resizing the table, the listings box, and the price slider
3.  Changing the color of the host table
4.  Trying to cache the data to reduce the time processing the image

## Problems

1.  We can't adjust the slider width beyond one hundred percent
2.  We can't move the longitude and latitude out of the hover box without removing these two variables from the code
3.  It's challenging to make all points on the map easy to click on the hover box
4.  It's challenging to change the color of the hover box of the map to match the color of points on the map
