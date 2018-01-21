

// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });
'use strict';

process.env.DEBUG = 'actions-on-google:*';
const App = require('actions-on-google').DialogflowApp;
const functions = require('firebase-functions');


// a. the action name from the make_name Dialogflow intent

const NAME_ACTION = 'workout';
// b. the parameters that are parsed from the make_name intent 
const ANY_ARGUMENT = 'any';
const NUMBER_ARGUMENT = 'number';


exports.rehab = functions.https.onRequest((request, response) => {
  const app = new App({request, response});
  console.log('Request headers: ' + JSON.stringify(request.headers));
  console.log('Request body: ' + JSON.stringify(request.body));


// c. The function that generates the silly name
  function workout (app) {
    let any = app.getArgument(ANY_ARGUMENT);
    let number = app.getArgument(NUMBER_ARGUMENT);
    
   
      app.tell('Alright, let\'s do ' +
        number + ' reps with ' + any +
        '! Start! ');
    
      console.log("bye\n");


  }
  // d. build an action map, which maps intent names to functions
  let actionMap = new Map();
  actionMap.set(NAME_ACTION, workout);


app.handleRequest(actionMap);
});