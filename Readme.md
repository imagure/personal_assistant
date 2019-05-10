
# Personal Assistant

##### English:
The Personal Assistant puts together diferent tools for Natural Language
Understanding and manages the negotiation between diferent people.

For a use case on english using Slack, see the video from the link:
https://www.youtube.com/watch?v=b4FkjeTk4yI

##### Portuguese:
O Personal Assistant reúne diferentes ferramentas 
de reconhecimento de linguagem natural e realiza a negociação
entre diferentes pessoas para marcar um compromisso!

Para ver um caso de uso em português no Slack, ver o vídeo no link:
https://www.youtube.com/watch?v=_MivRI66NpY&t=3s

## Getting Started

### Install the used packages with Pipenv

See used packages in Pipfile.
To install pipenv see: https://github.com/pypa/pipenv

To create a project environment with python 3.7 use:
```
pipenv --python 3.7
```
Enter the pipenv shell with:
```
pipenv shell
```
To install the packages from the Pipfile use:
```
pipenv install
```

### Create de DB with PostgreSQL

Download PostgreSQL (10.7). [https://www.postgresql.org]

At the root folder, execute:
```
psql -f db/create_database.sql
```

### External services

External services will also require specific keys. Right now, that's just for "Watson Assistant"

### Run the tests using pytest
To run the tests from the pipenv shell use:
```
python -m pytest -v tests/<module_test>/<name_test>.py 
```

To run a single test from within a module use:
```
python -m pytest -v tests/<module_test>/<name_test>.py -k "<single_test>" 
```

### About the Deploy

Deployment is currently being done on Heroku. To see Heroku's logs use:
```
heroku logs --tail
```

To access Heroku's database use:

```
heroku pg:psql
```

## Authors

* **Mateus R. Vendramini**
* **Ricardo C. C. Imagure**


See also the list of [contributors](https://github.com/ricardoimagure/personal_assistant/settings/collaboration) who participated in this project.

## License


## Acknowledgments
* Helped by:
    * **Bruno Tinen**
* Oriented by:
    * **Marcos R. P. Barreto**
* Also helped by the work from:
    * **Erich Natsubori Sato**
    * **Nicolas Silverio Figueiredo**
