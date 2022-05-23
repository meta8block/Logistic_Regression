import ast
from hstest.stage_test import List
from hstest import *

answer_dict = {'coef_': [0.47488716263507635, -1.1358115859394329, -0.9647865195516206, -0.9578169580688974], 'accuracy': 0.9649122807017544}


class LogisticRegression(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase(time_limit=1000000)]

    def check(self, reply: str, attach):

        reply = reply.strip().lower()

        if len(reply) == 0:
            return CheckResult.wrong("No output was printed")

        if reply.count('{') != 1 or reply.count('}') != 1:
            return CheckResult.wrong('Print output as a dictionary')

        index_from = reply.find('{')
        index_to = reply.find('}')
        dict_str = reply[index_from: index_to + 1]

        try:
            user_dict = ast.literal_eval(dict_str)
        except Exception as e:
            return CheckResult.wrong(f"Seems that output is in wrong format.\n"
                                     f"Make sure you use only the following Python structures in the output: string, int, float, list, dictionary")

        if not isinstance(user_dict, dict):
            return CheckResult.wrong('Print output as a dictionary')

        if 'coef_' not in user_dict or 'accuracy' not in user_dict.keys():
            return CheckResult.wrong('Didn\'t find correct keys of the dictionary in the output.'
                                     'There should be "coef_" and "accuracy". Check the format in the Examples section.')

        user_coefficients = user_dict["coef_"]
        if not isinstance(user_coefficients, list):
            return CheckResult.wrong('Print coefficients as a list')

        if len(user_coefficients) != 4:
            if len(user_coefficients) == 3:
                return CheckResult.wrong('There should be the bias term. Check that fit_intercept=True')
            return CheckResult.wrong(
                f'The list of coefficients should contain 4 values, found {len(user_coefficients)}')

        answer_coefficients = answer_dict["coef_"]
        for user_coef, answer_coef in zip(user_coefficients, answer_coefficients):

            try:
                user_coef = float(user_coef)
            except ValueError:
                return CheckResult.wrong("There should be only numbers in the coefficients list, found something else")

            # 2% error is allowed
            error = abs(answer_coef * 0.02)
            if not answer_coef - error < user_coef < answer_coef + error:
                return CheckResult.wrong(
                    "Incorrect values of coefficients. Check your learning rate and epoch parameters and MSE gradient descent implementation.")

        user_acc = user_dict["accuracy"]
        answer_acc = answer_dict["accuracy"]
        if not isinstance(user_acc, float):
            return CheckResult.wrong('Print accuracy as a float')
        # 2% error is allowed
        error = abs(answer_acc * 0.02)
        if not answer_acc - error < user_acc < answer_acc + error:
            return CheckResult.wrong(
                f'Wrong accuracy value. Check the parameters of your train-test split. Don\'t forget to set random_state=43.')

        return CheckResult.correct()


if __name__ == '__main__':
    LogisticRegression('logistic').run_tests()
