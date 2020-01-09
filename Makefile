# On Linux, these commands will need to run with root privileges. Just invoke them manually.
all:
	docker build -t pascali_integration .
	docker run -it pascali_integration

PYTHON_FILES=`find . -name '*.py'`
python-style:
	yapf -i --style='{column_limit: 100}' ${PYTHON_FILES}
	pylint -f parseable --disable=W,line-too-long,invalid-name ${PYTHON_FILES}
