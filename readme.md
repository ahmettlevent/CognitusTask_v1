# Local Celery Async Task Alternatives

* ### Redis Task Queue RQ

#### Advantages
- Each worker will process a single job at a time. Within a worker, there is no concurrent processing going on. If you want to perform jobs concurrently, simply start more workers.

* ### Task Tiger

#### Advantages
- https://github.com/closeio/tasktiger#features"

* ### Task Master

* ### Huey

* ### Kuyruk

* ### Dramatiq

* ### Django-carrot

* ### tasq

* ### WorQ

# Cloud Based Celery Async Task Solutions

* ### Google Task Queue API

* ### AWS's Cloud Watch Events
