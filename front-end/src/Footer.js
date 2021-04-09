import React, { Component } from 'react';


class Footer extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            modalVisible: false,
            modalType: null
        };
        
        this.showModal = this.showModal.bind(this);
        this.hideModal = this.hideModal.bind(this);
    }
    
    showModal() {
        console.log('show modal');
        this.setState({modalVisible:true});
    }

    hideModal(userChoice) {
        //handle user choice
        console.log(userChoice);
        this.setState({modalVisible:false});
    }
            
    render() {
           
        return (
                 <footer>
                  <p>Δημιουργήθηκε απο: Can't git enough</p>
                  <p>Στοιχεία επικοινωνίας: <a href="mailto:someone@example.com">
                  cantgitenough@gmail.com</a>.</p>
                </footer>
        );
    }
    
}

export default Footer;
