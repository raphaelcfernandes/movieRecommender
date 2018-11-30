# Required Dependencies 

MongoDB

NPM >= 3.5.2

python >= 3.6.5

Angular CLI

Download the ml-latest-small.zip (https://grouplens.org/datasets/movielens/latest/) and extract it inside server_side/routes

# Installation

npm install 

In order to have the right dataset, you need to execute the file createMongoDB.py inside server_side/scripts/ with the argument 20M for the movielens dataset with ml-latest, or with 100k to run it with ml-latest-small. This script will connect to your mongo dataset and will create a collection for you. Make sure your mongo service is running :).

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Development server

First run ng build with --watch flag to allow node to listen automatically to the directory built by Angular.

Run `nodemon` for a dev server. Navigate to `http://localhost:8080/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
