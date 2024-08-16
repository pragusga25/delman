@echo off

IF "%1"=="test" (
    coverage run --rcfile=.coveragerc -m unittest discover tests
    GOTO :EOF
)

IF "%1"=="coverage" (
    coverage report --rcfile=.coveragerc -m --include="app/services/*,app/routes/*"
    GOTO :EOF
)

IF "%1"=="coverage-html" (
    coverage html --rcfile=.coveragerc --include="app/services/*,app/routes/*"
    GOTO :EOF
)

echo Usage:
echo run_tests.bat test        - Run tests with coverage
echo run_tests.bat coverage    - Show coverage report
echo run_tests.bat coverage-html - Generate HTML coverage report
