Feature: Analyse Software Stack (in a Container Image) and get Recommendations

    Background: Test Environment
        Given I am using the TEST environement

    @wip
    Scenario Outline: Submitting a Container Image for analysis
        When I submit <a container image> to the User API for analysis by <analyser image>
        Then I want to receive a Analyser Job ID
        And I wait for the Analyser Job to finish successful
        And the Analyzer Job Log should not be empty

        Examples: Container Image and Analysers
            | a container image | analyser image               |
            | fedora:27         | fridex/thoth-package-extract |

    @wip
    Scenario: Query for currently available Analyser Results
        When I query the Result API for a list of analyser results
        Then the list of results should not be empty

    @wip
    Scenario: Get the Analyser Results for my last submitted Container Image
        When I query the Result API for my latest analyser result
        Then the result should not be empty
        And the analyser should be "thoth-package-extract"
        And the analyser version should be "1.0.0"
<<<<<<< HEAD:features/analyse_container_image.feature
=======

    @wip
    Scenario Outline: Finished analysing a software stack
        When I submit <a container image> to the User API for analysis by <analyser image>
        Then I wait for the analysis to be finished

        Examples: Container Image and Analysers
            | a container image | analyser image               |
            | fedora:27         | fridex/thoth-package-extract |

    @wip
    Scenario: Get Recommendations about a software stack
        When I query Thoth for Recommendation about <a software stack>
        Then I want to receive a Recommdation
        And the recommendation should be "thoth-recommendation"
        And the recommendation version should be "0.1.0"
>>>>>>> db1998c... renamed the feature:features/analyse_software_stack.feature
