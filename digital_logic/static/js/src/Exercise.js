import $ from 'jquery';
import _ from 'underscore';
import API from './api';

let ExercisePhase = {
  start(sectionName, subjectId, assignmentId) {
    console.log('Starting the Exercise phase');
    this.sectionName = sectionName;
    this.subjectId = subjectId;
    this.assignmentId = assignmentId;

    this.state = {
      totalExercises: 4,
      currentExercise: '',
      count: 0
    };

    this.totalExercises = 4;

    this.API = new API();

    this.$readingSection = $('.reading-wrapper');
    this.$loadingBar = $('.progress');
    this.$exerciseSection = $('.exercise-wrapper');
    this.$eText = $('.exercise-text');
    this.$eAnswer = $('.exercise-answer');
    this.$currentExerciseCount = $('.current-exercise-counter');
    this.$exerciseTotal = $('.total-exercises');
    this.$exerciseForm = $('.exercise-form');

    this.$readingSection.hide();
    // this.$loadingBar.show();
    // this.$exerciseSection.show();

    this.getNextExercise = this.getNextExercise.bind(this);

    this.getNextExercise()

  },

  exerciseLoading() {
    this.$readingSection.hide();
    this.$loadingBar.show()
  },

  exerciseLoaded() {
    this.$loadingBar.hide();
    this.$exerciseSection.show()

  },

  updateExerciseCounter() {
    this.$currentExerciseCount.empty();
    this.$exerciseTotal.empty();
    this.$currentExerciseCount.html(this.state.count + 1);
    this.$exerciseTotal.html(this.state.totalExercises)
  },

  loadExercise(exercise) {

    this.updateExerciseCounter();

    console.log('loading exercise...');

    this.$eText.empty();
    this.$eAnswer.empty();

    this.$eText.html(exercise['text']);
    this.loadChoices(exercise['choices']);
    this.exerciseDelayLoad()

  },

  loadChoices(choices) {
    console.log(choices);
    let $inputField = $('<div></div>');
    let $optionsList = $('<ul></ul>')
      .addClass('input-field');
      // .addClass('col s12');


    _.forEach(choices, function(choice, index) {
      let $listItem = $('<li></li>');
      let $label = $('<label>' + choice.markup + '</label>').attr('for', 'choice-' + index);

      let $option = $('<input type="radio" value='+ index + '>');
      $option.attr('name', 'choice').attr('id', 'choice-' + index);

      $listItem.append($option);
      $listItem.append($label);

      $optionsList.append($listItem);
      //<input id="skill_level-0" name="skill_level" type="radio" value="Zero">*/}
      console.log(choice)
    });

    $inputField.append($optionsList);
    this.$exerciseForm.append($inputField)

  },

  getNextExercise() {
    let self = this;
    console.log('Retrieving the next exercise from the API');
    this.exerciseLoading();
    let exercise = this.API.getNextExercise(this.subjectId, this.sectionName, this.assignmentId)
      .done(function (response) {
        console.log(response);
        self.currentExerciseId = response['id'];
        self.loadExercise(response);
        self.state.count += 1
      })
  },

  handleSubmit(event) {
    event.preventDefault();

    console.log('handling submit')
  },

  exerciseDelayLoad() {
    setTimeout(_.bind(this.exerciseLoaded, this), 1000)
  },

};

window.ExercisePhase = ExercisePhase;
