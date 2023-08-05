# -*- coding: utf-8 -*-
"""
Created on Tues Feb 22 09:30:44 2016

@author: Timothy Brathwaite
@notes:  Credit is due to Akshay Vij and John Canny for the idea of using
         "mapping" matrices to avoid the need for "for loops" when computing
         quantities of interest such as probabilities, log-likelihoods,
         gradients, and hessians. This code is based on an earlier multinomial
         logit implementation by Akshay Vij which made use of such mappings.

         This version differs from version 1 by partitioning the parameters to
         be estimated, theta, as shape parameters, intercept parameters, and
         index coefficients.
"""

import pickle
from copy import deepcopy
from collections import OrderedDict

import scipy.linalg
import scipy.stats
import numpy as np
import pandas as pd

from choice_tools import create_design_matrix
from choice_tools import create_long_form_mappings
from choice_tools import convert_mixing_names_to_positions
from choice_tools import get_dataframe_from_data
from choice_calcs import calc_probabilities, calc_asymptotic_covariance
from nested_choice_calcs import calc_nested_probs
import mixed_logit_calcs as mlc


# Create a basic class that sets the structure for the discrete outcome models
# to be specified later. MNDC stands for MultiNomial Discrete Choice.
class MNDC_Model(object):
    """
    Parameters
    ----------
    data : str or pandas dataframe.
        If string, data should be an absolute or relative path to a CSV file
        containing the long format data for this choice model. Note long format
        is has one row per available alternative for each observation. If
        pandas dataframe, the dataframe should be the long format data for the
        choice model.
    alt_id_col : str.
        Should denote the column in data which contains the alternative
        identifiers for each row.
    obs_id_col : str.
        Should denote the column in data which contains the observation
        identifiers for each row.
    choice_col : str.
        Should denote the column in data which contains the ones and zeros that
        denote whether or not the given row corresponds to the chosen
        alternative for the given individual.
    specification : OrderedDict.
        Keys are a proper subset of the columns in `data`. Values are either a
        list or a single string, "all_diff" or "all_same". If a list, the
        elements should be:
            - single objects that are in the alternative ID column of `data`
            - lists of objects that are within the alternative ID column of
              `data`. For each single object in the list, a unique column will
              be created (i.e. there will be a unique coefficient for that
              variable in the corresponding utility equation of the
              corresponding alternative). For lists within the
              `specification` values, a single column will be created for all
              the alternatives within the iterable (i.e. there will be one
              common coefficient for the variables in the iterable).
    intercept_ref_pos : int, optional.
         Valid only when the intercepts being estimated are not part of the
         index. Specifies the alternative in the ordered array of unique
         alternative ids whose intercept or alternative-specific constant is
         not estimated, to ensure model identifiability. Default == None.
    shape_ref_pos : int, optional.
        Specifies the alternative in the ordered array of unique alternative
        ids whose shape parameter is not estimated, to ensure model
        identifiability. Default == None.
    names : OrderedDict, optional.
        Should have the same keys as `specification`. For each key:
            - if the corresponding value in `specification` is "all_same", then
              there should be a single string as the value in names.
            - if the corresponding value in `specification` is "all_diff", then
              there should be a list of strings as the value in names. There
              should be one string in the value in names for each possible
              alternative.
            - if the corresponding value in `specification` is a list, then
              there should be a list of strings as the value in names. There
              should be one string the value in names per item in the value in
              `specification`.
        Default == None.
    intercept_names : list, or None, optional.
        If a list is passed, then the list should have the same number of
        elements as there are possible alternatives in data, minus 1. Each
        element of the list should be a string--the name of the corresponding
        alternative's intercept term, in sorted order of the possible
        alternative IDs. If None is passed, the resulting names that are shown
        in the estimation results will be
        `["Outside_ASC_{}".format(x) for x in shape_names]`. Default = None.
    shape_names : list, or None, optional.
        If a list is passed, then the list should have the same number of
        elements as there are possible alternative IDs in data. Each element of
        the list should be a string denoting the name of the corresponding
        shape parameter for the given alternative, in sorted order of the
        possible alternative IDs. Default == None.
    nest_spec : OrderedDict, or None, optional.
        Keys are strings that define the name of the nests. Values are lists of
        alternative ids, denoting which alternatives belong to which nests.
        Each alternative id must only be associated with a single nest!
        Default == None.
    mixing_vars : list, or None, optional.
        All elements of the list should be strings. Each string should be
        present in the values of `names.values()` and they're associated
        variables should only be index variables (i.e. part of the design
        matrix). If `model_type == "Mixed Logit"`, then `mixing_vars` must be
        passed. Default == None.
    mixing_id_col : str, or None, optional.
        Should be a column heading in `data`. Should denote the column in
        `data` which contains the identifiers of the units of observation over
        which the coefficients of the model are thought to be randomly
        distributed. If `model_type == "Mixed Logit"`, then `mixing_id_col`
        must be passed. Default == None.
    model_type : str, optional.
        Denotes the model type of the choice model being instantiated.
        Default == "".
    """
    def __init__(self,
                 data,
                 alt_id_col,
                 obs_id_col,
                 choice_col,
                 specification,
                 intercept_ref_pos=None,
                 shape_ref_pos=None,
                 names=None,
                 intercept_names=None,
                 shape_names=None,
                 nest_spec=None,
                 mixing_vars=None,
                 mixing_id_col=None,
                 model_type=""):
        dataframe = get_dataframe_from_data(data)

        ##########
        # Make sure all necessary columns are in the dataframe
        ##########
        for column in [alt_id_col, obs_id_col, choice_col]:
            try:
                assert column in dataframe.columns
            except AssertionError as e:
                print("{} not in data.columns".format(column))
                raise e

        ##########
        # Make sure the various 'name' arguments are of the correct lengths
        ##########
        # Get a sorted array of all possible alternative ids in the dataset
        all_ids = np.sort(dataframe[alt_id_col].unique())

        # Check for correct length of shape_names and intercept_names
        name_and_ref_args = [(shape_names,
                              shape_ref_pos,
                              "shape_names"),
                             (intercept_names,
                              intercept_ref_pos,
                              "intercept_names")]
        for alt_param_names, alt_ref_pos, param_string in name_and_ref_args:
            if alt_param_names is not None:
                if alt_ref_pos is None:
                    if param_string == "intercept_names":
                        msg = "At least one intercept should be constrained"
                        raise ValueError(msg)
                    alt_params_not_estimated = 0
                elif isinstance(alt_ref_pos, int):
                    alt_params_not_estimated = 1
                else:
                    msg = "Ref position is of the wrong type. "
                    msg_2 = "Should be an integer"
                    raise AssertionError(msg + msg_2)
                try:
                    cond_1 = (len(alt_param_names) ==
                              (len(all_ids) - alt_params_not_estimated))
                    assert cond_1
                except AssertionError as e:
                    print("{} is of the wrong length".format(param_string))
                    print("len({}) == {}".format(param_string,
                                                 len(alt_param_names)))
                    correct_length = len(all_ids) - alt_params_not_estimated
                    print("The correct length is: {}".format(correct_length))
                    raise e

        ##########
        # Check for validity of the nest_spec argument if necessary
        ##########
        if nest_spec is not None:
            try:
                assert isinstance(nest_spec, OrderedDict)
            except AssertionError:
                msg = "nest_spec must be an OrderedDict."
                raise ValueError(msg)

            try:
                assert all([isinstance(k, str) for k in nest_spec])
                assert all([isinstance(nest_spec[k], list) for k in nest_spec])
            except AssertionError:
                msg = "All nest_spec keys/values must be strings/lists."
                raise ValueError(msg)

            try:
                empty_nests = []
                for k in nest_spec:
                    if len(nest_spec[k]) == 0:
                        empty_nests.append(k)
                assert empty_nests == []
            except AssertionError:
                msg = "The following nests are INCORRECTLY empty: {}"
                raise ValueError(msg.format(empty_nests))

            try:
                list_elements = []
                for key in nest_spec:
                    list_elements.extend(nest_spec[key])
                assert all([isinstance(x, int) for x in list_elements])
            except AssertionError:
                msg = "All elements of the nest_spec values should be integers"
                raise ValueError(msg)

            try:
                assert len(set(list_elements)) == len(list_elements)
            except AssertionError:
                msg = "Each alternative id should only be in a single nest."
                raise ValueError(msg)

            try:
                unaccounted_alt_ids = []
                for alt_id in all_ids:
                    if alt_id not in list_elements:
                        unaccounted_alt_ids.append(alt_id)
                assert unaccounted_alt_ids == []
            except AssertionError:
                msg = "Associate the following alternative ids with a nest: {}"
                raise ValueError(msg.format(unaccounted_alt_ids))

            try:
                invalid_alt_ids = []
                for x in list_elements:
                    if x not in all_ids:
                        invalid_alt_ids.append(x)
                assert invalid_alt_ids == []
            except AssertionError:
                msg = "The following elements are not in df[alt_id_col]: {}"
                raise ValueError(msg.format(invalid_alt_ids))

        ##########
        # Add an intercept column to the data if necessary based on the model
        # specification.
        ##########
        condition_1 = "intercept" in specification
        condition_2 = "intercept" not in dataframe.columns

        if condition_1 and condition_2:
            dataframe["intercept"] = 1.0

        ##########
        # Make sure all the columns in the specification dict are all
        # in the dataframe
        ##########
        problem_cols = []
        dataframe_cols = dataframe.columns
        for key in specification:
            if key not in dataframe_cols:
                problem_cols.append(key)
        if problem_cols != []:
            msg = "The following keys in the specification are not in 'data':"
            print(msg)
            print(problem_cols)
            raise ValueError

        ##########
        # Make sure that the columns we are using in the specification are all
        # numeric and exclude positive or negative infinity variables.
        ##########
        problem_cols = []
        for col in specification:
            # The condition below checks for positive or negative inifinity
            # values.
            if np.isinf(dataframe[col]).any():
                problem_cols.append(col)
            # The condition below checks for values that are not real numbers
            # This will catch values that are strings.
            elif not np.isreal(dataframe[col]).all():
                problem_cols.append(col)

        if problem_cols != []:
            msg = "The following columns contain either +/- inifinity values "
            msg_2 = "or values that are not real numbers (e.g. strings):"
            print(msg + msg_2)
            print(problem_cols)
            raise ValueError

        ##########
        # Create the design matrix for this model
        ##########
        design_res = create_design_matrix(dataframe,
                                          specification,
                                          alt_id_col,
                                          names=names)
        ##########
        # Store needed data
        ##########
        self.data = dataframe
        self.name_spec = names
        self.design = design_res[0]
        self.ind_var_names = design_res[1]
        self.alt_id_col = alt_id_col
        self.obs_id_col = obs_id_col
        self.choice_col = choice_col
        self.specification = specification
        self.alt_IDs = dataframe[alt_id_col].values
        self.choices = dataframe[choice_col].values
        self.model_type = model_type
        self.shape_names = shape_names
        self.intercept_names = intercept_names
        self.shape_ref_position = shape_ref_pos
        self.intercept_ref_position = intercept_ref_pos
        self.nest_names = nest_spec.keys() if nest_spec is not None else None
        self.nest_spec = nest_spec
        self.mixing_id_col = mixing_id_col
        self.mixing_vars = mixing_vars
        if mixing_vars is not None:
            mixing_pos = convert_mixing_names_to_positions(mixing_vars,
                                                           self.ind_var_names)
        else:
            mixing_pos = None
        self.mixing_pos = mixing_pos

        return None

    def get_mappings_for_fit(self, dense=False):
        """
        Parameters
        ----------
        dense : bool, optional.
            Dictates if sparse matrices will be returned or dense numpy arrays.

        Returns
        -------
        mapping_dict : OrderedDict.
            Keys will be `["rows_to_obs", "rows_to_alts", "chosen_row_to_obs",
            "rows_to_nests"]`. The value for `rows_to_obs` will map the rows of
            the `long_form` to the unique observations (on the columns) in
            their order of appearance. The value for `rows_to_alts` will map
            the rows of the `long_form` to the unique alternatives which are
            possible in the dataset (on the columns), in sorted order--not
            order of appearance. The value for `chosen_row_to_obs`, if not
            None, will map the rows of the `long_form` that contain the chosen
            alternatives to the specific observations those rows are associated
            with (denoted by the columns). The value of `rows_to_nests`, if not
            None, will map the rows of the `long_form` to the nest (denoted by
            the column) that contains the row's alternative. If `dense==True`,
            the returned values will be dense numpy arrays. Otherwise, the
            returned values will be scipy sparse arrays.
        """
        return create_long_form_mappings(self.data,
                                         self.obs_id_col,
                                         self.alt_id_col,
                                         choice_col=self.choice_col,
                                         nest_spec=self.nest_spec,
                                         mix_id_col=self.mixing_id_col,
                                         dense=dense)

    def store_fit_results(self, results_dict):
        """
        Parameters
        ----------
        results_dict : dict.
            The estimation result dictionary that is output from
            scipy.optimize.minimize. In addition to the standard keys which are
            included, it should also contain the following keys:
           ` ["final_gradient", "final_hessian", "fisher_info",
            "final_log_likelihood", "chosen_probs", "long_probs", "residuals",
             "ind_chi_squareds"]`.
            The "final_gradient", "final_hessian", and "fisher_info" values
            should be the gradient, hessian, and Fisher-Information Matrix of
            the log likelihood, evaluated at the final parameter vector.

        Returns
        -------
        None. Will calculate and store a variety of estimation results and
        inferential statistics as attributes of the model instance.
        """
        # Store the log-likelilhood, fitted probabilities, residuals, and
        # individual chi-square statistics
        self.log_likelihood = results_dict["final_log_likelihood"]
        self.fitted_probs = results_dict["chosen_probs"]
        self.long_fitted_probs = results_dict["long_probs"]
        self.long_residuals = results_dict["residuals"]
        self.ind_chi_squareds = results_dict["ind_chi_squareds"]
        self.chi_square = self.ind_chi_squareds.sum()

        # Store the 'estimation success' of the optimization
        self.estimation_success = results_dict["success"]
        self.estimation_message = results_dict["message"]

        # Account for peculiar things from the em algorithm
        if "log_likelihood_progress" in results_dict:
            self.log_likelihood_progression =\
                            np.array(results_dict["log_likelihood_progress"])
        else:
            self.log_likelihood_progression = None
        if "estimation_reason" in results_dict:
            self.em_estimation_reason = results_dict["estimation_reason"]
        else:
            self.em_estimation_reason = None
        # Account for attributes from the mixed logit model.
        if not hasattr(self, "design_3d"):
            self.design_3d = None

        # Store the summary measures of the model fit
        self.rho_squared = results_dict["rho_squared"]
        self.rho_bar_squared = results_dict["rho_bar_squared"]

        # Store the initial and null log-likelihoods
        self.null_log_likelihood = results_dict["log_likelihood_null"]

        # Initialize the lists of all parameter names and all parameter values
        # Note we add the new mixing variables to the list of index
        # coefficients after estimation so that we can correctly create the
        # design matrix needed for estimation
        if self.mixing_vars is not None:
            new_ind_var_names = ["Sigma " + x for x in self.mixing_vars]
            self.ind_var_names += new_ind_var_names
        all_names = deepcopy(self.ind_var_names)
        all_params = [deepcopy(results_dict["utility_coefs"])]

        ##########
        # Figure out whether this model had nest, shape, or intercept
        # parameters and store each of these appropriately
        ##########
        if results_dict["intercept_params"] is not None:
            # Identify the number of intercept parameters
            num_intercepts = results_dict["intercept_params"].shape[0]

            # Get the names of the intercept parameters
            if self.intercept_names is None:
                intercept_names = ["Outside_ASC_{}".format(x) for x in
                                   range(1, num_intercepts + 1)]
            else:
                intercept_names = self.intercept_names

            # Store the names of the intercept parameters
            all_names = intercept_names + all_names
            # Store the values of the intercept parameters
            all_params.insert(0, results_dict["intercept_params"])

            # Store the intercept parameters
            self.intercepts = pd.Series(results_dict["intercept_params"],
                                        index=intercept_names,
                                        name="intercept_parameters")
        else:
            self.intercepts = None

        if results_dict["shape_params"] is not None:
            # Identify the number of shape parameters
            num_shapes = results_dict["shape_params"].shape[0]

            # Get the names of the shape parameters
            if self.shape_names is None:
                shape_names = ["shape_{}".format(x) for x in
                               range(1, num_shapes + 1)]
            else:
                shape_names = self.shape_names

            # Store the names of the shape parameters
            all_names = shape_names + all_names
            # Store the values of the shape parameters
            all_params.insert(0, results_dict["shape_params"])

            # Store the shape parameters
            self.shapes = pd.Series(results_dict["shape_params"],
                                    index=shape_names,
                                    name="shape_parameters")
        else:
            self.shapes = None

        if results_dict["nest_params"] is not None:
            # Identify the number of nestt parameters
            num_nests = results_dict["nest_params"].shape[0]

            # Get the names of the nest parameters
            if self.nest_names is None:
                nest_names = ["Nest_Param_{}".format(x) for x in
                              range(1, num_nests + 1)]
            else:
                nest_names = [x + " Nest Param" for x in self.nest_names]

            # Store the names of the nest parameters
            all_names = nest_names + all_names
            # Store the values of the nest parameters
            all_params.insert(0, results_dict["nest_params"])

            # Store the nest parameters
            self.nests = pd.Series(results_dict["nest_params"],
                                   index=nest_names,
                                   name="nest_parameters")
        else:
            self.nests = None

        ##########
        # Store the model results and values needed for model inference
        ##########
        # Store the utility coefficients
        self.coefs = pd.Series(results_dict["utility_coefs"],
                               index=self.ind_var_names,
                               name="coefficients")

        # Store the gradient
        self.gradient = pd.Series(results_dict["final_gradient"],
                                  index=all_names,
                                  name="gradient")

        # Store the hessian
        self.hessian = pd.DataFrame(results_dict["final_hessian"],
                                    columns=all_names,
                                    index=all_names)

        # Store the variance-covariance matrix
        self.cov = pd.DataFrame(-1 * scipy.linalg.inv(self.hessian),
                                columns=all_names,
                                index=all_names)

        # Store all of the estimated parameters
        self.params = pd.Series(np.concatenate(all_params, axis=0),
                                index=all_names,
                                name="parameters")

        # Store the standard errors
        self.standard_errors = pd.Series(np.sqrt(np.diag(self.cov)),
                                         index=all_names,
                                         name="std_err")

        # Store the t-stats of the estimated parameters
        self.tvalues = self.params / self.standard_errors
        self.tvalues.name = "t_stats"

        # Store the p-values
        self.pvalues = pd.Series(2 *
                                 scipy.stats.norm.sf(np.abs(self.tvalues)),
                                 index=all_names,
                                 name="p_values")

        # Store the fischer information matrix of estimated coefficients
        self.fisher_information = pd.DataFrame(results_dict["fisher_info"],
                                               columns=all_names,
                                               index=all_names)

        # Store the 'robust' variance-covariance matrix
        self.robust_cov = calc_asymptotic_covariance(self.hessian,
                                                     self.fisher_information)

        # Store the 'robust' standard errors
        self.robust_std_errs = pd.Series(np.sqrt(np.diag(self.robust_cov)),
                                         index=all_names,
                                         name="robust_std_err")

        # Store the 'robust' t-stats of the estimated coefficients
        self.robust_t_stats = self.params / self.robust_std_errs
        self.robust_t_stats.name = "robust_t_stats"

        # Store the 'robust' p-values
        one_sided_p_vals = scipy.stats.norm.sf(np.abs(self.robust_t_stats))
        self.robust_p_vals = pd.Series(2 *
                                       one_sided_p_vals,
                                       index=all_names,
                                       name="robust_p_values")
        #####
        # Insert cleanup activity for the covariance matrix, the hessian,
        # the fisher information matrix, the robust covariance matrix, the
        # standard errors, the t-stats, the p-values, the robust standard
        # errors, the robust t-stats, and the robust p-values on account of
        # any "constrained" parameters that were not actually estimated.
        #####
        # Only perform cleanup activities if necessary
        params_constrained = ("constrained_pos" in results_dict and
                              results_dict["constrained_pos"] is not None)
        if params_constrained:
            for series in [self.standard_errors, self.tvalues,
                           self.pvalues, self.robust_std_errs,
                           self.robust_t_stats, self.robust_p_vals]:
                for pos in results_dict["constrained_pos"]:
                    series.loc[all_names[pos]] = np.nan

        ##########
        # Store a summary dataframe of the estimation results
        # (base it on statsmodels summary dataframe/table perhaps?)
        ##########
        self.summary = pd.concat((self.params,
                                  self.standard_errors,
                                  self.tvalues,
                                  self.pvalues,
                                  self.robust_std_errs,
                                  self.robust_t_stats,
                                  self.robust_p_vals), axis=1)

        ##########
        # Record values for the fit_summary and statsmodels table
        ##########
        # Record the number of observations
        self.nobs = self.fitted_probs.shape[0]
        # This is the number of estimated parameters
        self.df_model = self.params.shape[0]
        # The number of observations minus the number of estimated parameters
        self.df_resid = self.nobs - self.df_model
        # This is just the log-likelihood. The opaque name is used for
        # conformance with statsmodels
        self.llf = self.log_likelihood
        # This is just a repeat of the standard errors
        self.bse = self.standard_errors

        ##########
        # Store a "Fit Summary"
        ##########
        self.fit_summary = pd.Series([self.df_model,
                                      self.nobs,
                                      self.null_log_likelihood,
                                      self.log_likelihood,
                                      self.rho_squared,
                                      self.rho_bar_squared,
                                      self.estimation_message],
                                     index=["Number of Parameters",
                                            "Number of Observations",
                                            "Null Log-Likelihood",
                                            "Fitted Log-Likelihood",
                                            "Rho-Squared",
                                            "Rho-Bar-Squared",
                                            "Estimation Message"])

    # Note that the function below is a placeholder and template for the
    # function to be placed in each model class.
    def fit_mle(self,
                init_vals,
                print_res=True,
                method="BFGS",
                loss_tol=1e-06,
                gradient_tol=1e-06,
                maxiter=1000,
                ridge=None,
                *args):
        """
        Parameters
        ----------
        init_vals : 1D ndarray.
            The initial values to start the optimizatin process with. There
            should be one value for each utility coefficient, outside intercept
            parameter, shape parameter, and nest parameter being estimated.
        print_res : bool, optional.
            Determines whether the timing and initial and final log likelihood
            results will be printed as they they are determined.
        method : str, optional.
            Should be a valid string which can be passed to
            scipy.optimize.minimize. Determines the optimization algorithm
            which is used for this problem.
        loss_tol : float, optional.
            Determines the tolerance on the difference in objective function
            values from one iteration to the next which is needed to determine
            convergence. Default == 1e-06.
        gradient_tol : float, optional.
            Determines the tolerance on the difference in gradient values from
            one iteration to the next which is needed to determine convergence.
            Default == 1e-06.
        ridge : int, float, long, or None, optional.
            Determines whether or not ridge regression is performed. If an int,
            float or long is passed, then that scalar determines the ridge
            penalty for the optimization. Default == None.

        Returns
        -------
        None. Saves estimation results to the model instance.
        """

        print("This model class' fit_mle method has not been constructed.")
        raise NotImplementedError

        return None

    def print_summaries(self):
        """
        Returns None. Will print the measures of fit and the estimation results
        for the  model.
        """
        if hasattr(self, "fit_summary") and hasattr(self, "summary"):
            print("\n")
            print(self.fit_summary)
            print("=" * 30)
            print(self.summary)

        else:
            msg = "This {} object has not yet been estimated so there "
            msg_2 = "are no estimation summaries to print."
            print(msg.format(self.model_type) + msg_2)

        return None

    # Note this functionn is called when creating the statsmodels summary.
    def conf_int(self, alpha=0.05, coefs=None, return_df=False):
        """
        Parameters
        ----------
        alpha : float, optional.
            Should be between 0.0 and 1.0. Determines the (1-alpha)% confidence
            interval that will be reported. Default == 0.05.
        coefs : array-like, optional.
            Should contain strings that denote the coefficient names that one
            wants the confidence intervals for. Default == None because that
            will return the confidence interval for all variables.
        return_df : bool, optional.
            Determines whether the returned value will be a dataframe or a
            numpy array. Default = False.

        Returns
        -------
        pandas dataframe or ndarray.
            Depends on return_df kwarg. The first column contains the lower
            bound to the confidence interval whereas the second column contains
            the upper values of the confidence intervals.
        """

        # Get the critical z-value for alpha / 2
        z_critical = scipy.stats.norm.ppf(1.0 - alpha / 2.0,
                                          loc=0, scale=1)

        # Calculate the lower and upper values for the confidence interval.
        lower = self.params - z_critical * self.standard_errors
        upper = self.params + z_critical * self.standard_errors

        # Combine the various series.
        combined = pd.concat((lower, upper), axis=1)

        # Subset the combined dataframe if need be.
        if coefs is not None:
            combined = combined.loc[coefs, :]

        # Return the desired object, whether dataframe or array
        if return_df:
            return combined
        else:
            return combined.values

    def get_statsmodels_summary(self,
                                title=None,
                                alpha=.05):
        """
        Parameters
        ----------
        title : str, or None, optional.
            Will be the title of the returned summary. If None, the default
            title is used.
        alpha : float, optional.
            Should be between 0.0 and 1.0. Determines the width of the
            displayed, (1 - alpha)% confidence interval.

        Returns
        -------
        statsmodels.summary object.
        """
        try:
            # Get the statsmodels Summary class
            from statsmodels.iolib.summary import Summary
        except:
            print("statsmodels not installed. Resorting to standard summary")
            return self.print_summaries()

        try:
            assert hasattr(self, "estimation_success")
        except AssertionError:
            msg = "Must estimate a model before a summary can be returned."
            raise ValueError(msg)

        # Get an instantiation of the Summary class.
        smry = Summary()

        # Get the yname and yname_list.
        # Note I'm not really sure what the yname_list is.
        new_yname, new_yname_list = self.choice_col, None

        # Get the model name
        model_name = self.model_type

        ##########
        # Note the following commands are basically directly from
        # statsmodels.discrete.discrete_model
        ##########
        top_left = [('Dep. Variable:', None),
                    ('Model:', [model_name]),
                    ('Method:', ['MLE']),
                    ('Date:', None),
                    ('Time:', None),
            # ('No. iterations:', ["%d" % self.mle_retvals['iterations']]),
                    ('converged:', [str(self.estimation_success)])
                    ]

        top_right = [('No. Observations:', ["{:,}".format(self.nobs)]),
                     ('Df Residuals:', ["{:,}".format(self.df_resid)]),
                     ('Df Model:', ["{:,}".format(self.df_model)]),
                     ('Pseudo R-squ.:',
                      ["{:.3f}".format(self.rho_squared)]),
                     ('Pseudo R-bar-squ.:',
                      ["{:.3f}".format(self.rho_bar_squared)]),
                     ('Log-Likelihood:', ["{:,.3f}".format(self.llf)]),
                     ('LL-Null:',
                      ["{:,.3f}".format(self.null_log_likelihood)]),
                     ]

        if title is None:
            title = model_name + ' ' + "Regression Results"

        xnames = self.params.index.tolist()

        # for top of table
        smry.add_table_2cols(self,
                             gleft=top_left,
                             gright=top_right,  # [],
                             yname=new_yname,
                             xname=xnames,
                             title=title)
        # for parameters, etc
        smry.add_table_params(self,
                              yname=[new_yname_list],
                              xname=xnames,
                              alpha=alpha,
                              use_t=False)
        return smry

    def check_param_list_validity(self, param_list):
        """
        Parameters
        ----------
        param_list : list.
            Contains four elements, each being a numpy array. Either all of the
            arrays should be 1D or all of the arrays should be 2D. If 2D, the
            arrays should have the same number of columns. Each column being a
            particular set of parameter values that one wants to predict with.
            The first element in the list should be the index coefficients. The
            second element should contain the 'outside' intercept parameters if
            there are any, or None otherwise. The third element should contain
            the shape parameters if there are any or None otherwise.
            Default == None.

        Returns
        -------
        None. Will check whether `param_list` and its elements meet all
        requirements specified above and required for correct calculation of
        the probabilities to be predicted.
        """
        if param_list is None:
            return None

        # Make sure there are three elements in param_list
        try:
            assert isinstance(param_list, list)
            assert len(param_list) == 4
        except AssertionError as e:
            print("param_list must be a list containing 3 elements.")
            raise e

        # Make sure each element in the list is a numpy array or is None
        try:
            assert isinstance(param_list[0], np.ndarray)
            assert all([(x is None or isinstance(x, np.ndarray))
                        for x in param_list])
        except AssertionError as e:
            print("param_list[0] must be a numpy array.")
            print("All other elements must be numpy arrays or None.")
            raise e

        # Make sure each array in param_list has the same number of dimensions
        try:
            num_dimensions = len(param_list[0].shape)
            assert num_dimensions in [1, 2]
            assert all([(x is None or (len(x.shape) == num_dimensions))
                        for x in param_list])
        except AssertionError as e:
            print("Each array in param_list should be 1D or 2D.")
            print("And all arrays should have the same number of dimensions.")
            raise e

        # If using 2D arrays, ensure each array has the same number of columns.
        if num_dimensions == 2:
            try:
                num_columns = param_list[0].shape[1]
                assert all([x is None or (x.shape[1] == num_columns)
                            for x in param_list])
            except AssertionError as e:
                print("param_list arrays should have equal number of columns.")
                raise e

        # Make sure each array has the correct number of elements
        try:
            num_index_coefs = len(self.ind_var_names)
            assert param_list[0].shape[0] == num_index_coefs
        except AssertionError as e:
            msg = "param_list[0].shape[0] should equal {}, but it does not"
            print(msg.format(num_index_coefs))
            raise e

        if param_list[1] is not None:
            try:
                num_intercepts = (0 if self.intercept_names is None else
                                  len(self.intercept_names))
                assert param_list[1].shape[0] == num_intercepts
            except AssertionError as e:
                msg = "param_list[1].shape[0] should equal {}, but it does not"
                print(msg.format(num_intercepts))
                raise e

        if param_list[2] is not None:
            try:
                num_shapes = (0 if self.shape_names is None else
                              len(self.shape_names))
                assert param_list[2].shape[0] == num_shapes
            except AssertionError as e:
                msg = "param_list[2].shape[0] should equal {}, but it does not"
                print(msg.format(num_shapes))
                raise e

        if param_list[3] is not None:
            try:
                num_nests = (0 if self.nest_names is None else
                             len(self.nest_names))
                assert param_list[3].shape[0] == num_nests
            except AssertionError as e:
                msg = "param_list[3].shape[0] should equal {}, but it does not"
                print(msg.format(num_nests))
                raise e

        return None

    def predict(self,
                data,
                param_list=None,
                return_long_probs=True,
                choice_col=None,
                num_draws=None,
                seed=None):
        """
        Parameters
        ----------
        data : string or pandas dataframe.
            If string, data should be an absolute or relative path to a CSV
            file containing the long format data for this choice model. Note
            long format is has one row per available alternative for each
            observation. If pandas dataframe, the dataframe should be the long
            format data for the choice model. The data should include all of
            the same columns as the original data used to construct the choice
            model, with the sole exception of the "intercept" column. If needed
            the "intercept" column will be dynamically created.
        param_list : list, optional.
            Contains four elements, each being a numpy array. Either all of the
            arrays should be 1D or all of the arrays should be 2D. If 2D, the
            arrays should have the same number of columns. Each column being a
            particular set of parameter values that one wants to predict with.
            The first element in the list should contain the index
            coefficients. The second element should contain the 'outside'
            intercept parameters if there are any, or None otherwise. The third
            element should contain the shape parameters if there are any or
            None otherwise. The fourth element should contain the nest
            coefficients if there are any or None otherwise. Default == None.
        return_long_probs : bool, optional.
            Indicates whether or not the long format probabilites (a 1D numpy
            array with one element per observation per available alternative)
            should be returned. Default == True.
        choice_col : str, optional.
            Denotes the column in `long_form` which contains a one if the
            alternative pertaining to the given row was the observed outcome
            for the observation pertaining to the given row and a zero
            otherwise. Default == None.
        num_draws : int, or None, optional.
            Should be greater than zero. Denotes the number of draws that we
            are making from each normal distribution. This kwarg is only used
            if self.model_type == "Mixed Logit Model". Default == None.
        seed : int, or None, optional.
            If an int is passed, it should be greater than zero. Denotes the
            value to be used in seeding the random generator used to generate
            the draws from the normal distribution. This kwarg is only used if
            self.model_type == "Mixed Logit Model". Default == None.

        Returns
        -------
        numpy array or tuple of two numpy arrays.
            If `choice_col` is passed AND `return_long_probs is True`, then the
            tuple `(chosen_probs, long_probs)` is returned. If
            `return_long_probs is True` and `chosen_row_to_obs is None`, then
            `long_probs` is returned. If `chosen_row_to_obs` is passed and
            `return_long_probs is False` then `chosen_probs` is returned.

            `chosen_probs` is a 1D numpy array of shape (num_observations,).
            Each element is the probability of the corresponding observation
            being associated with its realized outcome.

            `long_probs` is a 1D numpy array with one element per observation
            per available alternative for that observation. Each element is the
            probability of the corresponding observation being associated with
            that rows corresponding alternative.

            It is NOT valid to have `chosen_row_to_obs == None` and
            `return_long_probs == False`.
        """
        # Get the dataframe of observations we'll be predicting on
        dataframe = get_dataframe_from_data(data)

        # Determine the conditions under which we will add an intercept column
        # to our long format dataframe.
        condition_1 = "intercept" in self.specification
        condition_2 = "intercept" not in dataframe.columns

        if condition_1 and condition_2:
            dataframe["intercept"] = 1.0

        # Make sure the necessary columns are in the long format dataframe
        for column in [self.alt_id_col,
                       self.obs_id_col,
                       self.mixing_id_col]:
            if column is not None:
                try:
                    assert column in dataframe.columns
                except AssertionError as e:
                    print("{} not in data.columns".format(column))
                    raise e

        # If param_list is passed, check the validity of its elements
        self.check_param_list_validity(param_list)

        # Get the new column of alternative IDs and get the new design matrix
        new_alt_IDs = dataframe[self.alt_id_col].values

        new_design_res = create_design_matrix(dataframe,
                                              self.specification,
                                              self.alt_id_col,
                                              names=self.name_spec)

        new_design = new_design_res[0]

        # Get the new mappings between the alternatives and observations
        mapping_res = create_long_form_mappings(dataframe,
                                                self.obs_id_col,
                                                self.alt_id_col,
                                                choice_col=choice_col,
                                                nest_spec=self.nest_spec,
                                                mix_id_col=self.mixing_id_col)

        new_rows_to_obs = mapping_res["rows_to_obs"]
        new_rows_to_alts = mapping_res["rows_to_alts"]
        new_chosen_to_obs = mapping_res["chosen_row_to_obs"]
        new_rows_to_nests = mapping_res["rows_to_nests"]
        new_rows_to_mixers = mapping_res["rows_to_mixers"]

        # Get the parameter arrays to be used in calculating the probabilities
        if param_list is None:
            new_index_coefs = self.coefs.values
            new_intercepts = (self.intercepts.values if self.intercepts
                              is not None else None)
            new_shape_params = (self.shapes.values if self.shapes
                                is not None else None)
            new_nest_coefs = (self.nests.values if self.nests
                              is not None else None)
        else:
            new_index_coefs = param_list[0]
            new_intercepts = param_list[1]
            new_shape_params = param_list[2]
            new_nest_coefs = param_list[3]

        # Get the probability of each observation choosing each available
        # alternative
        if self.model_type == "Nested Logit Model":
            # This condition accounts for the fact that we have a different
            # functional interface for nested vs non-nested models
            return calc_nested_probs(new_nest_coefs,
                                     new_index_coefs,
                                     new_design,
                                     new_rows_to_obs,
                                     new_rows_to_nests)
        elif self.model_type == "Mixed Logit Model":
            ##########
            # This condition accounts for the fact that Mixed Logit models have
            # a different functional interface than the standard logit-type
            # models.
            ##########
            # Get the draws for each random coefficient
            num_mixing_units = new_rows_to_mixers.shape[1]
            draw_list = mlc.get_normal_draws(num_mixing_units,
                                             num_draws,
                                             len(self.mixing_pos),
                                             seed=seed)
            # Calculate the 3D design matrix for the prediction.
            design_args = (new_design,
                           draw_list,
                           self.mixing_pos,
                           new_rows_to_mixers)
            new_design_3d = mlc.create_expanded_design_for_mixing(*design_args)
            # Calculate the desired probabilities for the mixed logit model.
            prob_args = (new_index_coefs,
                         new_design_3d,
                         new_alt_IDs,
                         new_rows_to_obs,
                         new_rows_to_alts,
                         self.utility_transform)
            prob_kwargs = {"intercept_params": new_intercepts,
                           "shape_params": new_shape_params,
                           "chosen_row_to_obs": new_chosen_to_obs,
                           "return_long_probs": return_long_probs}
            prob_array = calc_probabilities(*prob_args, **prob_kwargs)
            return prob_array.mean(axis=1)
        else:
            return calc_probabilities(new_index_coefs,
                                      new_design,
                                      new_alt_IDs,
                                      new_rows_to_obs,
                                      new_rows_to_alts,
                                      self.utility_transform,
                                      intercept_params=new_intercepts,
                                      shape_params=new_shape_params,
                                      chosen_row_to_obs=new_chosen_to_obs,
                                      return_long_probs=return_long_probs)

    def to_pickle(self, filepath):
        """
        Parameters
        ----------
        filepath : str.
            Should end in .pkl. If it does not, ".pkl" will be appended to the
            passed string.

        Returns
        -------
        None. Saves the model object to the location specified by `filepath`.
        """
        assert isinstance(filepath, str)
        if filepath[-4:] != ".pkl":
            filepath = filepath + ".pkl"
        with open(filepath, "wb") as f:
            pickle.dump(self, f)
        print("Model saved to {}".format(filepath))

        return None
