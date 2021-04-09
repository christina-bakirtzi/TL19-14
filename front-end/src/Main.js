import React, { Component } from 'react';
// import Select, { components } from 'react-select';
// import Dropdown from 'react-dropdown';


class Main extends Component {
    // constructor(props){
    //     super(props);
    // }
    showdata=()=>{
       var testobj=localStorage.getItem('data');
       console.log("IS THIS REAL LIFE")
       console.log(JSON.parse(testobj));
       console.log(JSON.stringify(JSON.parse(testobj)))
    }

    render() {
        return (
            <div align="center">
                <h1>Can't GIT Enough</h1>
                <p>Αριστοτέλης Συμπέθερος</p>
                <p>Βίκυ Ξεφτέρη</p>
                <p>Χριστίνα Μπακιρτζή</p>
                <p>Γιάννης Παπαγεωργίου</p>
                <p>Νίκος Φρυγανιώτης</p>


            </div>
        );
    }
    
}

export default Main;