// Experiment brings together the different phases of the experiment and acts
// as a controller for "playing" the experiment.

// The main parts of the experiment are:
// Timeline - runs the  phases of the experiment in order.
// The timeline contains all the components of the experiment. In this case,
// 1. Demography data
// 2. Reading / Practice exercise portion
// 3. Assessment
// 4. Summary

import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';

import psyLabs from './psylabs';

import DemographicForm from './components/demographicInfoForm'

class Experiment {
  constructor(config) {

    this.config = {};

    let defaults = {
      'displayElement': undefined,
    };

    // get all items from config and assign
    Object.assign(this.config, defaults, config);

    this.psylabs = new psyLabs({subjectId: this.config.subjectId});

    // Check if the subjectId was provided. Without it we can't get the data
    // from the API.
    if (typeof this.config.subjectId == 'undefined') {
      throw new Error('A subjectId is not defined for the experiment')
    }
    else {
      console.log('The subjectId for this experiment is: ' + this.config.subjectId)
    }

    // Check if a displayElement was defined
    if (typeof this.config.displayElement == 'undefined') {
      throw new Error('A displayElement was not defined for this experiment')
    }
    else {
      this.config.displayElement.append('<div class="experiment-content-wrapper">' +
        '<div id="experiment-content"></div></div>');
      this.domTarget = document.getElementById('experiment-content')
    }

  }
  // Tells the timeline to start at its first phase.
  start() {

    // Loads the Demography Form
    // var form = React.createElement(DemographicForm, {psylabs: this.psylabs, next: this.next});
    // ReactDOM.render(form, this.domTarget)

    // Next we need to load the Reading portion of the experiment
    // The reading portion contains a reading of the digital logic material.
    // A section is presented for the subject to read.
    // They are then asked a series of questions related to the section.

  }

  next() {
    console.log('moved to next')
  }
}

export default Experiment
