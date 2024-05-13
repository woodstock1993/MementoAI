from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

if __name__ == '__main__':
    app.start()