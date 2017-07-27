from flask import render_template


def unwrap(string):
    """
    Take a string with new lines and make one line
    :param string:
    :return: string
    """
    return ' '.join([x.strip() for x in string.split('\n')]).strip()


class ExperimentError(Exception):
    experiment_errors = dict(
        page_not_found=404,
        incorrect_experiment_params=1000,
        biglearn_service_error=1001,
        experiment_completed=1002,
        quit_experiment_early=1003,
        unknown_status=1004,
        algorithm_error=1005,
        database_error=1006,
        phase_completed=1007,
        phase_not_completed=1008,
        unqualified_worker=1009,
    )

    error_descriptions = dict()
    error_descriptions['page_not_found'] = unwrap(
        '''
        The resource you are looking for cannot be found.
        '''
    )

    error_descriptions['incorrect_experiment_params'] = unwrap(
        '''
        Either the HIT id, the assignment id, or the worker id
        were not provided to the start experiment page.
        '''
    )

    error_descriptions['biglearn_service_error'] = unwrap(
        '''
        There was an error with the Biglearn API.
        '''
    )

    error_descriptions['experiment_completed'] = unwrap(
        '''
        The experiment has already been completed by the user.
        '''
    )

    error_descriptions['quit_experiment_early'] = unwrap(
        '''
        The experiment was started and cannot be continued because
        it ended prematurely.
        '''
    )

    error_descriptions['unknown_status'] = unwrap(
        '''
        There was an issue with the status of the experiment that the
        application cannot handle.
        '''
    )

    error_descriptions['database_error'] = unwrap(
        '''
        There was an issue with saving your response to the database. Please contact
        the research team via email at <a href="mailto:labs@openstax.org">labs@openstax.org</a>.
        '''
    )

    error_descriptions['phase_completed'] = unwrap(
        '''
        This phase of the experiment has already been completed. Please contact
        the research team via email at <a href="mailto:labs@openstax.org">labs@openstax.org</a>.
        '''
    )

    error_descriptions['phase_not_completed'] = unwrap(
        '''
        You have not completed the first part of this experiment. Please contact
        the research team via email at <a href="mailto:labs@openstax.org">labs@openstax.org</a>.
        '''
    )
    error_descriptions['unqualified_worker'] = unwrap(
        '''
        You do not have the correct qualification on your Mechanical Turk account. Please contact
        the research team via email at <a href="mailto:labs@openstax.org">labs@openstax.org</a>.
        '''
    )

    def __init__(self, value):
        self.value = value
        self.error_num = self.experiment_errors[self.value]
        self.error_desc = self.error_descriptions[self.value]
        self.template = "error.html"

    def __str__(self):
        return repr(self.value)

    def error_page(self, request, contact_on_error=None):
        return render_template(self.template,
                               error_num=self.error_num,
                               error_desc=self.error_desc,
                               contact_address=contact_on_error,
                               **request.args), 400


class SectionNotFound(Exception):
    pass
