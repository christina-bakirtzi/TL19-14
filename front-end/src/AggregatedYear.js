import React, { Component } from 'react';
import 'react-dropdown/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import './Aggregated.css';
// import App from './App';
// import UserConfirmationModal from './UserConfirmationModal';
function getJson_country(arr){
    var country=arr[0].AreaName
    return country;
}
function getJson_mapcode(arr){
    var map=arr[0].MapCode
    return map;
}
function getJson_year(arr){
    var y=arr[0].Year
    return y;
}
class AggregatedYear extends Component {
	constructor(props) {
    super(props)
    this.state = {
      json: [],
	  country: getJson_country(this.showdata()),
	  mapcode: getJson_mapcode(this.showdata()),
      year: getJson_year(this.showdata())
    }
  }

  componentDidMount() {
    this.setState((prevState) => {
      return {
        json: this.showdata()
      }
    })
  }

    showdata=()=>{
        var testobj=localStorage.getItem('data');
        var jsondata=JSON.parse(testobj)   //Μπορει και να θέλετε με JSON.stringify
        console.log("IS THIS REAL LIFE")
        console.log(jsondata);
        console.log(JSON.stringify(JSON.parse(testobj)))  //όπως εδω
		return JSON.parse(testobj);
     }
    render() {
		return (
		  <div >
		  <h1 id='title'>Aggregated Generation Values in {this.state.country} ({this.state.mapcode}) on {this.state.year}</h1>
			<table>
			  <thead  align="center">
				<th>MONTH</th>
				<th>PRODUCTION TYPE</th>
				<th>AGGREGATED GENERATION VALUE</th>
			  </thead>
			  <tbody>
				{this.state.json.map((data, i) => {
				  return (
					<tr key={i}>
					  <td align="center">{data.Month}</td>
					  <td align="center">{data.ProductionType}</td>
					  <td align="center">{data.ActualGenerationOutputByMonthValue}</td>
					</tr>
				  )
				})}
			  </tbody>
			</table>
		  </div>
		);
	}
}
 export default AggregatedYear;