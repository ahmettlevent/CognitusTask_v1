# Async Task Queues - Local Alternatives 

### Redis Task Queue RQ
- #### Advantages
  - Bulk job enqueueing  
  - Job dependencies via mutex lock
  - Job callbacks (on_success & on_failure)
- #### Disadvantages
  - Each worker will process a single job at a time. Within a worker, there is no concurrent processing going on. If you want to perform jobs concurrently, you need to start more workers.
  - RQ workers will only run on systems that implement fork(). Most notably, this means it is not possible to run the workers on Windows without using the Windows Subsystem for Linux and running in a bash shell.

### Task Tiger
- #### Advantages
  - https://github.com/closeio/tasktiger#features"
- #### Disadvantages

### Task Master
- #### Advantages
  - 
- #### Disadvantages

### Huey
- #### Advantages
- #### Disadvantages

### Kuyruk
- #### Advantages
- #### Disadvantages

### Dramatiq
- #### Advantages
- #### Disadvantages

### Django-carrot
- #### Advantages
- #### Disadvantages

### tasq
- #### Advantages
- #### Disadvantages

### WorQ
- #### Advantages
- #### Disadvantages

# Celery Async Task - Cloud Based Solutions

### Google Task Queue API
- #### Advantages
- #### Disadvantages

### AWS's Cloud Watch Events
- #### Advantages
- #### Disadvantages
