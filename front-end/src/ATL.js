import React, { Component } from 'react';
// import Select, { components } from 'react-select';
// import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';
import { UserContext } from './UserContext';
import './ATL.css';

class ATL extends Component {
    static contextType = UserContext;


    constructor(props){
        super(props);
        this.state={date:"date",
                    dateinput:"2018-01-01",
                    tabletype:"ActualTotalLoad",
                    prodtype:"AllTypes"};
    }

        show=()=> {
        var validation=true;
        let tabletype = this.tabletype.value;
        let country=this.country.value;
        let resolution = this.resolution.value;
        let date = this.date.value;
        let productiontype;
        if(this.state.prodtype!=null){
            productiontype =this.state.prodtype;
            console.log(productiontype);
        }
        let dateinput=this.state.dateinput;
        var arr= dateinput.split('-');
        var year=undefined,month=undefined,day=undefined;
        if(arr.length==3){
         year=arr[2];
         month=arr[1];
         day=arr[0];
         dateinput=year+'-'+month+'-'+day;
        } else if(arr.length==2){
         year=arr[1];
         month=arr[0];
         dateinput=year+'-'+month;
        } else if(arr.length==1){
         year=arr[0];
         dateinput=year;
        }
        console.log(month);
        console.log(day);
        console.log(year);
        this.setState({validation:true});
        if (day>31 || day<1 || month>12 || month<1 || year>2020 || year <1990 ){
            validation=false;
            alert("Invalid date given");
        }
        else if (day!==undefined && (date==='month' || date==='year')){
            validation=false;
            alert("Invalid date given ");
        }
        else if (month!==undefined &&  date==='year'){
            validation=false;
            alert("Invalid date given");
        }
        else if (date==='date' && (day===undefined || month===undefined || year===undefined)){
            validation=false;
            alert("Invalid date given");
        }
        else if (date==='month' && (month===undefined || year===undefined)){
            validation=false;
            alert("Invalid date given");
        }
        else if (date==='year' && (year===undefined)){
            validation=false;
            alert("Invalid date given");
        }
        console.log(dateinput);
        var url='https://b16d8614.ngrok.io//energy/api/'+this.state.tabletype+'/'+country+"/"+resolution+'/'+date+'/'+dateinput;
        if(tabletype==='AggregatedGenerationPerType'&& productiontype!==null){
            url='https://b16d8614.ngrok.io//energy/api/AggregatedGenerationPerType/'+country+'/'+productiontype+'/'+resolution+'/'+date+'/'+dateinput;
        }
        console.log(url);
        if(validation===true){
            fetch(url,{
                method: 'GET',
                headers: {
                    'X-OBSERVATORY-AUTH':this.context.token,
                },
            }).then((response) =>{console.log(response.status);
                if(response.status===401){
                    response.text().then(resp => alert(resp));
                    this.props.history.push('/Logout');
                }else if(response.status===402){
                    response.text().then(resp => alert(resp));
                }else if(response.status===403){
                    response.text().then(resp => alert(resp));
                }else if(response.status===400){
                    response.text().then(resp => alert(resp));
                }
                else{
                    response.text().then(json=>{
                    localStorage.setItem('data',json)
                    if(tabletype==='ActualTotalLoad' && date==='date'){
                        this.props.history.push('/ATLchart_date');}
                    else if(tabletype==='ActualTotalLoad' && date==='month'){
                        this.props.history.push('/ATLchart_month');}
                    else if(tabletype==='ActualTotalLoad' && date==='year'){
                        this.props.history.push('/ATLchart_year');}
                    else if(tabletype==='AggregatedGenerationPerType' && date==='date'){
                        this.props.history.push('/AggregatedDate');}
                    else if(tabletype==='AggregatedGenerationPerType' && date==='month'){
                        this.props.history.push('/AggregatedMonth');}
                    else if(tabletype==='AggregatedGenerationPerType' && date==='year'){
                        this.props.history.push('/AggregatedYear');}
                    else if(tabletype==='DayAheadTotalLoadForecast' && date==='date'){
                        this.props.history.push('/DayAheadchart_date');}
                    else if(tabletype==='DayAheadTotalLoadForecast' && date==='month'){
                        this.props.history.push('/DayAheadchart_month');}
                    else if(tabletype==='DayAheadTotalLoadForecast' && date==='year'){
                        this.props.history.push('/DayAheadchart_year');}
                    else if(tabletype==='ActualvsForecast' && date==='date'){
                        this.props.history.push('/ATLvsForecastchart_date');}
                    else if(tabletype==='ActualvsForecast' && date==='month'){
                        this.props.history.push('/ATLvsForecastchart_month');}
                    else if(tabletype==='ActualvsForecast' && date==='year'){
                        this.props.history.push('/ATLvsForecastchart_year');}})
                }})
        }
    }

