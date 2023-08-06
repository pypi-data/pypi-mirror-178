# hrin-msb

## Pre-requisites for setup
1. `pip install poetry`

## How To Build

1. `poetry build`
2. `poetry config http-basic.pypi __token__ <access-token>`
3. `poetry publish`


# Change Log
 ### Version 0.1.1

 ### Version 0.1.2

 ### Version 0.1.3

1.  Default serializer added to ApiView
2. fixed incorrect import in _validators.py
3. fixed msb_database_router
4. fixed Config.is_local_env() not working
5. moved devscripts -> utils/devtools
6. File Utils Added to utils/files
7. "app_label" removed from "TestConfig" & "ApiTest" Classes
8. Fixed Bug : 'LoggingModelManager' object has no attribute '_queryset_class'
9. Fixed : Logging Model not showing any records
10. Fixed : str method for base model, & removed current_timestamp method from base model