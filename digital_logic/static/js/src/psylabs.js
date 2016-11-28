import {Subject, ExperimentData} from './models';


class psyLabs {
  constructor(options) {
    this.subjectId = options.subjectId;

    this.subject = new Subject({id: this.subjectId});
    this.experimentData = new ExperimentData({id: this.subjectId});

    this.subject.fetch();
    this.experimentData.fetch();

    console.log('psyLabs Initialized!');

  }

  recordFormData(formName, responses) {
    return this.experimentData.addFormData(formName, responses)
  }

  recordSessionData(sessionData, action) {
    return this.experimentData.addSessionData(sessionData, action)
  }

  recordQuestionData(questionData, meta) {
    if (meta) {
      questionData['meta'] = meta
    }

    // record data to the backend
    return this.experimentData.addQuestionData(questionData)
  }

  saveData() {
    return this.experimentData.save()
  }

}

export default psyLabs
