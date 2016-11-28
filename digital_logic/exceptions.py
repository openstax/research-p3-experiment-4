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
        unknown_status=1004
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