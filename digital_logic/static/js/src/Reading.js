import _ from 'lodash';
import $ from 'jquery';

const preface = {name: 'preface', questions: false};
const introduction = {name: 'introduction', questions: false};
const boolean_variables = {name: 'boolean-variables', questions: false};
const logic_gates = {name: 'logic-gates', questions: true};
const truth_tables = {name: 'truth-tables', questions: true};
const compound_boolean = {name: 'compound-boolean-expression', questions: true};
const circuits_to_truth = {name: 'circuits-to-truth-tables', questions: true};
const tt_to_boolean = {name: 'truth-tables-to-boolean', questions: true};
const summary = {name: 'summary', questions: false};

const sections = [
  preface,
  introduction,
  boolean_variables,
  logic_gates,
  truth_tables,
  compound_boolean,
  circuits_to_truth,
  tt_to_boolean,
  summary
];

class ReadingPlayer {
  constructor() {
    this.textbook = [];
    this.preloadTextbook();
  };

  preloadTextbook() {
    _.each({
      sections, function(section) {
        $.ajax({
          url: '/api/v1/textbook/' + section.name,
          success: function (data) {
            section['text'] = data.html;
            this.textbook.push(section)
          }
        })
      }
    })
  }
}

export default ReadingPlayer
