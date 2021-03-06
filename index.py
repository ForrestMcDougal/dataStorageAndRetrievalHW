index = '''
<html lang="en-us">
    <head>
        <title>Climate App</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <h1>Welcome to the Hawaii Climate App</br></h1>
        <img src="/Users/RunforrrestruN/Desktop/dataStorageAndRetrievalHW/images/surfs-up.jpeg" alt="surfer riding a wave">
        <h2>Available Routes:</br></h2>
        <div>
            <a href="http://127.0.0.1:5000/api/v1.0/precipitation">Precipitation by date</a> /api/v1.0/precipitation
        </div>
        <div>
            <a href="http://127.0.0.1:5000/api/v1.0/stations">List of all stations</a> /api/v1.0/stations
        </div>
        <div>
            <a href="http://127.0.0.1:5000/api/v1.0/tobs">Temperature observations for the past year</a> /api/v1.0/tobs
        </div>
        <div>
            If you want to find the minimun, average and maximum temperatures for a given range, you can use the endpoints /api/v1.0/(start) or /api/v1.0/(start)/(end) with format YYYY-MM-DD.
        </div>
    </body>
</html>'''