# EECS486-Ethnicity-Identifier

#### Folder Structure

```shell
.
├── README.md
├── archive
├── data
├── Analysis.ipynb
├── gatherData.ipynb
├── olympic_scrapper.py
├── combMethod.py
├── dataHandler.py
├── ngram.py
├── postertest.py
├── prepostfix.dll
├── prepostfix.so
```

**archive** stores the open-source data sets we used, their links are included below

**data** stores the processed data we used to train the model and our test results.

**Analysis.ipynb gatherData.ipynb** are scripts used to process data

**olympic_scrapper.py** is used to crawl data from Olympics website

**combMethod.py** stores the base class of our model, including code for testing

**dataHandler.py ngrams.py** are used to do preprocessing

**postertest.py** is the code for presentation demo

**prepostfix.dll prepostfix.so** are c++ dynamic link library

#### To Use it

Make sure you have *python3* and *numpy, BeautifulSoup, requests* installed,

To run the demo 

```shell
python3 postertest.py
```

It will take some time to initialize and return the prediction result with confidence score every time entering a (full) name.

 To run the test of the model

```shell
python3 combMethod.py
```

It will generate a csv file with evaluation results. It will take a long time to run, but you can see the result we have generated in *data* folder. There can be some different between your result and ours because of randomness.

To run the scraper 

```shell
python3 olympic_scrapper.py
```

**Note: both nation and region in variable names refer to ethnicity.** 

#### Links

Some relevant repos & datasets:
https://www.kaggle.com/bryanpark/nana-dataset
https://github.com/kaionwong/ethnicity-ml-prediction/tree/master/data
https://github.com/Ahalya24/ethinicity_from_name
https://github.com/d4em0n/nationality-classify/tree/master/datasets

Other data website:
https://www.goratings.org/en/
https://ratings.fide.com/top.phtml?list=men
https://www.worldathletics.org/world-rankings/marathon/men
https://www.mlb.com/fans/top-100-right-now/

