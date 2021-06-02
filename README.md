# project-gng-multiplayer-restful

This supports the GNG's leaderboard.

## Set Up
1. Create a virtual environment
```shell
$ python -m venv venv
```
2. Activate it:
- If you are in linux:
  ```shell
  $ source venv/bin/activate
  ```
- If you are in windows
  ```
  > venv\Scripts\activate
  ```
3. Create a `.env` file with
  ```shell
  FLASK_APP=api.py
  FLASK_RUN_PORT=8000
  FLASK_DEBUG=1
  ```
4. Migrate the db
  ```shell
  $ flask db init
  $ flask db upgrade
  ```
5. Now you're ready to run it. Ideally all you'll ever need from this point is activating the virtual environment and running it as shown below:
  ```shell
  $ flask run
  ```
