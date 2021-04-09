import React, { Component } from 'react';
import { UserContext } from './UserContext';
import https from 'https'
export class Login extends Component {        
    
    static contextType = UserContext;
    
    constructor(props) {
        super(props);
        this.username = React.createRef();
        this.password = React.createRef();
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    
    handleSubmit(event) {
        console.log('ref to username: ', this.username.current);
        
        const u = this.username.current.value;
        const p = this.password.current.value;
        console.log('Submitting...', u, p);
        const agent=new https.Agent({rejectUnauthorized:true})
        fetch('https://b16d8614.ngrok.io/energy/api/Login',{
            method: 'POST',
            headers: {
                'Content-Type':'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                "username": u,
                "password": p
            }),agent
        }).then((response) => response.json())
        .then(json => {   

            console.log(json);

            //store the user's data in local storage
            //to make them available for the next
            //user's visit
            localStorage.setItem('token', json.token);
            localStorage.setItem('username', u);

            //use the setUserData function available
            //through the UserContext
            this.context.setUserData(json.token, u);
            
            //use the history prop available through
            //the Route to programmatically navigate
            //to another route            
            this.props.history.push('/main');
        }).catch( function(error) {alert("Non valid username or password");});
        
        event.preventDefault();
    }
    
    render() {        
        return (                                    
            <form onSubmit={this.handleSubmit}>

                <label htmlFor="username">Όνομα χρήστη: </label>
                <input id="username" type="text" ref={this.username} required/>
				<br></br>
                <label htmlFor="password">Κωδικός Πρόσβασης: </label>
                <input id="password" type="password" ref={this.password}  required/>
				<br></br>

                <button class="btn btn-success" align="center" type="submit">
                    Σύνδεση
                </button>
            </form>
        );        
    }    
}
export class Logout extends Component {
    
    static contextType = UserContext;
    
    doLogout() {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
                    
        this.context.setUserData(null, null);
        
        this.props.history.push('/');
    }
    
    componentDidMount() {
        //perform an ajax call to logout
        //and then clean up local storage and
        //context state.
        console.log('TEST')
        console.log(this.context.token)

        fetch('https://b16d8614.ngrok.io/energy/api/Logout',{
            method: 'POST',
            headers: {
                'X-OBSERVATORY-AUTH': this.context.token,
                'Content-Type':'application/x-www-form-urlencoded',
            }
        }).then(() => this.doLogout());
    }
    
    render() {
        return (<h2>Loggin out...</h2>);
    }
}