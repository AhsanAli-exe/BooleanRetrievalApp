The Boolean Retrieval Model



Link: https://k224036boolean.streamlit.app/



Files:



1 .Preprocessing.ipynb : This notebook contains all the code for Preprocessing the documents.

I have coverted text to lowercase

Removed punctuation marks

Removed numbers

Removed stop words

Applied stemming



2. indexCreation.ipynb:  I have created the inverted index and positional index in this notebook. 

Everything is done manually. I haven't used python libraries like collections etc. I have used traditional dictionary for indexes



3. booleanModel.ipynb: Query validation, model creation and evaluation is in this notebook.

I have validated the query and then created two models

One for handling boolean queries and other for proximity queries. I have used the traditional merge algorithm that was used in course slides.

Nothing fancy was used. 

I have evaluated the queries according to gold query set in the same document

You can see that there is upto 95% resemblance indicating that my code is correctly fetching the relevant docs.



4. searchFunctions.py : it contains the functions to fetch documents in response to boolean queries and proximity queries.



5. myApp.py : it contains the streamlit gui code which is integrated with the main logical code. I have also included a side bar on the website which can be opened to see the rules of inputting queries. 



Note: I have done extensive testing and edge case handling. Error messages are shown when user inputs wrong query.

Just open the link and you can see the working of my model



Thank You 😊

