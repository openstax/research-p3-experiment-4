import $ from "jquery";
import Experiment from "./experiment";

window.$ = window.jQuery = $;

require('materialize-css/dist/css/materialize.min.css');

let config = {
  subjectId: window.subjectId,
  displayElement: $('#experiment-panel')
};

let experiment = new Experiment(config);

experiment.start();
