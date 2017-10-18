# hawaiireadings

This repository collects the following code pertaining to an analysis of temperature and precipitation readings in Hawaii.

1. Code to create cleaned up CSVS consisting of data with all NaN values removed. The reason why I removed the NaNs rather than substituted values is that I have no idea what the NaN values were originally supposed to be, therefore I decided not to make an assumption.

2. Code that converted the cleaned CSVS into a dataframe, added ISODates and then uploaded them to a database using the SQLAlchemy ORM.

3. A jupyter notebook that consisted of many analysis of this data. Including:
    A. Measurement of TOBS readings from one station over the course of the year charted in a histogram.
    B. Measurement of Precipitation readings over the past year.
    C. Measurement of the average temperatures, max temperatures, and minimum temperatures over a specified date.

4. A Flask app that created a RESTFUL API through which a user could make several calls to access said data. 
