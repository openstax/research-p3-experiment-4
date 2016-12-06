import Backbone from 'backbone';
import _ from 'underscore';
import $ from 'jquery';

import randString from './utils'

Backbone.$ = $;


let Subject = Backbone.Model.extend({
  urlRoot: '/api/v1/subjects',

  blacklist: ['data_string',],

  toJSON: function(options) {
    return _.omit(this.attributes, this.blacklist);
  },

  setStatus: function(status) {
    this.set('status', status);
    console.log('Updating status: ' + status + ' on subject: #' + this.get('id'));
    this.save();
  },

  getExternalId: function() {
    return this.get('external_id');
  },

  getExperimentGroup: function() {
    return this.get('experiment_group')
  },

  assignCompletionCode: function() {
    let completionCode = randString(6);
    this.set('completion_code', completionCode);
    console.log('Creating completion code: ' + completionCode + ' on user: #' + this.get('id'))
    this.save();
    return this.get('completion_code')
  },

  getCompletionCode: function() {
    return this.get('completion_code')
  }


});




let ExperimentData = Backbone.Model.extend({
  urlRoot: '/api/v1/subjects/data',

  defaults: {
    assignment_id: 0,
    worker_id: 0,
    hit_id: 0,
    sessionData: [],
    questionData: [],
    formData: [],
    eventData: [],
    userAgent: ""
  },

  initialize: function() {
    this.userAgent = navigator.userAgent;
  },

  addQuestionData: function(questionData) {
    let data = this.get(questionData);
    data.push(questionData);
    this.set('questionData', data)
  },

  addSessionData: function(session, action) {
    let sessionData = {
      'session': session,
      'dateTime': (new Date().getTime()),
      'action': action ? action : ''
    };
    let data = this.get('sessionData');
    data.push(sessionData);
    this.set('sessionData', data);
  },

  addFormData: function(formName, responses) {
    let formData = {
      'formName': formName,
      'dateTime': (new Date().getTime()),
      'responses': responses
    };
    let data = this.get('formData');
    data.push(formData);
    this.set('formData', data)
  }
});



export {ExperimentData, Subject}
