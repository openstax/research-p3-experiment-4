import React from 'react';
import {$c} from '../utils';

const skillLevels = [
  {label: 'Zero', value: 'Zero'},
  {label: 'A Little', value: 'A Little'},
  {label: 'Some', value: 'Some'},
  {label: 'A lot', value: 'A lot'},
];

const english = [
  {label: 'Yes. English is my first language', value: 'Yes'},
  {label: 'No. English is NOT my first language', value: 'No'}
];

const education = [
  {label: 'Choose your option', value: ''},
  {label: 'Grammar School, High School or equivalent', value: 'School'},
  {label: 'Vocational/Technical School (2 year)', value: 'Vocational'},
  {label: 'College Graduate (4 year)', value: 'College'},
  {label: 'Master\'s Degree (MS)', value: 'Masters'},
  {label: 'Doctoral Degree (PhD)', value: 'Doctoral'},
  {label: 'Professional Degrees (MD, JD, etc.)', value: 'Professional'}
];

class DemographicForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      skill_level: '',
      english: '',
      age: '',
      education: '',
      errors: []};
    // Not sure if this is necessary but i see other projects doing this
    // also the React docs.
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.renderTextInput = this.renderTextInput.bind(this);
    this.renderField = this.renderField.bind(this);
    this.renderRadial = this.renderRadial.bind(this);
  }

  handleChange(e) {
    // The handleChange call back placed on forms. Will grab the name and value
    // of the target and add a state value for it
    let obj = {};
    obj[e.target.name] = e.target.value;
    this.setState(obj);
  }

  handleSubmit(event) {
    event.preventDefault();

    if (this.isValid() == true) {
      console.log('Form Validates');
      let data = this.getFormData();
      console.log(data);

      // Save the data with psyLabs prop
      this.props.psylabs.recordFormData('DemographyForm', data);
      this.props.psylabs.saveData();

      // Increment the timeline
      this.props.next();

    } else {
      // TODO: Add a message for why the form did not validate.
      console.log('Form does not validate')
    }
  }

  getFormData () {
    let data = this.state;
    delete data['errors'];
    return data
  }

  // Validate the form inputs
  isValid() {
    let validation = {};
    validation['errors'] = [];

    //Check and see if any of the fields are blank
    for (var key in this.state ) {
      let value = this.state[key];
      if (!value) {
        validation.errors.push(key);
      }
    }

    this.setState(validation);

    let valid = true;

    if (validation.errors.length > 0) {
      valid = false;
    }

    return valid;

  }

  // Create the ages used for the age selection field
  createAgeOptions() {
    let ages = [{label: 'Choose your option', value: "", key: 0}];
    let min = 10,
        max = 110;
    for (var i = min; i< max; i++) {
      ages.push({label: i, value: i, key: i})
    }
    return ages
  }
  // Render a select field
  renderSelect(id, label, values) {
    let self = this;
    let options = values.map(function(value) {
      return <option value={value.value}>{value.label}</option>
    });
    return this.renderField(id, label,
    <select className="form-control browser-default" name={id} id={id} ref={id} onChange={this.handleChange}>
      {options}
    </select>
      )
  }

  // Render Radio buttons
  renderRadial(id, label, values) {
    let self = this;
    let radials = values.map(function(value) {
      return (
        <div>
          <input type="radio" ref={id + value.value} id={id + value.value} name={id} value={value.value} onChange={self.handleChange}/>
          <label htmlFor={id + value.value}>{value.label}</label>
        </div>
      )
    });
    return this.renderField(id, label, radials)
  }

  // Render Text Input
  renderTextInput(id, label, info) {
    return this.renderField(id, label,
    <input type="text" className="form-control" id={id} name={id} ref={id} placeholder={info} onChange={this.handleChange}/>)
  }

  renderField(id, label, field) {
    return(
      <li className={$c('question ' + id, {'has-error': id in this.state.errors})}>
        <div className="form-group">
          <div className="form-label">
            {label}
          </div>
          <div>
            {field}
          </div>
        </div>
      </li>
    )
  }

  render() {
    return (
      <div>
        <h5>We'd like to know a little bit about you before you begin the study</h5>
        <form onSubmit={this.handleSubmit} name="demographyForm">
          <ol style={{listStyle: 'none'}}>
            {this.renderRadial('skill_level', 'What is your experience level in digital logic?', skillLevels)}
            {this.renderRadial('english', 'Is English your first language', english)}
            {this.renderSelect('age', 'What is your age', this.createAgeOptions())}
            {this.renderTextInput('gender', 'What is your gender?', 'Type in your gender')}
            {this.renderSelect('education', 'Indicate the highest level of education completed', education )}
            <li className="question submit">
              <button type="submit" className="btn"> Submit and begin</button>
            </li>

          </ol>
        </form>
      </div>
    )
  }
}


export default DemographicForm
