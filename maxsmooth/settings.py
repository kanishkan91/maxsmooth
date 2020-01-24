
"""
The Settings class is used to define options that are passed to maxsmooth.
It should be called by the user before the function ``smooth`` by,

.. code:: bash

    from maxsmooth.settings import setting
    setting = setting()

and changes to the settings can be made before a call to ``smooth``
like so,

.. code:: bash

    setting.model_type = 'polynomial'
"""

class setting(object):
    r"""
    **Attributes**

    **fit_type:** (Default=='qp-sign_flipping')

    The type of fitting routine used to fit the model. There are two options
    designed to explore the sign space of the function.

    *Accepted options:*

    'qp' - Quadratic programming testing every combination of sign
        on the derivatives. This is a quick process provided the
        order of the polynomial is small.

    'qp-sign_flipping' - Quadratic Programming testing a sub
        sample of sign combinations on the derivatives. The
        algorithm currently generates a random set of signs for
        the :math:`N-2` derivatives. It then flips sucessive signs in the
        list until it calculates a chi squared smaller than the
        previous evaluation of the objective function. For
        example a 4th order polynomial has 2 derivatives with :math:`m>=2`
        which means it has 4 sign combinations [1,1],[-1,-1],[-1,1]
        and [1,-1]. On first random generation we get [-1,1] with
        which we evaluate the objective function. We then flip the
        first sign and evaluate again with [1,1]. If the new chi chi squared
        is less than the first calculated value the algorithm
        then goes back to the original list and flips the second sign
        evaluating with [-1,-1]. The process repeats until the new
        chi squared is no longer smaller than the previous
        evaluation and the previous evaluation is taken to be optimal.
        The algorithm then repeats the entire process for a set number
        of random sign generations to ensure that the
        true minimum is identified. The number of repeats needed
        is dependent on the polynomial order. High polynomial
        orders require a larger number of repeats to find the true
        minimum. Currently the number of repeats is set at
        :math:`{2\times(N-2)^2}`.

    **model_type:** (Default = 'normalised_polynomial')

    The type of model used to fit the data. There is a built in library of
    maximally smooth functions that can be called by the user.

    *Accepted options:*

        'normalised_polynomial' - This is a polynomial of the form,

            .. math::
                {y=y_0 \sum (p_i\bigg(\frac{x}{x_0}\bigg)^i)}.

        'polynomial' - This is a polynomial of the form,
            .. math::

                {y=sum(p_i(x)^i)}.

        'MSF_2017_polynomial' - This is a polynomial of the form
            described in section 4 of
            `Sathyanarayana Rao, 2017
            <https://iopscience.iop.org/article/10.3847/1538-
            4357/aa69bd/meta>`__

        'logarithmic_polynomial' - This is a polynomial model
            similar to that used with the setting 'polynomial' but
            solved in log-space. It has the form,

            .. math::
                {log_{10}(y)=\sum(p_i(log_{10}(x))^i)}.

            NOTE this model will not work if the y values are negative.

    **base_dir:** (Default = 'Fitted_Output')
        This is the directory in which the output of the program is saved. If
        the directory does not exist the software will create it in the working
        as long as the files that preceed it also exist. When testing multiple
        model types it is recommended to include this in the base directory
        name eg `self.base_dir= 'Data_Name_' + self.model_type + '/'.`

    **cvxopt_maxiter:** (Default=1000)
        The maximum number of iterations for the cvxopt quadratic
        programming routine. If cvxopt reaches maxiter the fitting routine
        will exit with an error recommending this be increased.

    **filtering:** (Default=True)
        Generally for high order N there will be
        combinations of sign for which CVXOPT cannot find a solution and
        these terminate with the error "Terminated (Singular KKT Matrix)".
        If filtering is set to True these cases will be flagged with a warning
        and the corresponding sign combinations will be excluded when
        determining the best possible fit. Setting filtering to False will
        cause the program to crash with CVXOPT error.

    **all_output:** (Default=False)
        If set to True this will output the results of each run of cvxopt
        to the terminal.

    **ifp:** (Default = False)
        Setting equal to True allows for inflection points in the m order
        derivatives listed in ifp_derivatives.
        *NOTE:* The algorithm will not necessarily return derivatives
                with inflection points if this is set to True.
        *NOTE:* Allowing for inflection points will increasese run time.

    **ifp_list:** (Default = 'None')
        The list of derivatives you wish to allow
        to have inflection points in(see ifp above). This should be a list
        of derivative orders eg. if I have a fith order
        polynomial and I wish to allow the the second derivative to have
        an inflection point then ifp_list=[2]. If I wished to allow the
        second and fourth derivative to have inflection points
        I would write ifp_list=[2,4]. Values in ifp_list cannot exceed the
        number of possible derivatives and cannot equal 1.

    **data_save:** (Default = True)
        Setting data_save to True will save sample
        graphs of the derivatives, fit and residuals. The inputs to
        produce these graphs are all outputted from the *smooth* function
        and they can be reproduced with more specific axis labels/units in
        the users code. If filtering is also set to True, which it is by
        default, then parameters, objective function values and sign
        combinations from each successful run of cvxopt will be saved
        to the base directories in seperate folders. The condition on
        filtering prevents saving data from runs of cvxopt that did not
        find solutions and terminated with a singular KKT matrix.

    **warnings:** (Default = False)
        Setting to False will prevent warnings showing in the terminal.
        Setting to True will show all warnings.

    """
    def __init__(self):

        self.fit_type = 'qp-sign_flipping'
        self.model_type = 'normalised_polynomial'
        self.base_dir = 'Fitted_Output/'
        self.cvxopt_maxiter = 1000
        self.filtering = True
        self.all_output = False
        self.ifp = False
        self.ifp_list = 'None'
        self.data_save = False
        self.ud_initial_params = False
        self.warnings = False
