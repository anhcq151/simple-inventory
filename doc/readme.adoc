= Simple Inventory Manager

My very first python webapp, using Flask.
(STILL IN DEVELOPMENT...)

Containing basic features which match my personal requirements:

* Asset information: name/type, location, status, description
* Edit single asset item information
* Transfer log
* Item information change log

== Install

Clone this repo

[,bash]
----
git clone https://github.com/anhcq151/simple-inventory.git
----

=== Quick run under development environment

Prerequisites:

* `python 3.6` or newer
* `pipenv`

Change to cloned directory then install

[,bash]
----
pipenv install && pipenv install --dev
----

Start development server

[,bash]
----
pipenv shell
flask run
----

=== Run in container

Prerequisites:

* `podman` version 1.9 or newer and `buildah`

Execute `devcontainer.sh` script under link:.devcontainer[.devcontainer] directory to start using this app.

If `docker` is your preference, change to cloned repo and run:

[,bash]
----
docker volume create simple-inventory
docker build --tag simple-inventory .
docker run -d --mount type=volume,source=simple-inventory,destination=/opt/simple-inventory/data --name simple-inventory --publish 8000:5000 simple-inventory
----