    handledateChange=(event)=>{
        this.setState({date:event.target.value});
    }
    
    handledateChangedateinput=(event)=>{
        this.setState({dateinput:event.target.value});

        // document.getElementById(event.target.value).show().siblings().hide();
    }
    handledateChangetabletype=(event)=>{
        this.setState({tabletype:event.target.value});
    }

    handleChangeprodtype=(event)=>{
        console.log("IN HERE")
        console.log(event.target.value)
        this.setState({prodtype:event.target.value});
    }

    
    render() {
        return (
            <React.Fragment>
			<div align="center">
                <label>
                    Δεδομένα:
					<br></br>
                <select id = "dropdown1" ref = {(input)=> this.tabletype = input} required  onChange={this.handledateChangetabletype}>
                    <option value="ActualTotalLoad">ActualTotalLoad</option>
                    <option value="AggregatedGenerationPerType">AggregatedGenerationPerType</option>
                    <option value="DayAheadTotalLoadForecast">DayAheadTotalLoadForecast</option>
                    <option value="ActualvsForecast">ActualTotalLoadvsDayAheadTotalLoadForecast</option>
                </select>
				<br></br>
                {this.state.tabletype==='AggregatedGenerationPerType' && <label>
                        Τύπος Παραγωγής: <br></br>
                    <select id = "dropdownextra" ref = {(input)=> this.prodtype = input} required onChange={this.handleChangeprodtype}>
                        <option value="AllTypes">AllTypes</option>
                        <option value="AC Link">AC Link</option>
                        <option value="Biomass">Biomass</option>
                        <option value="DC Link">DC Link</option>
                        <option value="Fossil Brown coal/Lignite">Fossil Brown coal/Lignite</option>
                        <option value="Fossil Coal-derived gas">Fossil Coal-derived gas</option>
                        <option value="Fossil Gas">Fossil Gas</option>
                        <option value="Fossil Hard coal">Fossil Hard coal</option>
                        <option value="Fossil Oil">Fossil Oil</option>
                        <option value="Fossil Oil shale">Fossil Oil shale</option>
                        <option value="Fossil Peat">Fossil Peat</option>
                        <option value="Geothermal">Geothermal</option>
                        <option value="Hydro Pumped Storage">Hydro Pumped Storage</option>
                        <option value="Hydro Run-of-river and poundage">Hydro Run-of-river and poundage</option>
                        <option value="Hydro Water Reservoir">Hydro Water Reservoir</option>
                        <option value="Marine">Marine</option>
                        <option value="Nuclear">Nuclear</option>
                        <option value="Other">Other</option>
                        <option value="Other renewable">Other renewable</option>
                        <option value="Solar">Solar</option>
                        <option value="Substation">Substation</option>
                        <option value="Transformer">Transformer</option>
                        <option value="Waste">Waste</option>
                        <option value="Wind Offshore">Wind Offshore</option>
                        <option value="Wind Onshore">Wind Onshore</option>
                    </select>
                    </label>}
                
                </label> 
				<br></br>

                <label>
                    Χώρα:
					<br></br>
                    <input id="country" name="country" type="text"  ref = {(input)=> this.country = input} required />
                </label> 
				<br></br>

                <label>
                    Χρόνος εξέτασης:
					<br></br>
                <select id = "dropdown3" ref = {(input)=> this.resolution = input} required>
                    <option value="PT15M">PT15M</option>
                    <option value="PT30M">PT30M</option>
                    <option value="PT60M">PT60M</option>
                </select>
                </label>
				<br></br>

                <label>
                    Ανά : 
				
				<br></br>
                    <select id = "dropdown2" ref = {(input)=> this.date = input}  required onChange={this.handledateChange}>
				

                    {/* <select table={this.state.table} onChange={this.handleChange}> */}
                    <option value="date">Ημέρα</option>
                    <option value="month">Μήνα</option>
                    <option value="year">Χρόνο</option>
                    </select>
				<br></br>

                </label>
				<br></br>
                {this.state.date==='date' &&  <input id="date" name="date" type="text" placeholder="DD-MM-YYYY" value={this.state.email} onChange={this.handledateChangedateinput}  />}
                {this.state.date==='month' &&  <input id="date" name="date" type="text" placeholder="MM-YYYY" value={this.state.email} onChange={this.handledateChangedateinput}  />}
                {this.state.date==='year' &&  <input id="date" name="date" type="text" placeholder="YYYY" value={this.state.email} onChange={this.handledateChangedateinput}  />}

				<br></br>
                <form onSubmit={this.show}>
					<br></br>

                    <button class="btn btn-info" type="submit" >
                        Υποβολή 
                    </button>
                </form>
				</div> 
            </React.Fragment>

        );
    }
    
}

export default ATL;
