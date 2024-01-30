#!/bin/bash

celery -A application.tasks.celery worker -l INFO
