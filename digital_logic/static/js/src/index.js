import $ from "jquery";
import _ from "underscore";
import Experiment from "./experiment";

window.$ = window.jQuery = $;

require('materialize-css/dist/css/materialize.min.css');

let config = {
  subjectId: window.subjectId,
  displayElement: $('.experiment-panel')
};

let experiment = new Experiment(config);
