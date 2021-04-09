# Mobile app
### Steps to build the app:
-  Εγκατάσταση του [Android Studio](https://developer.android.com/studio)
-  Εγκατάσταση του [ngrok](https://ngrok.com/) 

Εκτελούμε το αρχείο ngrok και πληκτρολογούμε την εντολή:
````
ngrok http https://localhost:8765/
````

Στο αρχείο *RequestManager.kt* (path: CGEEnergy\app\src\main\java\com\cge\cgeenergy\managers) τροποποιούμε το baseUrl ώστε να αντικαταστήσουμε το https://localhost:8765/ με το url αντιστοίχισης που βλέπουμε στο παράθυρο ngrok.

Συνδέουμε android κινητό στο οποίο έχουμε ενεργοποιήσει τις επιλογές android development και τρέχουμε την εφαρμογή.
