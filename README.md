# Mirth VSCode JavaScript Runner

> IMPORTANT: This only works on localhosted mirth instances

This project gives us the ability to write JavaScript within VSCode and automatically run the channel after the file has been saved. It will then take the logs printed out and display them in the Run On Save Output.

## Requirements
- Python (3.10 >)
- Local Mirth Instance

## Instructions
1. Download this repository
2. Run `pip install -r requirements.txt` in console
3. Create your test js file within the repository folder.
4. Create channel within Mirth and edit the transformer to be an external script.
5. Add the location of the test js file to the external script transformer.
6. Create your test message on your local machine.
7. Within VS Code, download the Run On Save extension by emeraldwalk
8. Open Command Palette (Ctrl + Shift + P)
9. Search for "Preferences: Open Workspace Settings (JSON)"
10. Add the following json
```
{
    "emeraldwalk.runonsave": {
        "commands": [
            {
                "match": "*.js",
                "isAsync": true,
                "cmd": "py run_javascript.py -cid {channel_id} -msg {message_file_location}"
            }
        ]
    }
}
```
- replace {channel_id} with the channel id you intead to deploy and send a message to
- replace {message_file_location} with the file location with the message you want to send
11. Write your script within the test js file and save and watch it log out the logs for your channel within the Run On Save Output view.

## In Action
![](media/inaction.gif)