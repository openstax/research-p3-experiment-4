import $ from 'jquery';
import API from './api';

let ExercisePhase = {
  start(sectionName, subjectId, assignmentId) {
    console.log('Starting the Exercise phase');
    this.sectionName = sectionName;
    this.subjectId = subjectId;
    this.assignmentId = assignmentId

    this.totalExercises = 4;

    this.API = new API();

    this.$readingSection = $('.reading-wrapper');
    this.$loadingBar = $('.progress');
    this.$exerciseSection = $('.exercise-wrapper');

    this.$readingSection.hide();
    this.$loadingBar.show();
    this.$exerciseSection.show();

    this.getNextExercise = this.getNextExercise.bind(this);

    this.getNextExercise()

  },

  loadExercise() {

  },

  getNextExercise() {
    console.log('Retrieving the next exercise from the API');

    let exercise = this.API.getNextExercise(this.subjectId, this.sectionName, this.assignmentId)
      .done(function(response) {
        console.log(response);

        this.currentExerciseId = response['id'];
    })
  }

};

window.ExercisePhase = ExercisePhase;
