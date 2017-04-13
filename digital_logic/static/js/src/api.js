class API {
  constructor() {
    this.rootUrl = '/api/v1/'
  }

  getNextExercise(subjectId, sectionName, assignmentId) {
    const resource = 'exercises/next';
    let response = $.ajax({
      type: 'GET',
      dataType: 'json',
      url: this.rootUrl + resource,
      data: {
        subject_id: subjectId,
        section_name: sectionName,
        assignment_id: assignmentId
      }
    });

    return response
  }
}

export default API
