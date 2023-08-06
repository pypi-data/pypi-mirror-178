# `cenc`

**Usage**:

Start an encoding task with passing the full ffmpeg command to the `cenc` command.

A trivial example that prints the version of ffmpeg on our system:

```bash
cenc ffmpeg --help
```

A more complex example that resizes a video file hosted on a remote server:

```bash
cenc ffmpeg -i 'https://storage.googleapis.com/kapan_public_videos/SampleVideo_1280x720_1mb%20(1).mp4' -vf scale=320:240 output.mp4
```

After the task has been started,
you will be given a task ID and 
the logs of the task will be printed to the console.

When the task is finished,
you can download the outputs of the task.
The url of the output files will be printed to the console, such as:

```
{
  "id": "b6c0d5607f224dc3b646068710d2e08a",
  "output.mp4": "https://storage.googleapis.com/store/tmp/ffmpeg/b6c0d5607f224dc3b646068710d2e08a/output.mp4",
  "returncode": "0",
  "status": "done"
}
```


## Using the API

The API is available at `https://ffmpeg-kopg2w5bka-ez.a.run.app`.
You can start a task by sending a POST request to the `/ffmpeg` endpoint.

```python
endpoint = "https://ffmpeg-kopg2w5bka-ez.a.run.app"
command = "ffmpeg -i 'https://storage.googleapis.com/kapan_public_videos/SampleVideo_1280x720_1mb%20(1).mp4' -vf scale=320:240 output.mp4"
response = requests.post(endpoint, params={"command": command})
task_id = response.json()["id"]
```

You can check the status of the task by sending a GET request to the `/ffmpeg/<task_id>` endpoint.

```python
while True:
    response = requests.get(f"{endpoint}/ffmpeg/{task_id}")
    if response.status_code != 200:
        # Task has not been started processing yet
        continue
    
    data = response.json()

    if data.get("returncode"):
        # Task has finished processing
        print(data)
        break
```