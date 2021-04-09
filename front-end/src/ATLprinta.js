import React, { Component } from 'react';
// import Select, { components } from 'react-select';
// import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';

//Γκρινιάζει οτι δεν χρησιμοποιώ το React kai to var jsondata

class ATLprinta extends Component {


    showdata=()=>{
        var testobj=localStorage.getItem('data');
        var jsondata=JSON.parse(testobj)   //Μπορει και να θέλετε με JSON.stringify
        console.log("IS THIS REAL LIFE")
        console.log(jsondata);
        console.log(JSON.stringify(JSON.parse(testobj)))  //όπως εδω 
     }
    render() {
    return (
        <div>
            <h1>The Team:</h1>
            <p>Aristotelis Sibetheros Rules</p>
        </div>
    );
}
}
 export default ATLprinta;