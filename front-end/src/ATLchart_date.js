import React, { Component } from 'react';
// import Select, { components } from 'react-select';
// import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';
import {Bar} from 'react-chartjs-2';
//Γκρινιάζει οτι δεν χρησιμοποιώ το React kai to var jsondata

// function getJson_forecasted(arr){
//     var c=[];
//     for (var i = 0; i < arr.length; i++){
//        c.push(arr[i].DayAheadTotalLoadForecastValue);
//   }return c;}

function getJson_actual(arr){
    var p=[];
    for (var i = 0; i < arr.length; i++){
      p.push(arr[i].ActualTotalLoadValue);
  }return p;}

function getJson_date(arr){
    var d=[];
    for (var i = 0; i < arr.length; i++){
      d.push(arr[i].DateTimeUTC);
      console.log(arr[i].DateTimeUTC)
  }return d;}

function clrs1(arr){
    var color=[];
    for (var i=0; i< arr.length; i++){
        color.push('rgba(255, 99, 132, 0.6)')
    }return color;
}
function getJson_country(arr){
    var country=arr[0].AreaName
    return country;
}
function getJson_mapcode(arr){
    var map=arr[0].MapCode
    return map;
}
function getJson_day(arr){
    var da=arr[0].Day
    return da;
}
function getJson_year(arr){
    var y=arr[0].Year
    return y;
}
function getJson_month(arr){
    var m=arr[0].Month
    return m;
}
class ATLchart_date extends Component {    constructor(props){
    super(props);
    this.state = {
        chartData: {
            labels:getJson_date(this.showdata()),
            datasets:[
                {
                    label:'Πραγματικό Φορτίο (MWh)',
                    data:getJson_actual(this.showdata()),
                    backgroundColor:clrs1(this.showdata())
            //     },
            //     {
            //       label:'2 Population',
            //       data:getJson_forecasted(this.showdata()),
            //       backgroundColor:[
            //           'rgba(54, 162, 235, 0.6)',
            //           'rgba(54, 162, 235, 0.6)',
            //           'rgba(54, 162, 235, 0.6)'
            //       ]
            //   }
                }]
        },
        country: getJson_country(this.showdata()),
        mapcode: getJson_mapcode(this.showdata()),
        day: getJson_day(this.showdata()),
        month: getJson_month(this.showdata()),
        year: getJson_year(this.showdata())
    }
}
showdata=()=>{
        var testobj=localStorage.getItem('data');
        var jsondata=JSON.parse(testobj);   //Μπορει και να θέλετε με JSON.stringify
        console.log("IS THIS REAL LIFE")
        console.log(jsondata);
        console.log(JSON.stringify(JSON.parse(testobj)))  //όπως εδω
        return JSON.parse(testobj);
        }
static defaultProps = {
    displayTitle:true,
    displayLegend:true,
    legendPosition:'right',
}

    render() {
        return (
            <div className="chart">
            <Bar
                data={this.state.chartData}
                width={100}
                height={50}
                options={{
                    responsive:true,
                    title:{
                        display:this.props.displayTitle,
                        text: 'Actual Total Load in '+this.state.country+' ('+this.state.mapcode+') on '+this.state.day+'/'+this.state.month+'/'+this.state.year,
                        fontSize:25
                    },
                    legend:{
                        display:this.props.displayLegend,
                        position: this.props.legendPosition
                    }
                }}
                />
            </div>
        );
    }
}

 export default ATLchart_date;